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