
import time
from typing import Optional

from cprint import cprint

from core.processor import StartProcessOpcForConnectToPLC
from core import models
from core.socket_server import start_socket
from data import list_connections, statuses_connection

models.Base.metadata.create_all(bind=models.engine)


pr = {}
data_for_restart = {}



def main():
    count = 0
    for connection in list_connections:
        try:
            time.sleep(3)
            pr[connection['name']] = StartProcessOpcForConnectToPLC(
                connection['ip'],
                connection['rack'],
                connection['slot'],
                connection['DB'],
                connection['start'],
                connection['offset'],
                values_list=connection['value_list'],
                name_connect=connection['name'],
                status=statuses_connection,
                count=count
            )
            data_for_restart[connection['name']] = {
                                                        "ip":connection['ip'],
                                                        "rack":connection['rack'],
                                                        "slot":connection['slot'],
                                                        "DB":connection['DB'],
                                                        "start":connection['start'],
                                                        "offset":connection['offset'],
                                                        'values_list':connection['value_list'],
                                                        'count':count
                                                    }
            count += 1
            pr[connection['name']].start()
        except:
            cprint.err('Not start process %s' % connection['name'])
    start_socket()
    while True:
        for p in pr:
            restart_process_if_not_alive(p)
            print(pr[p].is_alive(), 'process', p)
        for a in statuses_connection:
            print(a)
        time.sleep(1)


def restart_process_if_not_alive(p):
    if (not pr[p].is_alive()):
        cprint.err("restart process %s" % p)
        pr[p].kill()
        pr[p] = StartProcessOpcForConnectToPLC(
            data_for_restart[p]['ip'],
            data_for_restart[p]['rack'],
            data_for_restart[p]['slot'],
            data_for_restart[p]['DB'],
            data_for_restart[p]['start'],
            data_for_restart[p]['offset'],
            values_list=data_for_restart[p]['value_list'],
            name_connect=data_for_restart[p]['name'],
            status=statuses_connection,
            count=data_for_restart[p]['count']
        )






if __name__ == '__main__':
    main()
