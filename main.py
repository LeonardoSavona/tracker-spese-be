from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from functools import wraps

SECRET_PASSWORD = "DajeRoma777!"

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "API Spese attiva!"

# Decoratore per autenticazione
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            abort(401)  # Non autorizzato
        token = auth[7:]
        if token != SECRET_PASSWORD:
            abort(403)  # Accesso negato
        return f(*args, **kwargs)
    return decorated

@app.route("/auth", methods=["POST"])
@require_auth
def auth():
    return jsonify({"status": "ok"})

@app.route("/sync", methods=["POST"])
@require_auth
def sync():
    data = request.json
    # TODO: salva i dati su Google Sheet
    print("Dati ricevuti:", data)
    return jsonify({"status": "ok", "message": "Dati sincronizzati"})
