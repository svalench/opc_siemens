import multiprocessing as mp

list_data = [
    {"name": "p1101", "start": 0, "type": "int", 'table': 'real', "itarable": True, 'divide': True, 'if_change': False,
     'byte_bind': 168, 'bit_bind': 0, "hint": "Разряжение газа на входе компрессорной"},
    {"name": "p1201", "start": 2, "type": "int", 'table': 'real', "itarable": True, 'divide': True, 'if_change': False,
     'byte_bind': 168, 'bit_bind': 0, "hint": "Компрессор 1 - Текущее давление"},
    {"name": "p1202", "start": 4, "type": "int", 'table': 'real', "itarable": True, 'divide': True, 'if_change': False,
     'byte_bind': 168, 'bit_bind': 0, "hint": "Компрессор 1 - Текущее разряжение"},
    {"name": "p1301", "start": 6, "type": "int", 'table': 'real', "itarable": True, 'divide': True, 'if_change': False,
     'byte_bind': 168, 'bit_bind': 0, "hint": "Компрессор 2 - Текущее давление"},
    {"name": "p1302", "start": 8, "type": "int", 'table': 'real', "itarable": True, 'divide': True, 'if_change': False,
     'byte_bind': 168, 'bit_bind': 0, "hint": "Компрессор 2 - Текущее разряжение"},
    {"name": "p1401", "start": 10, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Компрессор 3 - Текущее давление"},
    {"name": "p1402", "start": 12, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Компрессор 2 - Текущее разряжение"},
    {"name": "p1501", "start": 14, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Давление газа на выходе компрессорной"},
    {"name": "p1502", "start": 16, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Камера ГР1 - давление газа"},
    {"name": "p1601", "start": 18, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "ГПА1 - давление газа"},
    {"name": "p1701", "start": 20, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "ГПА2 - давление газа"},
    {"name": "p1801", "start": 22, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "ГПА3 - давление газа"},
    {"name": "p1901", "start": 24, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Факел - давление газа"},
    {"name": "pdcah1103", "start": 26, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Демистр - превышение перепада давления"},
    {"name": "pdcah1104", "start": 28, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Дефлаграционный предохранитель S1104 - превышение перепада давления"},
    {"name": "pdcah1601", "start": 30, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Дефлаграционный предохранитель S1601 (ГПА1 D0601) - превышение перепада давления"},
    {"name": "pdcah1701", "start": 32, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Дефлаграционный предохранитель SXXXX (ГПА2 D0602) - превышение перепада давления"},
    {"name": "pdcah1801", "start": 34, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Дефлаграционный предохранитель SXXXX (ГПА3 D0603) - превышение перепада давления"},
    {"name": "pdcah1901", "start": 36, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Дефлаграционный предохранитель S1901 (факел) - превышение перепада давления"},
    {"name": "pw1600", "start": 38, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "___"},
    {"name": "pw1700", "start": 40, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "___"},
    {"name": "pw1800", "start": 42, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "___"},
    {"name": "pw1900", "start": 44, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "___"},
    {"name": "pzal1201", "start": 46, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Компрессор 1 - превышение давление"},
    {"name": "pzal1301", "start": 48, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Компрессор 2 - превышение давление"},
    {"name": "pzal1401", "start": 50, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Компрессор 3 - превышение давление"},
    {"name": "co2_1101", "start": 52, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Газоанализатор - содержание СО2"},
    {"name": "qziah_o2_1101", "start": 54, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Газоанализатор - содержание О2"},
    {"name": "qzial_ch4_1101", "start": 56, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Газоанализатор - содержание СН4"},
    {"name": "T1501", "start": 58, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Температура газа - компрессорная"},
    {"name": "T1601", "start": 60, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Температура газа - ГПА1 D0601"},
    {"name": "T1701", "start": 62, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Температура газа - ГПА2 D0602"},
    {"name": "T1801", "start": 64, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Температура газа - ГПА3 D0603"},
    {"name": "T1901", "start": 66, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Температура газа - факел"},
    {"name": "TK1901", "start": 68, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Температура пламени - факел"},
    {"name": "tshl1101", "start": 70, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Температура газа в дефлаграционном предохранителе - факел"},
    {"name": "tzah1101", "start": 72, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "___"},
    {"name": "tzah1201", "start": 74, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Компрессор 1 - температура газа вход"},
    {"name": "tzah1202", "start": 76, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Компрессор 1 - превышение температуры"},
    {"name": "tzah1203", "start": 78, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Компрессор 1 - температура газа выход"},
    {"name": "tzah1301", "start": 80, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Компрессор 2 - температура газа вход"},
    {"name": "tzah1302", "start": 82, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Компрессор 2 - превышение температуры"},
    {"name": "tzah1303", "start": 84, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Компрессор 2 - температура газа выход"},
    {"name": "tzah1401", "start": 86, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Компрессор 3 - температура газа вход"},
    {"name": "tzah1402", "start": 88, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Компрессор 3 - превышение температуры"},
    {"name": "tzah1403", "start": 90, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Компрессор 3 - температура газа выход"},
    {"name": "tzah1601", "start": 92, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Температура газа в дефлаграционном предохранителе - ГПА1 В0601"},
    {"name": "tzah1701", "start": 94, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Температура газа в дефлаграционном предохранителе - ГПА1 В0602"},
    {"name": "tzah1801", "start": 96, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Температура газа в дефлаграционном предохранителе - ГПА1 В0603"},
    {"name": "d601_ch4_gpa1", "start": 98, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Концентрация метана"},
    {"name": "d602_ch4_gpa2", "start": 100, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Концентрация метана"},
    {"name": "d603_ch4_gpa3", "start": 102, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Концентрация метана"},
    {"name": "d604_ch4_gpa4", "start": 104, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Концентрация метана"},
    {"name": "d601_la_gpa1", "start": 106, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "___"},
    {"name": "d602_la_gpa2", "start": 108, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "___"},
    {"name": "d603_la_gpa3", "start": 110, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "___"},
    {"name": "d604_la_gpa4", "start": 112, "type": "int", 'table': 'real', "itarable": True, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "___"},

    # Значения частотников
    {"name": "freq_v501", "start": 114, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Частота ПЧ1"},
    {"name": "freq_v502", "start": 116, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Частота ПЧ2"},
    {"name": "freq_v503", "start": 118, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Частота ПЧ3"},
    {"name": "qur_v501", "start": 120, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Ток ПЧ1"},
    {"name": "qur_v502", "start": 122, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Ток ПЧ2"},
    {"name": "qur_v503", "start": 124, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Ток ПЧ3"},
    {"name": "moment_v501", "start": 126, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Момент ПЧ1"},
    {"name": "moment_v502", "start": 128, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Момент ПЧ2"},
    {"name": "moment_v503", "start": 130, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Момент ПЧ3"},

    {"name": "flow_fi1501", "start": 150, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Расход общий"},
    {"name": "flow_fi1601", "start": 152, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Расход линии 1"},
    {"name": "flow_fi1701", "start": 154, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Расход линии 2"},
    {"name": "flow_fi1801", "start": 156, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Расход линии 3"},
    {"name": "flow_fi1901", "start": 158, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Расход линии 4"},

    # Мощности машин
    {"name": "power1", "start": 160, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Мощность D0601"},
    {"name": "power2", "start": 162, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Мощность D0602"},
    {"name": "power3", "start": 164, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Мощность D0603"},
    {"name": "power_sum", "start": 166, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, 'byte_bind': 168, 'bit_bind': 0, "hint": "Мощность D0604"},
]

list_data1 = [
    {"name": "iso1", "start": 0, "type": "double", 'table': 'double', "itarable": False, 'divide': False,
     'if_change': False, "hint": "___"},
    {"name": "pol1", "start": 36, "type": "double", 'table': 'double', "itarable": False, 'divide': False,
     'if_change': False, "hint": "___"},
    {"name": "pol2", "start": 40, "type": "double", 'table': 'double', "itarable": False, 'divide': False,
     'if_change': False, "hint": "___"}
]

list_data2 = [
    {"name": "vibro1", "start": 0, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, "hint": "Вибрация левый подшипник - 1"},
    {"name": "vibro2", "start": 2, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, "hint": "Вибрация правый подшипник - 1"},
    {"name": "vibro3", "start": 4, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, "hint": "Вибрация левый подшипник - 2"},
    {"name": "vibro4", "start": 6, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, "hint": "Вибрация правый подшипник - 2"},
    {"name": "vibro5", "start": 8, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, "hint": "Вибрация левый подшипник - 3"},
    {"name": "vibro6", "start": 10, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, "hint": "Вибрация правый подшипник - 3"},
    {"name": "temp1", "start": 12, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, "hint": "Температура левый подшипник - 1"},
    {"name": "temp2", "start": 14, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, "hint": "Температура правый подшипник - 1"},
    {"name": "temp3", "start": 16, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, "hint": "Температура левый подшипник - 2"},
    {"name": "temp4", "start": 18, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, "hint": "Температура правый подшипник - 2"},
    {"name": "temp5", "start": 20, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, "hint": "Температура левый подшипник - 3"},
    {"name": "temp6", "start": 22, "type": "int", 'table': 'real', "itarable": False, 'divide': True,
     'if_change': False, "hint": "Температура правый подшипник - 3"},
]

list_data_not_speed_s300_low_limits_warn = [
    {'name': 'low_limit_warning_%s' % i['name'], 'start': (100 * int(k) + 14), 'type': 'real', 'table': 'real',
     "itarable": False, 'divide': False, 'if_change': True, 'hint': i["hint"]} for k, i in enumerate(list_data) if i['itarable']]

list_data_not_speed_s300_hight_limits_warn = [
    {'name': 'hight_limit_warning_%s' % i['name'], 'start': (100 * int(k) + 18), 'type': 'real', 'table': 'real',
     "itarable": False, 'divide': False, 'if_change': True, 'hint': i["hint"]} for k, i in enumerate(list_data) if i['itarable']]

list_data_not_speed_s300_low_limits_error = [
    {'name': 'low_limit_error_%s' % i['name'], 'start': (100 * int(k) + 22), 'type': 'real', 'table': 'real',
     "itarable": False, 'divide': False, 'if_change': True, 'hint': i["hint"]} for k, i in enumerate(list_data) if i['itarable']]

list_data_not_speed_s300_hight_limits_error = [
    {'name': 'hight_limit_error_%s' % i['name'], 'start': (100 * int(k) + 26), 'type': 'real', 'table': 'real',
     "itarable": False, 'divide': False, 'if_change': True, 'hint': i["hint"]} for k, i in enumerate(list_data) if i['itarable']]

text_alarm = [
    {"name": "Авария - сработка нижнего аварийного предела", "type": "alarm"},
    {"name": "Авария - сработка нижнего предела предупреждения", "type": "warning"},
    {"name": "Авария - сработка верхнего предела предупреждения", "type": "warning"},
    {"name": "Авария - сработка верхнего аварийного предела", "type": "alarm"},
    {"name": "Авария - сработка верхнего предела рассогласования", "type": "alarm"},
    {"name": "Авария - сработка верхнего предела изменения скорости", "type": "alarm"},
]

struct_alarm_word_all1 = [
    {"name": "ОГРАНИЧИТЕЛЬ ПЕРЕНАПРЯЖЕНИЙ", "type": "alarm"},
    {"name": "F3 Частотный преобразователь, предохранитель", "type": "alarm"},
    {"name": "F12 2-х фазная розетка, предохранитель", "type": "alarm"},
    {"name": "F14 3-х фазная розетка, предохранитель", "type": "alarm"},
    {"name": "F4 (A0604) Факел, предохранитель", "type": "alarm"},
    {"name": "1. предохранитель насоса (Р301)", "type": "alarm"},
    {"name": "2. предохранитель насоса (Р302)", "type": "alarm"},
    {"name": "F1 Автомат вентилятора", "type": "alarm"},
    {"name": "F2 газовый вентилятор, предохранитель", "type": "alarm"},
    {"name": "F7 газоизмерит. станция, предохранитель", "type": "alarm"},
    {"name": "Вентилятор щитовой, предохранитель", "type": "alarm"},
    {"name": "F10 Обогреватель щитовой, предохраниель", "type": "alarm"},
    {"name": "Уровень конденсата Конденсатный колодец K1101 (LZAH) НОРМАЛЬНЫЙ УРОВЕНЬ", "type": "alarm"},
    {"name": "Конденсатный колодец K1101 (LZAH) ВЫСОКИЙ УРОВЕНЬ", "type": "alarm"},
    {"name": "Защита компрессора", "type": "alarm"},
    {"name": "F11 Обогреватель , предохраниель", "type": "alarm"},
]

struct_alarm_word_all2 = [
    {"name": "V1 аварийный выключатель", "type": "alarm"},
    {"name": "V2 аварийный выключатель", "type": "alarm"},
    {"name": "KV1 аварийная остановка", "type": "alarm"},
    {"name": "KV2 аварийная остановка", "type": "alarm"},
    {"name": "KV3 аварийная остановка", "type": "alarm"},
    {"name": "KV4 аварийная остановка", "type": "alarm"},
    {"name": "RF Задымление", "type": "alarm"},
    {"name": "F18 газосигнализатор, предохранитель", "type": "alarm"},
    {"name": "Тревога! Утечка газа, 40 %", "type": "alarm"},
    {"name": "Тревога! Утечка газа, 20 %", "type": "alarm"},
    {"name": "3. предохранитель датчика вибрации", "type": "alarm"},
    {"name": "4. предохранитель датчика вибрации", "type": "alarm"},
    {"name": "5. предохранитель датчика вибрации", "type": "alarm"},
    {"name": "6. предохранитель датчика вибрации", "type": "alarm"},
    {"name": "газосигнализатор, ошибка", "type": "alarm"},
    {"name": "F31, F32, 1., 2. предохранитель датчика вибрации", "type": "alarm"},
]

struct_alarm_word_all3 = [
    {"name": "RD Диагностич. модуль", "type": "alarm"},
    {"name": "F35 Автомат контр. напр.", "type": "alarm"},
    {"name": "F13 Автомат освещения", "type": "alarm"},
    {"name": "F15 Автомат", "type": "alarm"},
    {"name": "Q1 Выключатель", "type": "alarm"},
    {"name": "24VDC Powersupply", "type": "alarm"},
    {"name": "F3 Частотный преобразователь, предохранитель", "type": "alarm"},
    {"name": "F3 Частотный преобразователь, предохранитель", "type": "alarm"},
]

alarm_all_world = [
    {
        "name": "alarm_all1",
        "start": 5856,
        'type': 'int',
        'table': 'int',
        "itarable": False,
        'divide': False,
        'if_change': True,
        'alarms': [{"bit": s, "text": str(a['name']), "type": a['type']} for s, a in enumerate(struct_alarm_word_all1)]
    },
    {
        "name": "alarm_all2",
        "start": 5858,
        'type': 'int',
        'table': 'int',
        "itarable": False,
        'divide': False,
        'if_change': True,
        'alarms': [{"bit": s, "text": str(a['name']), "type": a['type']} for s, a in enumerate(struct_alarm_word_all2)]
    },
    {
        "name": "alarm_all3",
        "start": 5860,
        'type': 'int',
        'table': 'int',
        "itarable": False,
        'divide': False,
        'if_change': True,
        'alarms': [{"bit": s, "text": str(a['name']), "type": a['type']} for s, a in enumerate(struct_alarm_word_all3)]
    },
]

alarm_world = [
    {'name': 'alarm_world_%s' % i['name'],
     'start': (100 * int(k) + 56),
     'type': 'int',
     'table': 'int',
     "itarable": False,
     'divide': False,
     'if_change': True,
     'alarms': [{"bit": s, "text": str(a['name']) + " - " + str(i['name']) + " - " + str(i["hint"]), "type": a['type']} for s, a in
                enumerate(text_alarm)]
     } for k, i in enumerate(list_data) if i['itarable']]

list_data_not_speed_s300 = list_data_not_speed_s300_low_limits_warn + list_data_not_speed_s300_hight_limits_warn + list_data_not_speed_s300_low_limits_error + list_data_not_speed_s300_hight_limits_error + alarm_world + alarm_all_world

status_oee = [
    {"value": 7, 'type': 2, "text": "авария", "factor": 7},
    {"value": 6, 'type': 2, "text": "авария", "factor": 7},
    {"value": 4, 'type': 2, "text": "авария", "factor": 7},
    {"value": 0, 'type': 0, "text": "простой", "factor": 24},
    {"value": 24, 'type': 1, "text": "работа", "factor": 24},
    {"value": 8, 'type': 1, "text": "работа", "factor": 24},
]

oee = [
    {"start": 5830, 'name': 'Машина 1', 'table_name': 'machine1', "end": 5831, "status": status_oee},
    {"start": 5836, 'name': 'Машина 2', 'table_name': 'machine2', "end": 5837, "status": status_oee},
    {"start": 5842, 'name': 'Машина 3', 'table_name': 'machine3', "end": 5843, "status": status_oee},
    {"start": 5848, 'name': 'Машина 4', 'table_name': 'machine4', "end": 5849, "status": status_oee},
]
list_connections = [
    {
        "name": "connect1",
        "ip": '192.168.32.128',
        # "ip":'185.6.25.155',
        "rack": 0,
        "slot": 2,
        'DB': 500,
        # 'DB':81,
        "start": 0,
        "offset": 170,
        # "offset":44,
        "value_list": list_data
    },
    {
        "name": "s300_not_speed",
        "ip": '192.168.32.128',
        "rack": 0,
        "slot": 2,
        'DB': 3001,
        "start": 0,
        "offset": 5862,
        "value_list": list_data_not_speed_s300,
        'oee': oee
    },
    {
        "name": "plc1200_speed_data",
        "ip": '192.168.32.81',
        "rack": 0,
        "slot": 1,
        'DB': 14,
        "start": 0,
        "offset": 24,
        "value_list": list_data2
    }
]

statuses_connection = mp.Array('i', [0 for i in list_connections])

PLC_init = {
    "address": "192.168.32.128",
    "rack": 0,
    "slot": 2,
    "port": 102
}

result_query = {}
