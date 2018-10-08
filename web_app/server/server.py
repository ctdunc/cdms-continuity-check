from flask import Flask, render_template, json, request, jsonify
from flaskext.mysql import MySQL
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

@app.route("/expectedData",methods=['GET'])
def getData():
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute('SELECT Date, Institution, VIB, Wiring, Device, Temperature, Validator, FROM RunHistory')
        data = cursor.fetchall()
        return jsonify(data)
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        conn.close()

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


