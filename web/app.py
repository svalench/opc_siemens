from cprint import cprint
from flask import Flask, render_template

app = Flask('opc', static_url_path='', static_folder='web/static', template_folder='web/template')
connections = None

@app.route('/')
def index():
    cprint.err("----------------THIS IS STATUSES----------")
    for i in connections:
        print(i)
    return render_template('index.html')






def run_flask(status):
    """ run flask in other thread
    :return:
    """
    globals()['connections'] = status
    app.run(host='0.0.0.0')