from flask import Flask, request, jsonify, abort

SECRET_PASSWORD = "DajeRoma777!"

app = Flask(__name__)

@app.route("/")
def home():
    return "API Spese attiva!"

@app.route("/sync", methods=["POST"])
def sync():
    data = request.json
    # TODO: salva i dati su Google Sheet
    print("Dati ricevuti:", data)
    return jsonify({"status": "ok", "message": "Dati sincronizzati"})

@app.route("/auth", methods=["POST"])
def auth():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        abort(401)
    token = auth[7:]
    if token != SECRET_PASSWORD:
        abort(403)
    return jsonify({"status": "ok"})
