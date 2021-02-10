import json
import socket
import threading

from cprint import cprint

from data import list_connections, statuses_connection
from settings import SOCKET_PORT


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
        cprint.warn('Listen localhost:%s' % SOCKET_PORT)
        conn, addr = s.accept()
        with conn:
            cprint.warn('Connected by %s' % str(addr))
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
                    # conn.sendall()
                except:
                    conn.close()
    start_socket()