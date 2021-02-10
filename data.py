import multiprocessing as mp

list_data = [
    {"name": "p1101", "start": 2, "type": "real"},
    {"name": "p1201", "start": 102, "type": "real"},
    # {"name": "p1202", "start": 202, "type": "real"},
    # {"name": "p1301", "start": 302, "type": "real"},
    # {"name": "p1302", "start": 402, "type": "real"},
    # {"name": "p1401", "start": 502, "type": "real"},
    # {"name": "p1402", "start": 602, "type": "real"},
    # {"name": "p1501", "start": 702, "type": "real"},
    # {"name": "p1502", "start": 802, "type": "real"},
]

list_data1 = [
    {"name": "iso1", "start": 0, "type": "double"},
    {"name": "pol1", "start": 36, "type": "double"},
    {"name": "pol2", "start": 40, "type": "double"}
]

list_connections = [
    {
        "name": "connect1",
        #"ip": '192.168.32.128',
        "ip":'185.6.25.155',
        "rack": 0,
        "slot": 2,
        #'DB': 3001,
        'DB':81,
        "start": 0,
        #"offset": 180,
        "offset":44,
        "value_list": list_data1
    }
]

statuses_connection = mp.Array('i', [0 for i in list_connections])