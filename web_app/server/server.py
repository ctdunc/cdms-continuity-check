from flask import Flask, render_template
import sqlite3 as sql 
app = Flask(__name__, static_folder="../static/dist",template_folder="../static")


@app.route("/")
def index():
        return render_template("index.html")

@app.route("/expected_result")
def expected_result():
    connection = sql.connect("expected_result.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM continuity_prediction")
    result = cursor.fetchall()
    return str(result)


if __name__ == "__main__":
    app.run()


