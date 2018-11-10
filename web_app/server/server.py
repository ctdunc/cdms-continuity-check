from flask import Flask, render_template, json, request, jsonify, Response
from sql_helper.sql_interface import *
from continuity_check.continuity import *
app = Flask(__name__, static_folder="../static/dist",template_folder="../static")


@app.route("/")
def index():
        return render_template("index.html")

@app.route("/run/<run>",methods=['GET'])
def getData(run):
    data = get_check(run)
    return jsonify(data)

@app.route("/runHistory", methods=['GET'])
def getRuns():
  data = get_runs()
  return jsonify(data)

@app.route("/startcheck")
def respond():
    def startcheck():
        for i in perform_check():
            yield "i:".join(str(i))+"!"
    return Response(startcheck())
if __name__ == "__main__":
    app.run()


