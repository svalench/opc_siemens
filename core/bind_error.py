import datetime
import threading
import asyncio
from cprint import cprint

from settings import createConnection


class BindError:
    """Клас для отслеживания состояния скоростных данных. Если прошло время self.dleay_upd то переносим их в таблицу долговременного хранения
     с усреднением данных в интервале self.dleay_upd (мин) вызывая метод __transfer_data.
    Если произола авария запрещаем перенос и выжидаем время self.deleay после чего переносим все данные без усреднения в таблицу долговременного хранения
    с временными рамками +-self.deleay с момента начала события (аварии)

     Methods
    ==========

     - __transfer_data - перенос данных из временной таблицы в основную с усреднением
     - bind_error_function геттер класса
     - __transfer_accident_data - перенсо данных если произошла авария
     - _try_to_connect_db - подключение к БД

    """
    def __init__(self,data,c):
        self.data = data
        self.c = c
        self.__accident = 0
        self.__accident_temp = 0
        self.__accident_last = 0
        self.__accident_start_time = 0
        self.__accident_end_time = 0
        self.__accident_last = 0
        self.__last_update = datetime.datetime.now()
        self.deleay = 10
        self.dleay_upd = self.deleay*2
        self.__interval = 3
        self.transfer_start = False


    def transform_data_to_bit(self, offset, bit, data):
        """получение статуса бита в прочитанном массиве данных"""
        value = int.from_bytes(data[int(offset):int(offset) + 1], byteorder='little', signed=True)
        bits = bin(value)
        bits = bits.replace("0b", "")
        bits = bits[::-1]
        try:
            status = bits[bit]
        except:
            status = 0
        return status

    def bind_error_function(self, data, c) -> None:
        """Метод для опредления необходимо ли отслеживание аварии для переменной. Происходит расчет начала и конца временного периода аварии"""
        self.__accident_last = self.__accident
        if 'byte_bind' in c:
            self.__accident = int(self.transform_data_to_bit(offset=int(c['byte_bind']), bit=int(c['bit_bind']),
                                                             data=data))
            # проверяем происходило ли событие до этого
            if self.__accident == 1:
                _conn = createConnection()
                _c = _conn.cursor()
                _c.execute(
                    '''INSERT INTO mvlab_alarms''' \
                    """ (text_alarm, status,type_alarm,object_alarm) VALUES ('оствнов машин','""" + str(
                        1) + """','alarm','""" + str(c['name']) + """');""")
                _conn.commit()
                _conn.close()
                self.__accident_temp = self.__accident
                if self.__accident_start_time == 0:
                    #  если событие происходит в первый раз то сохраняем с какого периода выбрать данные
                    self.__accident_start_time = datetime.datetime.now() - datetime.timedelta(minutes=self.deleay)
                    self.__accident_end_time = datetime.datetime.now() + datetime.timedelta(minutes=self.deleay)
                if self.__accident_last != self.__accident:
                    self.__accident_end_time = datetime.datetime.now() + datetime.timedelta(minutes=self.deleay)
            self.__transfer_accident_data(self.c['name'])
        else:
            if (self.__accident_end_time == 0 and not self.transfer_start and
                    self.__accident_start_time == 0 and
                    self.__accident_temp == 0 and
                    self.__last_update < datetime.datetime.now() - datetime.timedelta(minutes=self.dleay_upd)):
                # self.__transfer_data(self.c['name'])
                x = threading.Thread(target=self.__transfer_data, args=(self.c['name'],))
                x.start()
                self.transfer_start = True

    def __transfer_data(self, tablename) -> None:
        """Проверяет сколько времени прошло с мометна последеней записи если вышло за рамки __last_update  то перезаписываем в основню таблицу"""
        f = '%Y-%m-%d %H:%M:%S'
        if (self.__accident_end_time == 0 and
                self.__accident_start_time == 0 and
                self.__accident_temp == 0 and
                self.__last_update < datetime.datetime.now() - datetime.timedelta(minutes=self.dleay_upd)):
            _conn = createConnection()
            _c = _conn.cursor()
            #self._try_to_connect_db()
            start_update = datetime.datetime.now() - datetime.timedelta(days=7)
            end_update = datetime.datetime.now() - datetime.timedelta(minutes=self.dleay_upd)
            start_update = start_update.strftime(f)
            end_update = end_update.strftime(f)
            sql = "WITH temp as (SELECT n as tt from generate_series('" + str(start_update) + "'::timestamp,'" + str(
                end_update) + "'::timestamp,'" + str(self.__interval) + " minute'::interval) n ) \
        INSERT  INTO  mvlab_" + str(
                tablename) + " (now_time, value) SELECT tt,(SELECT mode() WITHIN GROUP (ORDER BY value) as modevar FROM mvlab_temp_" + str(
                tablename) + " r WHERE  r.now_time>b.tt and r.now_time<=(b.tt+('" + str(self.__interval) + " minutes'::interval))) as value \
        from mvlab_temp_" + str(tablename) + " a LEFT JOIN temp b ON a.now_time>b.tt and a.now_time<=(b.tt+('" + str(
                self.__interval) + " minutes'::interval)) WHERE a.value IS NOT NULL GROUP BY tt ORDER BY tt asc;"
            _c.execute(sql)
            _conn.commit()
            _c.execute(
                '''DELETE FROM mvlab_temp_''' + tablename + ''' WHERE
                                                 "now_time" >= %s AND 
                                                 "now_time" < %s  ;''', [start_update, end_update])
            _conn.commit()
            self.__last_update = datetime.datetime.now()
            _conn.close()
            self.transfer_start = False

    def __transfer_accident_data(self, tablename):
        """Функция следит за данными если время пришло усредняет их или если произошла авария """
        f = '%Y-%m-%d %H:%M:%S'
        self.__transfer_data(tablename)
        # если время вышло и была активна ошибка то переносим данные
        if (type(self.__accident_end_time)==type(datetime.datetime.now())
                and self.__accident_end_time < datetime.datetime.now()
                and self.__accident_temp==1):
            self._try_to_connect_db()
            totalsec_start = self.__accident_start_time.strftime(f)
            totalsec_end = self.__accident_end_time.strftime(f)
            self._c.execute(
                '''INSERT  INTO  mvlab_'''+tablename+''' (now_time, value)
                 SELECT now_time, value FROM mvlab_temp_'''+tablename+''' WHERE
                 "now_time">= %s AND 
                 "now_time"< %s  ;''',[totalsec_start,totalsec_end])
            try:
                self._conn.commit()
            except Exception as e:
                cprint.err('error переноса данных: %s' % e)
            self._c.execute(
                '''DELETE FROM mvlab_temp_'''+tablename+''' WHERE
                             "now_time" >= %s AND 
                             "now_time" < %s  ;''',[totalsec_start,totalsec_end])
            try:
                self._conn.commit()
                self.__accident_temp = 0
                self.__accident_start_time = 0
                self.__accident_end_time = 0
                self._conn.close()
            except Exception as e:
                cprint.err('error переноса данных: %s' % e)

    def _try_to_connect_db(self):
        """Connected to DB"""
        try:
            self._conn = createConnection()
            self._c = self._conn.cursor()
        except:
            cprint.err('error connection to DB for ', interrupt=False)