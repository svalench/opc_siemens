from flask import Flask, render_template

app = Flask('opc', static_url_path='', static_folder='web/static', template_folder='web/template')


@app.route('/')
def hello_world():
    return render_template('index.html')






def run_flask():
    """ run flask in other thread
    :return:
    """
    app.run(host='0.0.0.0')