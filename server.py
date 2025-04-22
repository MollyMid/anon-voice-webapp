from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

waiting_users = []

@app.route("/")
def home():
    return jsonify({"status": "API работает"})

@app.route("/join", methods=["POST"])
def join():
    data = request.json
    tg_id = data["tg_id"]
    peer_id = data["peer_id"]

    # Если кто-то уже в очереди — соединяем
    if waiting_users:
        partner = waiting_users.pop(0)
        return jsonify({
            "status": "matched",
            "partner_peer_id": partner["peer_id"],
            "partner_tg_id": partner["tg_id"]
        })

    # Иначе добавляем в очередь
    waiting_users.append({"tg_id": tg_id, "peer_id": peer_id})
    return jsonify({"status": "waiting"})


@app.route("/leave", methods=["POST"])
def leave():
    data = request.json
    tg_id = data["tg_id"]
    global waiting_users
    waiting_users = [u for u in waiting_users if u["tg_id"] != tg_id]
    return jsonify({"status": "left"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
