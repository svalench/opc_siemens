import json
import socket
import threading
import time
from unittest import TestCase
import multiprocessing as mp

from core.processor import StartProcessOpcForConnectToPLC
from core.socket_server import listen_server_mvlab


class TestSocetServerRun(TestCase):
    def setUp(self):
        time.sleep(5)
        self.my_thread = threading.Thread(target=listen_server_mvlab)
        self.my_thread.start()

    def test_send_socket(self):
        sock = socket.socket()
        time.sleep(1)

        sock.connect(('0.0.0.0', 8084))
        sock.send(b'{"test_socket":1}')
        data = sock.recv(1024)
        sock.close()
        time.sleep(1)
        data = json.loads(data)
        self.my_thread.join()
        self.assertEqual(data, "{'test':True}")

class TestStart100ProccessCase(TestCase):
    def test_start_10_process(self):
        pr = {}
        count = 0
        statuses_connection = mp.Array('i', [0 for i in range(10)])
        for i in range(10):
            pr[i] = StartProcessOpcForConnectToPLC(
                '192.168.1.1',
                0,
                0,
                0,
                0,
                10,
                values_list=[],
                name_connect="name"+str(i),
                status=statuses_connection,
                count=count
            )
            pr[i].start()
            count+=1
        status = True
        time.sleep(10)
        for p in pr:
            print(pr[p].is_alive())
            if not pr[p].is_alive():
                status = False
            pr[p].kill()
        self.assertEqual(status, True)


    def test_start_50_process(self):
        pr = {}
        count = 0
        statuses_connection = mp.Array('i', [0 for i in range(50)])
        for i in range(50):
            pr[i] = StartProcessOpcForConnectToPLC(
                '192.168.1.1',
                0,
                0,
                0,
                0,
                10,
                values_list=[],
                name_connect="name"+str(i),
                status=statuses_connection,
                count=count
            )
            pr[i].start()
            count+=1
        status = True
        time.sleep(10)
        for p in pr:
            print(pr[p].is_alive())
            if not pr[p].is_alive():
                status = False
            pr[p].kill()
        self.assertEqual(status, True)