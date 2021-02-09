import json
import multiprocessing
import socket
import threading
import time
from typing import Optional

from cprint import cprint

from core.processor import StartProcessOpcForConnectToPLC
from core import models

import multiprocessing as mp

from settings import SOCKET_PORT

models.Base.metadata.create_all(bind=models.engine)

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
        "name":"connect1",
        "ip":'192.168.32.128',
        #"ip":'185.6.25.155',
        "rack":0,
        "slot":2,
        'DB':3001,
        #'DB':81,
        "start":0,
        "offset":180,
        #"offset":44,
        "value_list": list_data1
    }
]
pr = {}
statuses_connection = mp.Array('i', [0 for i in list_connections])

def main():
    count = 0
    for connection in list_connections:
        pr[connection['name']] = StartProcessOpcForConnectToPLC(
                                                                    connection['ip'],
                                                                    connection['rack'],
                                                                    connection['slot'],
                                                                    connection['DB'],
                                                                    connection['start'],
                                                                    connection['offset'],
                                                                    values_list=connection['value_list'],
                                                                    name_connect=connection['name'],
                                                                    status = statuses_connection,
                                                                    count  = count
                                                                )
        count+=1
        pr[connection['name']].start()
        start_socket()
    while True:
        for p in pr:
            print(pr[p].is_alive(), 'process', p)
        for a in statuses_connection:
            print(a)
        time.sleep(1)







def start_socket():
    cprint.err('run socket ')
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = 'localhost'
        port = SOCKET_PORT
        conn.settimeout(0.01)
        conn.connect((host, port))
        conn.close()
        cprint.info("Socket isset")
    except:
        print("run socket server")
        my_thread = threading.Thread(target=listen_server_mvlab)
        my_thread.start()


def listen_server_mvlab():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', SOCKET_PORT))
        s.listen()
        cprint.warn('Listen localhost:%s'%SOCKET_PORT)
        conn, addr = s.accept()
        with conn:
            cprint.warn('Connected by %s'% str(addr))
            while True:
                try:
                    cprint.info('WIhlte cycle socket server')
                    data = conn.recv(1024)
                    if not data:
                        break
                    data = {}
                    count = 0
                    for i in list_connections:
                        data[i['name']] = [statuses_connection[count], i['name'], i['ip']]
                        count += 1
                    data = json.dumps(data).encode('utf-8')
                    cprint.warn('sended  %s' % data)
                    conn.send(data)
                    #conn.sendall()
                except:
                    conn.close()
    start_socket()






if __name__ == '__main__':
    main()

