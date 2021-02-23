import gzip
import json
import math
import socket
import threading
import time

from cprint import cprint

from core.teldafax_dashboard_data import PlcRemoteUse
from data import list_connections, statuses_connection, PLC_init, result_query
from settings import SOCKET_PORT


def start_socket():
    cprint.err('run socket ')
    get_dat_from_plc_thread = threading.Thread(target=get_data_from_plc)
    get_dat_from_plc_thread.start()
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '0.0.0.0'
        port = SOCKET_PORT
        conn.settimeout(1)
        conn.connect((host, port))
        conn.close()
        cprint.info("Socket isset")
    except:
        print("run socket server")
        my_thread = threading.Thread(target=listen_server_mvlab)
        my_thread.start()


def get_data_from_plc():
    while True:
        time.sleep(2)
        try:
            data = PlcRemoteUse(PLC_init["address"], PLC_init["rack"], PLC_init["slot"], PLC_init["port"])
            data1 = data.get_dashboard_teldafax_value_power()
            data2 = data.get_status_machine()
            data = {"data1": data1, "data2": data2}
            globals()['result_query'] = data
            # return data
        except:
            globals()['result_query'] = [{"error": 0}]
            # return json.dumps({"error": "no connection"}).encode('utf-8')


def listen_server_mvlab():
    while True:
        cprint.info("Try to start xocket server")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('0.0.0.0', SOCKET_PORT))
            s.listen()
            cprint.warn('Listen 0.0.0.0:%s' % SOCKET_PORT)
        except:
            time.sleep(5)
            continue
        while True:
            try:
                conn, addr = s.accept()
                while True:
                    try:
                        data = conn.recv(1024)
                        print(data)
                        if not data:
                            break
                        try:
                            data = json.loads(data)
                            print(data)
                        except:
                            cprint.err("string not json")
                            data = json.dumps("{'error':'string not json'}").encode('utf-8')
                            conn.send(data)

                        if "dash_teldafax" in data:
                            data = json.dumps(result_query).encode('utf-8')
                            cprint.warn('sended  %s' % data)
                            conn.send(data)
                        elif "get_connections" in data:
                            data = json.dumps(list_connections).encode('utf-8')
                            col_string = math.ceil(len(data) / 1024)
                            col_string += 1
                            conn.send(json.dumps({"col_string": col_string}).encode('utf-8'))
                            for i in range(col_string):
                                start = i * 1024
                                end = (i + 1) * 1024
                                conn.send(data[start:end])
                                print(data[start:end])

                            conn.close()
                        else:
                            data = {}
                            count = 0
                            for i in list_connections:
                                data[i['name']] = [statuses_connection[count], i['name'], i['ip']]
                                count += 1
                            print(data)
                            data = json.dumps(data).encode('utf-8')
                            cprint.warn('sended  %s' % data)
                            conn.send(data)
                    except Exception as e:
                        cprint.info(e)
                        break
            except:
                s.close()
                break
