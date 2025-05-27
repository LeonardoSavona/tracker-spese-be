import os
import json
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# Carica le variabili da .env se non sono già nel sistema
load_dotenv()

app = Flask(__name__)
CORS(app)

# Password per autenticazione semplice
USER_PASSWORD = os.environ.get("USER_PASSWORD")

# ID del Google Sheets
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")

# Funzione per ottenere il client gspread
def get_gspread_client():
    base64_creds = os.environ.get("GOOGLE_CREDENTIALS")
    if not base64_creds:
        raise ValueError("Variabile GOOGLE_CREDENTIALS non trovata")

    json_creds = base64.b64decode(base64_creds).decode("utf-8")
    creds_dict = json.loads(json_creds)

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

# Endpoint di autenticazione
@app.route("/auth", methods=["POST"])
def auth():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if token == USER_PASSWORD:
        return jsonify({"status": "ok"})
    return jsonify({"status": "unauthorized"}), 401

# Endpoint di sincronizzazione
@app.route("/sync", methods=["POST"])
def sync():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if token != USER_PASSWORD:
        return jsonify({"status": "unauthorized"}), 401

    dati = request.get_json()
    spese = dati.get("spese", [])

    try:
        gc = get_gspread_client()
        sh = gc.open_by_key(SPREADSHEET_ID)

        # Scrivi foglio "SPESE"
        ws_spese = sh.worksheet("SPESE")
        ws_spese.clear()
        ws_spese.append_row(["Carta", "Descrizione", "Importo", "Data"])
        for voce in spese:
            ws_spese.append_row([
                voce.get("carta", ""),
                voce.get("descrizione", ""),
                voce.get("importo", ""),
                voce.get("data", "")
            ])

        return jsonify({"status": "ok"})

    except gspread.exceptions.WorksheetNotFound as ex:
        print("Foglio 'SPESE' non trovato:", ex)
        return jsonify({"status": "error", "message": "Foglio 'SPESE' non trovato:" + str(ex)}), 500
    except Exception as e:
        print("Errore durante la sincronizzazione:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
