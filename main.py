import time
from typing import Optional

from core.processor import StartProcessOpcForConnectToPLC
from core import models

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


def main():
    pr = StartProcessOpcForConnectToPLC('192.168.32.128', 0, 2, 3001, 0, 130,values_list=list_data)
    pr.start()
    while True:
        print(pr.is_alive(), 'process')
        time.sleep(1)


if __name__ == '__main__':
    main()
