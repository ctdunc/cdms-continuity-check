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
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute('SELECT Date, Institution, VIB, Wiring, Device, Temperature, Validator, Check_name FROM RunHistory')
        data = cursor.fetchall()
        return jsonify(data)
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run()


