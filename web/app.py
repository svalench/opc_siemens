from cprint import cprint
from flask import Flask, render_template

from data import list_connections

app = Flask('opc', static_url_path='', static_folder='web/static', template_folder='web/template')
connections = []

@app.route('/')
def index():
    cprint.err("----------------THIS IS STATUSES----------")
    data = []
    for k,i in enumerate(list_connections):
        i['status_connection'] = connections[k]
        data.append(i)
    return render_template('index.html', data=data)






def run_flask(status):
    """ run flask in other thread
    :return:
    """
    globals()['connections'] = status
    app.run(host='0.0.0.0')