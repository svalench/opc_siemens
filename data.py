import multiprocessing as mp

list_data = [
    {"name": "p1101", "start": 0, "type": "int"},
    {"name": "p1201", "start": 2, "type": "int"},
    {"name": "p1202", "start": 4, "type": "int"},
    {"name": "p1301", "start": 6, "type": "int"},
    {"name": "p1302", "start": 8, "type": "int"},
    {"name": "p1401", "start": 10, "type": "int"},
    {"name": "p1402", "start": 12, "type": "int"},
    {"name": "p1501", "start": 14, "type": "int"},
    {"name": "p1502", "start": 16, "type": "int"},

    {"name": "p1601", "start": 18, "type": "int"},
    {"name": "p1701", "start": 20, "type": "int"},
    {"name": "p1801", "start": 22, "type": "int"},
    {"name": "p1901", "start": 24, "type": "int"},
    {"name": "pdcah1103", "start": 26, "type": "int"},
    {"name": "pdcah1104", "start": 28, "type": "int"},
    {"name": "pdcah1601", "start": 30, "type": "int"},
    {"name": "pdcah1701", "start": 32, "type": "int"},
    {"name": "pdcah1801", "start": 34, "type": "int"},
    {"name": "pdcah1901", "start": 36, "type": "int"},
    {"name": "pw1600", "start": 38, "type": "int"},
    {"name": "pw1700", "start": 40, "type": "int"},
    {"name": "pw1800", "start": 42, "type": "int"},
    {"name": "pw1900", "start": 44, "type": "int"},
    {"name": "pzal1201", "start": 46, "type": "int"},
    {"name": "pzal1301", "start": 48, "type": "int"},
    {"name": "pzal1401", "start": 50, "type": "int"},
    {"name": "co2_1101", "start": 52, "type": "int"},
    {"name": "qziah_o2_1101", "start": 54, "type": "int"},
    {"name": "qzial_ch4_1101", "start": 56, "type": "int"},
    {"name": "T1501", "start": 58, "type": "int"},
    {"name": "T1601", "start": 60, "type": "int"},
    {"name": "T1701", "start": 62, "type": "int"},
    {"name": "T1801", "start": 64, "type": "int"},
    {"name": "T1901", "start": 66, "type": "int"},
    {"name": "TK1901", "start": 68, "type": "int"},
    {"name": "tshl1101", "start": 70, "type": "int"},
    {"name": "tzah1101", "start": 72, "type": "int"},
    {"name": "tzah1201", "start": 74, "type": "int"},
    {"name": "tzah1202", "start": 76, "type": "int"},
    {"name": "tzah1301", "start": 78, "type": "int"},
    {"name": "tzah1302", "start": 80, "type": "int"},
    {"name": "tzah1401", "start": 82, "type": "int"},
    {"name": "tzah1402", "start": 84, "type": "int"},
    {"name": "tzah1403", "start": 86, "type": "int"},
    {"name": "tzah1601", "start": 88, "type": "int"},
    {"name": "tzah1701", "start": 90, "type": "int"},
    {"name": "tzah1801", "start": 92, "type": "int"},
    {"name": "d601_ch4_gpa1", "start": 94, "type": "int"},
    {"name": "d602_ch4_gpa2", "start": 96, "type": "int"},
    {"name": "d603_ch4_gpa3", "start": 98, "type": "int"},
    {"name": "d604_ch4_gpa4", "start": 100, "type": "int"},
    {"name": "d601_la_gpa1", "start": 102, "type": "int"},
    {"name": "d602_la_gpa2", "start": 104, "type": "int"},
    {"name": "d603_la_gpa3", "start": 106, "type": "int"},
    {"name": "d604_la_gpa4", "start": 108, "type": "int"},
]

list_data1 = [
    {"name": "iso1", "start": 0, "type": "double"},
    {"name": "pol1", "start": 36, "type": "double"},
    {"name": "pol2", "start": 40, "type": "double"}
]

list_data2 = [
    {"name": "vibro1", "start": 0, "type": "int"},
    {"name": "vibro2", "start": 2, "type": "int"},
    {"name": "vibro3", "start": 4, "type": "int"},
    {"name": "vibro4", "start": 6, "type": "int"},
    {"name": "vibro5", "start": 8, "type": "int"},
    {"name": "vibro6", "start": 10, "type": "int"},
    {"name": "temp1", "start": 12, "type": "int"},
    {"name": "temp2", "start": 14, "type": "int"},
    {"name": "temp3", "start": 16, "type": "int"},
    {"name": "temp4", "start": 18, "type": "int"},
    {"name": "temp5", "start": 20, "type": "int"},
    {"name": "temp6", "start": 22, "type": "int"},
]

list_connections = [
    {
        "name": "connect1",
        "ip": '192.168.32.128',
        #"ip":'185.6.25.155',
        "rack": 0,
        "slot": 2,
        'DB': 500,
        #'DB':81,
        "start": 0,
        "offset": 168,
        #"offset":44,
        "value_list": list_data
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