#!/usr/bin/env python

import flask, time
from flask_bootstrap import Bootstrap
from solenoids import Actuate

def test():
    return time.ctime()

app = flask.Flask(__name__)
Bootstrap(app)
act = Actuate()

@app.route('/')
def index():
    now = test()
    return flask.render_template('index.html', now=now)

@app.route('/update', methods=['POST'])
def update():
    return flask.redirect('/')

@app.route('/water', methods=['POST'])
def water():
    act.test()
    return flask.redirect('/')

if __name__ == '__main__':
    app.run('192.168.1.7','5000',debug=True)
