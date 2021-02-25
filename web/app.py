from cprint import cprint
from flask import Flask, render_template, request, redirect, url_for

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy_utils.types.choice import ChoiceType

from data import list_connections

engine = create_engine('sqlite:///test.db', echo=True)
base = declarative_base()


class Connections(base):
    __tablename__ = 'connections'
    id = Column(Integer(), primary_key=True)
    name = Column(String(128), nullable=False)
    ip = Column(String(128), nullable=False)
    rack = Column(Integer, nullable=False)
    slot = Column(Integer, nullable=False)
    DB = Column(Integer, nullable=False)
    start = Column(Integer, nullable=False)
    offset = Column(Integer, nullable=False)


class ListValue(base):
    TYPES = [
        ('int', 'int'),
        ('real', 'float'),
        ('bool', 'bool'),
        ('double', 'double')
    ]

    __tablename__ = 'listvalue'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    offset = Column(Integer, nullable=False)
    type_value = Column(ChoiceType(TYPES))
    type_table = Column(ChoiceType(TYPES))
    connections_id = Column(Integer, ForeignKey('connections.id'))
    # connections = relationship(Connections, cascade="all,delete", backref="value")
    divide = Column(Boolean, default=False)
    if_change = Column(Boolean, default=False)
    byte_bind = Column(Integer, nullable=False)
    bit_bind = Column(Integer, nullable=False)
    alarms_id = Column(Integer, ForeignKey('alarms.id'))


class Alarms(base):
    __tablename__ = 'alarms'

    id = Column(Integer, primary_key=True)
    bit = Column(Integer, nullable=False)
    text_alarm_id = Column(Integer, ForeignKey('text_alarm.id'))


class Text_Alarm(base):
    __tablename__ = 'text_alarm'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)


base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

app = Flask('opc', static_url_path='', static_folder='web/static', template_folder='web/template')
connections = []


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/alarm_text')
def alarm_text():
    session = Session()
    data = session.query(Text_Alarm).all()
    return render_template('alarem_text_list.html', data=data)


@app.route('/alarm_text/add_alarm_text', methods=['GET'])
def add_alarm_text_form():
    return render_template('add_alarm_text.html')


@app.route('/alarm_text/add_alarm_text', methods=['POST'])
def add_alarm_text():
    name = request.form['name']
    type = request.form['type']
    a = Text_Alarm(name=name, type=type)
    session = Session()
    session.add(a)
    session.commit()
    return redirect(url_for('alarm_text'))


@app.route('/alarm_text/del', methods=['POST'])
def alarm_text_del():
    id = request.form['del']
    session = Session()
    a = session.query(Text_Alarm).get(id)
    session.delete(a)
    session.commit()
    return redirect(url_for('alarm_text'))


@app.route('/alarm_text/up/<int:id_alarm_text>', methods=['GET'])
def up_alarm_text_form(id_alarm_text):
    session = Session()
    data = session.query(Text_Alarm).get(id_alarm_text)
    return render_template('up_alarm_text.html', alarm_text_get=data)


@app.route('/alarm_text/up/<int:id_alarm_text>', methods=['POST'])
def up_alarm_text(id_alarm_text):
    name = request.form['name']
    type = request.form['type']
    session = Session()
    a = session.query(Text_Alarm).get(id_alarm_text)
    a.name = name
    a.type = type
    session.commit()
    return redirect(url_for('alarm_text'))


@app.route('/connections')
def index():
    session = Session()
    data = session.query(Connections).all()
    return render_template('connections_list.html', data=data)


@app.route('/add_con', methods=['GET'])
def con():
    return render_template('conn.html')


@app.route('/add_con', methods=['POST'])
def add_connections():
    name = request.form['name']
    ip = request.form['ip']
    rack = request.form['rack']
    slot = request.form['slot']
    DB = request.form['DB']
    start = request.form['start']
    offset = request.form['offset']

    a = Connections(name=name, ip=ip, rack=rack, slot=slot, DB=DB, start=start, offset=offset)
    session = Session()
    session.add(a)
    session.commit()
    return redirect(url_for('index'))


@app.route('/updata_con/<int:id>', methods=['GET'])
def up_con(id):
    session = Session()
    data = session.query(Connections).get(id)
    return render_template('up_con.html', data=data)


@app.route('/updata_con', methods=['POST'])
def updata_connections():
    id = request.form['id']
    name = request.form['name']
    ip = request.form['ip']
    rack = request.form['rack']
    slot = request.form['slot']
    DB = request.form['DB']
    start = request.form['start']
    offset = request.form['offset']
    session = Session()
    a = session.query(Connections).get(id)
    a.name = name
    a.ip = ip
    a.rack = rack
    a.slot = slot
    a.DB = DB
    a.start = start
    a.offset = offset
    session.commit()
    return redirect(url_for('index'))


@app.route('/del_con', methods=['POST'])
def del_connections():
    id = request.form['id']
    session = Session()
    b = session.query(ListValue).filter_by(connections_id=id)
    for i in b:
        session.delete(i)
        session.commit()
    a = session.query(Connections).get(id)
    session.delete(a)
    session.commit()
    return redirect(url_for('index'))


@app.route('/value_list/<int:id>', methods=['GET'])
def value_list(id):
    session = Session()
    a = session.query(ListValue).filter_by(connections_id=id)
    b = session.query(Connections).get(id).name
    data = {
        "data": a,
        "id": id,
        "name": b
    }
    return render_template('value_list.html', data=data)


@app.route('/value_list/<int:id>/add_value_list', methods=['GET'])
def add_value_list(id):
    return render_template('add_value_list.html', data=id)


@app.route('/value_list/<int:id>/add_value_list', methods=['POST'])
def add_value(id):
    name = request.form['name']
    offset = request.form['offset']
    type_value = request.form['type_value']
    type_table = request.form['type_table']

    if request.form['divide'] == 'True':
        divide = 1
    else:
        divide = 0
    if request.form['if_change'] == 'True':
        if_change = 1
    else:
        if_change = 0
    byte_bind = request.form['byte_bind']
    bit_bind = request.form['bit_bind']
    a = ListValue(name=name,
                  offset=offset,
                  type_value=type_value,
                  type_table=type_table,
                  connections_id=id,
                  divide=divide,
                  if_change=if_change,
                  byte_bind=byte_bind,
                  bit_bind=bit_bind
                  )
    session = Session()
    session.add(a)
    session.commit()
    return redirect(url_for('value_list', id=id))


@app.route('/value_list/<int:id>/del', methods=['POST'])
def del_value(id):
    id1 = request.form['id_val']
    session = Session()
    a = session.query(ListValue).get(id1)
    session.delete(a)
    session.commit()
    return redirect(url_for('value_list', id=id))


@app.route('/value_list/up/<int:id1>/<int:id2>', methods=['GET'])
def up_value(id1, id2):
    session = Session()
    a = session.query(ListValue).get(id2)
    data = {
        "a": a,
        "id1": id1,
        "int": "int",
        "real": "real",
        "bool": "bool",
        "double": "double"
    }
    return render_template('up_value.html', data=data)


@app.route('/value_list/up/<int:id1>/<int:id2>', methods=['POST'])
def up_value_ch(id1, id2):
    session = Session()
    a = session.query(ListValue).get(id2)
    name = request.form['name']
    offset = request.form['offset']
    type_value = request.form['type_value']
    type_table = request.form['type_table']
    if request.form['divide'] == "True":
        divide = True
    else:
        divide = False
    if request.form['if_change'] == "True":
        if_change = True
    else:
        if_change = False
    byte_bind = request.form['byte_bind']
    bit_bind = request.form['bit_bind']
    a.name = name
    a.offset = offset
    a.type_value = type_value
    a.type_table = type_table
    a.connections_id = id1
    a.divide = divide
    a.if_change = if_change
    a.byte_bind = byte_bind
    a.bit_bind = bit_bind
    session.commit()
    return redirect(url_for('value_list', id=id1))

@app.route('/alarm_text/<int:id_alarm_text>/alarm', methods=['GET'])
def alarm_list(id_alarm_text):
    session = Session()
    a = session.query(Alarms).filter_by(text_alarm_id=id_alarm_text)
    b = session.query(Text_Alarm).get(id_alarm_text)
    data = {
        "id_alarm_text": id_alarm_text,
        "array_alarms": a,
        "text": b.name,
        "type": b.type
    }
    return render_template('alarm_list.html', data=data)


def run_flask(status):
    """ run flask in other thread
    :return:
    """
    globals()['connections'] = status
    app.run(host='0.0.0.0', port=5001)
