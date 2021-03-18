import datetime
import os
import struct
import threading
import time
from multiprocessing import Process
import multiprocessing as mp
import cprint
import snap7

from core.bind_error import BindError
from settings import createConnection


class StartProcessOpcForConnectToPLC(Process):

    def __init__(self, address: str, rack: int, slot: int, db: int, start_address_db: int, offset_db: int,
                 values_list: list = None, port=102, name_connect: str = "", status=[], count=0, oee:list = None):
        """Класс процесса для подключения к ПЛК по адресу address, с портом port (по умолчанию 102) и получения заданных
        значений из блока данных db в промежутке с start_address_db по start_address_db+offset_db
        (offset_db - количество забираемых byte из блока). После получения данных разбирает bytearray по
        списку values_list.

        :param address: ip адрес ПЛК
        :param rack:  линейка ПЛК (смотри в Step7 или Tia POrtal)
        :param slot: номер слота ПЛК (смотри в Step7 или Tia POrtal)
        :param db: номер ДБ блока данных в ПЛК
        :param start_address_db: начальный адрес ДБ в ПЛК
        :param offset_db: количество читаемых байт в ДБ
        :param values_list: список значений которые нужно разобрать из bytearray в числовые
        :param port: номер порта (по умолчанию 102)
        :param name_connect: префикс названия таблиц для подключения

        """
        if values_list is None:
            values_list = []
        self.name_connect = name_connect
        self.address = address
        self.status = status
        self.count = count
        self.rack = rack
        self.slot = slot
        self.port = port
        self.DB = db
        self.start_address_DB = start_address_db
        self.offset_DB = offset_db
        self.values_list = values_list
        self.bind = {}
        self.error_read_data = False
        self.last_error = ''
        self.bytearray_data = bytearray()
        self.values = {}
        self.oee = oee
        self.oee_status = {}
        self._conn = createConnection()
        self._c = self._conn.cursor()
        self.alarms_hash={}

        self.client = snap7.client.Client()
        self.client.set_connection_type(3)
        try:
            self.client.connect(self.address, self.rack, self.slot, tcpport=self.port)
        except:
            cprint.cprint.err("NotConnect to PLC")
        super(StartProcessOpcForConnectToPLC, self).__init__()

    def __get_db_data(self) -> bool:  # получение данных в байт формате
        """
        получение данных из ДБ блока в формате bytearray
        """
        try:
            self.bytearray_data = self.client.db_read(self.DB, self.start_address_DB, self.offset_DB)
            return True
        except Exception as e:
            self.last_error = str(e)
            self.error_read_data = True
            return False

    def __reconect_to_plc(self) -> bool:
        """пере подключение к плк в случае ошибки валидации данных"""
        cprint.cprint.warn("Переподключаюсь к ПЛК %s" % self.address)
        self.client.destroy()
        try:
            self.client = snap7.client.Client()
            self.client.set_connection_type(3)
            self.client.connect(self.address, self.rack, self.slot, tcpport=self.port)
            cprint.cprint.info("Удачно подключился к %s" % self.address)
            return True
        except:
            time.sleep(3)
            return False

    def __create_table_if_not_exist(self) -> None:
        """фнкция создания таблиц в БД"""
        cprint.cprint.info("Создаем таблицы")
        self._c.execute('''CREATE TABLE IF NOT EXISTS mvlab_alarms \
        (key serial primary key,now_time TIMESTAMP  WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, end_time TIMESTAMP  WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, \
        text_alarm TEXT, status int, type_alarm VARCHAR(100), object_alarm TEXT)''')
        self._c.execute('''CREATE TABLE IF NOT EXISTS mvlab_warnings \
                (key serial primary key,now_time TIMESTAMP  WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, \
                text_alarm TEXT, status int, type_alarm VARCHAR(100), object_alarm TEXT)''')
        self._conn.commit()
        for q in self.values_list:
            if (q['table'] == 'int'):
                vsql = 'INT'
            if (q['table'] == 'real'):
                vsql = 'REAL'
            if (q['table'] == 'double'):
                vsql = 'BIGINT'
            if (q['table'] == 'bool'):
                vsql = 'int'
            q['name'] = self.name_connect + '''_''' + q['name']
            if q['divide']:
                self._c.execute('''CREATE TABLE IF NOT EXISTS mvlab_temp_''' + q['name'] + ''' \
                                                                        (key serial primary key,now_time TIMESTAMP  WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, \
                                                                        value ''' + vsql + ''')''')
                self._c.execute('''CREATE TABLE IF NOT EXISTS mvlab_''' + q['name'] + ''' \
                                                                                    (key serial primary key,now_time TIMESTAMP  WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, \
                                                                                    value ''' + vsql + ''')''')
                self._conn.commit()
            else:
                self._c.execute('''CREATE TABLE IF NOT EXISTS mvlab_''' + q['name'] + ''' \
                                (key serial primary key,now_time TIMESTAMP  WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, \
                                value ''' + vsql + ''')''')
                self._conn.commit()

    def __parse_bytearray(self, data: dict) -> any:
        """разбор полученных данных с ПЛК"""
        type = data['type']
        start = data['start']
        if (type == 'int'):
            offset = 2
            end = int(start) + int(offset)
            result = self.disassemble_int(self.bytearray_data[int(start):int(end)])
            if data['divide']:
                if result > 65000:
                    result = 0
                else:
                    result = result / 10
        elif (type == 'real'):
            offset = 4
            end = int(start) + int(offset)
            result = self.disassemble_float(self.bytearray_data[int(start):int(end)])
        elif (type == 'double'):
            offset = 4
            end = int(start) + int(offset)
            result = self.disassemble_int(self.bytearray_data[int(start):int(end)])
        elif (type == 'bool'):
            result = self.from_bytearray_to_bit(bit=data['bit'], start=start)
        else:
            result = False
        return result

    def __write_to_db(self, tablename, value, divide):
        """Запись распаршеных данных в БД"""
        if divide:
            self._c.execute(
                '''INSERT INTO mvlab_temp_''' + tablename + ''' (value) VALUES (''' + str(value) + ''');''')
        else:
            self._c.execute(
                '''INSERT INTO mvlab_''' + tablename + ''' (value) VALUES (''' + str(value) + ''');''')

    def _thread_for_write_data(self, d):
        value = self.__parse_bytearray(d)
        if 'if_change' in d and d['if_change'] and not d['name'] in self.values:
            cprint.cprint.info("create last value in %s " % d['name'])
            self.values[d['name']] = value
            self.__write_to_db(tablename=d['name'], value=value, divide=d['divide'])
        if 'alarms' in d:
            x = threading.Thread(target=self.add_to_alarm_new, args=(d,))
            x.start()

        if 'if_change' in d and d['if_change'] and self.values[d['name']] != value:
            self.values[d['name']] = value
            self.__write_to_db(tablename=d['name'], value=value, divide=d['divide'])
        if 'alarms' in d:
            x = threading.Thread(target=self.add_to_alarm_new, args=(d,))
            x.start()

        if 'if_change' in d and not d['if_change']:
            self.__write_to_db(tablename=d['name'], value=value, divide=d['divide'])
        if 'alarms' in d:
            x = threading.Thread(target=self.add_to_alarm_new, args=(d,))
            x.start()

    def add_to_16_bit(self, string):
        while len(string)<16:
            string = "0"+string
        string1 = string[0:8]
        string2 = string[8::]
        return string2+string1

    def check_bit_in_int(self, value, bit):
        #value = int.from_bytes(int.to_bytes(value, byteorder='little'), byteorder='little', signed=True)
        bits = bin(value)
        print("88" * 12)
        print(bits)
        bits = bits.replace("0b", "")

        bits = self.add_to_16_bit(bits)
        bits = bits[::-1]
        print("77" * 12)
        print(bits)
        try:
            status = bits[bit]
        except:
            status = 0
        return status

    def add_to_alarm_new(self, d):
        cprint.cprint.err('add alarm')
        if d['name'] not in self.alarms_hash:
            self.alarms_hash[d['name']] = {}
        for a in d['alarms']:
            if a['text'] not in self.alarms_hash[d['name']]:
                self.alarms_hash[d['name']][a['text']] = 0
            status = self.check_bit_in_int(self.values[d['name']], int(a['bit']))
            if self.alarms_hash[d['name']][a['text']] == status:
               continue

            if status == "0":
                try:
                    self._c.execute(
                        """UPDATE mvlab_alarms SET status = 0, end_time = '"""+str(datetime.datetime.now())+"""'  WHERE status=1 and text_alarm = '""" + str(a['text']) + """' and \
                         type_alarm='""" + str(a['type']) + """' and  object_alarm='""" + str(d['name']) + """';""")
                    self._conn.commit()
                except:
                    pass


            if status == "1":
                if a['type'] == "alarm":
                    tablename = "alarms"
                else:
                    tablename = "warnings"
                records = []
                try:
                    self._c.execute(
                        """SELECT COUNT(*) FROM mvlab_alarms  WHERE status=1 and text_alarm = '""" + str(a['text']) + """' and \
                         type_alarm='""" + str(a['type']) + """' and  object_alarm='""" + str(d['name']) + """';""")
                    records = self._c.fetchall()

                except:
                    self._c.execute(
                        '''INSERT INTO mvlab_alarms''' \
                        """ (text_alarm, status,type_alarm,object_alarm) VALUES ('""" + str(
                            a['text']) + """','""" + str(
                            1) + """','""" + str(a['type']) + """','""" + str(d['name']) + """');""")
                    self._conn.commit()
                    return False
                try:
                    cprint.cprint.warn("--"*45)
                    print(records)
                    if len(records)>0:
                        pass
                    else:
                        self._c.execute(
                            '''INSERT INTO mvlab_alarms'''\
                            """ (text_alarm, status,type_alarm,object_alarm) VALUES ('""" + str(a['text']) + """','""" + str(
                                1) + """','""" + str(a['type']) + """','""" + str(d['name']) + """');""")
                        self._conn.commit()
                except:
                    self._c.execute(
                        '''INSERT INTO mvlab_alarms''' \
                        """ (text_alarm, status,type_alarm,object_alarm) VALUES ('""" + str(
                            a['text']) + """','""" + str(
                            1) + """','""" + str(a['type']) + """','""" + str(d['name']) + """');""")
                    self._conn.commit()
                    cprint.cprint.info("error in 202 string proccess.py")
                self.alarms_hash[d['name']][a['text']] = status
            return status

    def oee_module(self) -> None:
        """парсинг оее и запись в таблицы"""
        for e in self.oee: # проходим по списку ОЕЕ для подключения
            oee_status = self.find_oee_status(e)
            if oee_status['table_name'] not in self.oee_status:
                self.oee_status[oee_status['table_name']] = int(oee_status['type'])
                self.write_change_oee_to_db(oee_status)
            else:
                if self.oee_status[oee_status['table_name']] != int(oee_status['type']):
                    self.write_change_oee_to_db(oee_status)
                    self.oee_status[oee_status['table_name']] = int(oee_status['type'])


    def write_change_oee_to_db(self, oee:dict) -> None:
        """запись структурированнфх данных в БД"""
        self._c.execute(
            '''INSERT INTO mvlab_oee_''' + oee['table_name'] + ''' (value) VALUES (''' + str(oee['type']) + ''');''')
        self._conn.commit()

    def find_oee_status(self, e) -> dict:
        pre_result = self.disassemble_int(self.bytearray_data[int(e['start']):int(e['end'])])
        for res in e['status']:
            result = pre_result & res['factor']
            if result == res['value']:
                res['table_name'] = e['table_name']
                res['name'] = e['name']
                return res
        del pre_result


    def create_table_oee(self) -> None:
        """создание таблиц для ОЕЕ """
        for oee in self.oee:
            self._c.execute('''CREATE TABLE IF NOT EXISTS mvlab_oee_''' + oee['table_name'] + ''' \
                            (key serial primary key,now_time TIMESTAMP  WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, \
                            value int)''')
        self._c.execute('''CREATE TABLE IF NOT EXISTS mvlab_oee_list \
                                    (key serial primary key,date_add TIMESTAMP  WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, \
                                    name varchar(255), table_name varchar(255))''')
        self._conn.commit()

    def run(self):
        """основной цикл процесса"""
        self.__create_table_if_not_exist()  # создание таблиц если их нет
        if self.oee is not None:
            self.create_table_oee() # создаем таблицы для ОЕЕ если их нет
        while True:
            start_time = time.time()
            if (not self.__get_db_data()):
                self.__reconect_to_plc()
                self.status[self.count] = 0
            else:
                threads = list()
                if self.oee is not None:
                    self.oee_module()
                for d in self.values_list: # проход по массиву данных подключения
                    if d['name'] not in self.bind and d['divide']: # проверка на первый запуск.
                        # Если отслеживание включено но данной переменной нет в массиве с переменными слежения,
                        # то добавляем ее и включаем слежение
                        self.bind[d['name']] = BindError(self.bytearray_data, d)
                    if d['divide']: # если переменная отслеживается то чекаем аварию
                        self.bind[d['name']].bind_error_function(data=self.bytearray_data, c=d)
                    x = threading.Thread(target=self._thread_for_write_data, args=(d,))
                    threads.append(x)
                    while threading.active_count() > 250:
                        time.sleep(0.01)
                    x.start()
                for thread in threads:
                    thread.join()
                self._conn.commit()
                self.status[self.count] = 1

    def disassemble_float(self, data) -> float:  # метод для преобразования данных в real
        val = struct.unpack('>f', data)
        return val[0]

    def disassemble_double(self, data) -> int:  # метод для преобразования данных в bigint
        val = struct.unpack('>d', data)
        return val[0]

    def disassemble_int(self, data) -> int:  # метод для преобразования данных в int
        return int.from_bytes(data, "big", signed=True)

    def from_bytearray_to_bit(self, bit, start) -> int:
        value = int.from_bytes(self.bytearray_data[int(start):int(start) + 1], byteorder='little', signed=True)
        bits = bin(value)
        bits = bits.replace("0b", "")
        bits = bits[::-1]
        try:
            result = bits[bit]
        except:
            result = 0
        return result
