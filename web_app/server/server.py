from flask import Flask, render_template, json, request, jsonify, Response
from flask_socketio import SocketIO, emit
import numpy as np

from sql_helper.sql_interface import *
from continuity_check.continuity import perform_check

app = Flask(__name__, static_folder="../static/dist", template_folder="../static/")
app.config['SECRET_KEY'] = 'super-secret'
socketio=SocketIO(app)

@app.route("/")
def index():
        return render_template("index.html")


@app.route("/run/<run>", methods=['GET'])
def getData(run):
    data = get_check(run)
    return jsonify(data)


@app.route("/runHistory", methods=['GET'])
def getRuns():
    data = get_runs()

    return jsonify(data)

@socketio.on('startcheck')
def startCheck():
    def generate():
        data = perform_check(expected_table='slac_expected_values', 
                    institution='UC Berkeley')
        
        try:
            prev_data = next(data)
        except StopIteration:
            yield  '{"data": []}'
            raise StopIteration
        yield '{"data":['

        for d in data:
            yield json.dumps(str(prev_data)) + ','
            prev_data = d 
        
        yield json.dumps(str(prev_data))+ ']}'
    return Response(generate(), content_type='application/json')
         
if __name__ == "__main__":
    socketio.run(app)
