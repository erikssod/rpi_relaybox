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
    return flask.render_template('index.html', 
            now=now,
            foo='foo',
            bar='bar',
            lst=[1,2,3,4,5,6])

@app.route('/update', methods=['POST'])
def update():
    return flask.redirect('/')

@app.route('/do_thing', methods=['POST'])
def do_thing():
    data = flask.request.form
    print(dir(data))
    a = data.to_dict()
    print(a['thing'])
    b = a['thing']
    act.test2(b)
    return flask.redirect('/')

@app.route('/water', methods=['POST'])
def water():
    act.test()
    return flask.redirect('/')

if __name__ == '__main__':
    app.run('10.1.1.105','5000',debug=True)
