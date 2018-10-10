from flask import Flask, render_template, json, request, jsonify
from flaskext.mysql import MySQL
from sql_helper.sql_interface import *
app = Flask(__name__, static_folder="../static/dist",template_folder="../static")

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'cdms'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cdms'
app.config['MYSQL_DATABASE_DB']='CDMSTest'
app.config['MYSQL_DATABASE_HOST']='localhost'
mysql.init_app(app)

@app.route("/")
def index():
        return render_template("index.html")

@app.route("/run/<run>",methods=['GET'])
def getData(run):
    data = get_check(run)
    return jsonify(data)

# TODO: move this over to the sql_helper class
@app.route("/runHistory", methods=['GET'])
def getRuns():
  data = get_runs()
  return jsonify(data)

if __name__ == "__main__":
    app.run()


