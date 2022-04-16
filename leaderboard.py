from flask import Flask, request, jsonify
import mysql.connector
import random

app = Flask(__name__)

data = {}
required = ["game","name","score"]

def connect():
    dataBase = mysql.connector.connect(
      host ="assertjustice.mysql.pythonanywhere-services.com",
      user ="assertjustice",
      passwd ="REDACTED ;)",
      database = "assertjustice$leaderboard"
    )
    # preparing a cursor object
    cursorObject = dataBase.cursor()
    return dataBase, cursorObject

def execute(query, values = None):
    dataBase, cursorObject = connect()
    if not values:
        cursorObject.execute(query)
    else:
        cursorObject.execute(query,values)
    dataBase.close()

def fetch(query):
    dataBase, cursorObject = connect()
    cursorObject.execute(query)
    result = cursorObject.fetchall()
    dataBase.close()
    return result

def format_entry(result):
    id, game, name, score = result
    return {"id": id, "game": game, "name": name, "score": score} 

@app.route("/", methods=["GET"])
def list_data():
    game = request.args.get("game", default=None)
    query = "SELECT * FROM ENTRIES"
    if game:
        query = f"""SELECT * FROM ENTRIES WHERE GAME = '{game}' ORDER BY SCORE;
        """
    result = fetch(query)
    items = [format_entry(entry) for entry in result]
    return jsonify(items)

@app.route("/", methods=["POST"])
def create():
    if not request.is_json:
        return "Request was not json", 400
    req = request.get_json()
    for r in required:
        if r not in req:
            return f"Request body is missing the field {r}", 400
    query = "INSERT INTO ENTRIES (GAME, NAME, SCORE) VALUES (%s, %s, %s) SELECT * FROM ENTRIES"
    values = (req["game"], req["name"], req["score"])
    res = execute(query, values)
    return jsonify(res)

@app.route("/", methods=["DELETE"])
def delete():
    id = request.args.get("id", default=None)
    if not id:
        return "Request query has no id.", 400
    item = fetch(f"SELECT * FROM ENTRIES WHERE ID = '{id}'")
    if len(item) == 0:
        return f"Id {id} does not exist.", 400
    item = format_entry(item[0])
    query = f"DELETE FROM ENTRIES WHERE ID = '{id}'"
    execute(query)
    return jsonify(item)