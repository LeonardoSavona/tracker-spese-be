from flask import Flask, request, jsonify
import os

app = Flask(__name__)

SECRET_TOKEN = os.environ.get("SECRET_TOKEN", "dev-token")

@app.route("/")
def home():
    return "API Spese attiva!"

@app.route("/sync", methods=["POST"])
def sync():
    token = request.headers.get("Authorization")
    if token != f"Bearer {SECRET_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    # TODO: salva i dati su Google Sheet
    print("Dati ricevuti:", data)
    return jsonify({"status": "ok", "message": "Dati sincronizzati"})
