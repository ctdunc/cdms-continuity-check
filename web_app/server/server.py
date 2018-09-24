from flask import Flask, render_template, json
from flaskext.mysql import MySQL
app = Flask(__name__, static_folder="../static/dist",template_folder="../static")

mysql = MySQL()
app.config['MSYQL_DATABASE_USER'] = 'cmds'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cdms'
app.config['MYSQL_DATABASE_DB']='CDMSTest'
app.config['MYSQL_DATABASE_HOST']='localhost'
mysql.init_app(app)

@app.route("/")
def index():
        return render_template("index.html")

@app.route("/expectedData")
def getData():
    try:
        conn=msyql.connect()
        cursor=conn.cursor()
        data = cursor.fetchall()
        return data
    except Exeception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()
if __name__ == "__main__":
    app.run()


