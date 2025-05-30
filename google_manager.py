import json
import base64
import os
import gspread
from dotenv import load_dotenv
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import CellFormat, format_cell_range, NumberFormat

load_dotenv()

SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")

INTERVALLI_CARTA = {
    "Banco BPM": {"range": "13:27"},
    "Revolut": {"range": "45:119"}
}

gspread_client = None

def get_gspread_client():
    global gspread_client
    if not gspread_client:
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
        gspread_client = gspread.authorize(creds)
    return gspread_client

def update_spese(spese):
    gc = get_gspread_client()
    sh = gc.open_by_key(SPREADSHEET_ID)
    ws = sh.worksheet("SPESE")

    for voce in spese:
        inserisci_voce_spesa(ws,
            carta=voce.get("carta", ""),
            descrizione=voce.get("descrizione", ""),
            importo=voce.get("importo", ""),
            data_str=voce.get("data", "")
        )

def inserisci_voce_spesa(ws, carta, descrizione, importo, data_str):
    if carta not in INTERVALLI_CARTA:
        raise ValueError("Carta non riconosciuta")

    col_descr, col_importo, col_data = range_colonne(data_str)
    range_str = INTERVALLI_CARTA[carta]["range"]
    start_row = int(range_str.split(":")[0])
    end_row = int(range_str.split(":")[1])

    month_rows = f"{col_descr}{start_row}:{col_descr}{end_row}"
    rows_descriptions = ws.get(month_rows)
    riga = len(rows_descriptions) + start_row

    if riga > end_row:
        raise ValueError("Il numero di righe supera il limite consentito.")
    else:
        ws.update(f"{col_descr}{riga}", descrizione)
        ws.update(f"{col_importo}{riga}", float(importo))
        
        data_obj = datetime.strptime(data_str, "%Y-%m-%d")
        serial_date = datetime_to_serial_number(data_obj)
        ws.update(f"{col_data}{riga}", serial_date)

        format_cell_range(ws, f"{col_data}{riga}", CellFormat(
            numberFormat=NumberFormat(type="DATE", pattern="dd/mm/yyyy")
        ))
        return True
        
def range_colonne(data_str):
    data = datetime.strptime(data_str, "%Y-%m-%d")
    mese_index = data.month
    colonne = [
        ["B","C","D"],["E","F","G"],["H","I","J"],
        ["K","L","M"],["N","O","P"],["Q","R","S"],
        ["T","U","V"],["W","X","Y"],["Z","AA","AB"],
        ["AC","AD","AE"],["AF","AG","AH"],["AI","AJ","AK"]
    ]
    return colonne[mese_index-1]

def datetime_to_serial_number(dt):
    epoch = datetime(1899, 12, 30)
    delta = dt - epoch
    return delta.days + delta.seconds / 86400
