from sqlalchemy.orm import sessionmaker
from web.app import Connections, ListValue, Alarms, Text_Alarm
from sqlalchemy import create_engine
engine = create_engine('sqlite:///test.db', echo=True)
Session = sessionmaker(bind=engine)


def get_list_connections():
    session = Session()
    value_list = []
    k = session.query(ListValue).all()
    for i in k:
        val = {
            "name": i.name,
            "start": i.start,
            "type": str(i.type_value),
            "table": str(i.type_table),
            "divide": i.divide,
            "if_change": i.if_change,
            "byte_bind": i.byte_bind,
            "bit_bind": i.bit_bind
        }
        value_list.append(val)
    list_connections = []
    k = session.query(Connections).all()
    for i in k:
        connect = {
            "name": i.name,
            "ip": i.ip,
            "rack": i.rack,
            "slot": i.slot,
            "DB": i.DB,
            "start": i.start,
            "offset": i.offset,
            "value_list": value_list
        }
        list_connections.append(connect)
    return list_connections


def get_alarm_all_world():
    session = Session()
    c = session.query(ListValue).all()
    alarm_world = []
    for i in c:
        alarm = []
        if i.alarms_id != "Null":
            a = session.query(Alarms).get(i.alarms_id)
            b = session.query(Text_Alarm).get(a.text_alarm_id)
            al = {
                "bit": a.bit,
                "text": b.name + '-' + i.name,
                "type": b.type
            }
            alarm.append(al)
            k = {
                "name": 'alarm_world_%s' % i.name,
                "start": i.start,
                "type": str(i.type_value),
                "table": str(i.type_table),
                "divide": i.divide,
                "if_change": i.if_change,
                "alarms": alarm
            }
            alarm_world.append(k)
        else:
            k = {
                "name": 'alarm_world_%s' % i.name,
                "start": i.start,
                "type": str(i.type_value),
                "table": str(i.type_table),
                "divide": i.divide,
                "if_change": i.if_change
            }
            alarm_world.append(k)
    return alarm_world
