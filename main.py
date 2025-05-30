import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
from dotenv import load_dotenv
from google_manager import update_spese
from settings import get_settings, saveSettings

load_dotenv()

app = Flask(__name__)
CORS(app)

USER_PASSWORD = os.environ.get("USER_PASSWORD")

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if token != USER_PASSWORD:
            return jsonify({"status": "unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/ping', methods=['GET'])
@require_auth
def ping():
    try:
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route("/auth", methods=["POST"])
@require_auth
def auth():
    return jsonify({"status": "ok"})

@app.route("/sync", methods=["POST"])
@require_auth
def sync():
    try:
        dati = request.get_json()
        spese = dati.get("spese", [])
        update_spese(spese)
        return jsonify({"status": "ok"})
    except Exception as e:
        print("Errore durante la sincronizzazione:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/settings", methods=["GET"])
@require_auth
def settings():
    try:
        settings_data = get_settings()
        return jsonify(settings_data), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route("/saveSettings", methods=["POST"])
@require_auth
def saveSettings():
    try:
        settings = request.get_json()
        saveSettings(settings)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)
