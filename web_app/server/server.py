from flask import Flask, render_template, json, request, jsonify, Response, url_for
from flask_socketio import SocketIO
from celery import Celery
import numpy as np

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
def continuity_check(self):
    for i in perform_check():
        # Serialize i
        key = i.get('key')
        value= i.get('value')
        # Update task state
        self.update_state(state='PROGRESS',
                meta={'key': key,
                    'value': value
                     })
        # Change to socket.emit event

@socketio.on('hello')
def handleHello():
    print('jello')

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

@app.route('/continuitycheck',methods=['POST'])
def continuitycheck():
    task=continuity_check.apply_async()
    return jsonify({}),202,{'Location': url_for('taskstatus',task_id=task.id)}

@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = continuity_check.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'key': '',
            'value': '',
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        print(task.info)
        response = {
            'state': task.state,
            'key': task.info.get('key'),
            'value': task.info.get('value'),
            'status': 'Check in progress...'
        }
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'key': 1,
            'value': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response) 

if __name__ == "__main__":
    socketio.run(app,debug=True)
