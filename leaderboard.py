from flask import Flask, request, jsonify

app = Flask(__name__)

data = {}

leaderboard = [
    {"name":"AAG", "score":40},
    {"name":"AAF", "score":30},
    {"name":"AAE", "score":20},
    {"name":"AAD", "score":20},
    {"name":"AAC", "score":10},
    {"name":"AAB", "score":0}
]
for item in leaderboard:
    item["game"] = "swingwing"
    item["id"] = len(data)
    data[len(data)] = item

@app.route("/", methods=["GET"])
def list():
    game = request.args.get("game", default=None)
    if game:
        items = (item for item in data.values() if item["game"] == game)
        items = sorted(items, key=lambda item: item["score"], reverse=True)
    else:
        items = (item for item in data.values)
    return jsonify(items)

@app.route("/", methods=["POST"])
def create():
    if not request.is_json:
        return "Request was not json", 400
    req = request.get_json()
    id = len(data)
    req["id"] = id
    data[id] = req
    return jsonify(req)

if __name__ == "__main__":
    app.run()