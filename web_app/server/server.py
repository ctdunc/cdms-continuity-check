from flask import Flask, render_template, json, request, jsonify, Response, url_for
from flask_socketio import SocketIO
from celery import Celery
from requests import post
import functools

from sql_helper.sql_interface import *
from continuity_check.continuity import perform_check

import time
# Initialize App
app = Flask(__name__, static_folder="../static/dist", template_folder="../static/")

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


# configure socketio
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)



# Celery Workers
@celery.task(bind=True)
def continuity_check(self, url):
    iterator = perform_check()
    iterlen = functools.reduce(lambda acc, e: acc+1, iterator, 0)
    post(url, json={'key': 'TOTAL', 'value': iterlen})

    for i in perform_check():
        # Serialize i
        key = i.get('key')
        value= i.get('value')

       # Update task state
        meta={'key': key,
             'value': value
              }
        self.update_state(state='PROGRESS',
            meta=meta)

        post(url, json=meta)
        time.sleep(0.05)
    meta = {'key': 'COMPLETE',
            'value': 'COMPLETE!'
            }
    return True


# App routes
@app.route("/")
def index():
        return render_template("index.html")


@app.route("/continuity-history/<run>", methods=['GET'])
def getData(run):
    data = get_check(run)
    return jsonify(data)


@app.route("/continuity-history", methods=['GET'])
def getRuns():
    data = get_runs()
    return jsonify(data)

@app.route('/event/', methods=['POST'])
def event():
    data = request.json
    socketio.emit('checkUpdate',data)
    return '0'

@app.route('/continuitycheck',methods=['POST'])
def continuitycheck():
    task=continuity_check.delay(url_for('event',_external=True))
    socketio.emit('checkStarted', {'taskid': task.id})
    return 'started'    

if __name__ == "__main__":
    socketio.run(app,debug=True)
