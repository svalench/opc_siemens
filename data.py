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
    }
]

statuses_connection = mp.Array('i', [0 for i in list_connections])