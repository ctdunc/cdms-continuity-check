from flask import Flask, render_template, json, request, jsonify, Response, url_for
from celery import Celery
import time
from sql_helper.sql_interface import *
from continuity_check.continuity import perform_check

# Initialize App
app = Flask(__name__, static_folder="../static/dist", template_folder="../static/")

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Celery Workers
@celery.task(bind=True)
def continuity_check(self):
    rang = 100
    for i in range(rang):
        choice = random.random()
        self.update_state(state='PROGRESS',
                meta={'current':i, 'total':rang,
                    'status': choice})
        time.sleep(1)
        i=i+1
    return{'current': rang, 'total': rang, 'result': 'yeet'}

       

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

@app.route('/taskstatus',methods=['POST'])
def continuitycheck():
    task=continuity_check.apply_async()
    return jsonify({}),202,{'Location': url_for('taskstatus',task_id=task.id)}

@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = continuity_check.AsyncResult(task_id)
    print(task.info);
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response) 
if __name__ == "__main__":
    app.run()
