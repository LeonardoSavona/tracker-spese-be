import os
from google_manager import SPREADSHEET_ID, INTERVALLI_CARTA, SHEET_NAME

def get_settings():
    return {
        "Spredsheet ID": SPREADSHEET_ID,
        "Sheet Name": SHEET_NAME,
        "Intervalli Carte": INTERVALLI_CARTA}

def saveSettings(settings):
    global SPREADSHEET_ID, INTERVALLI_CARTA, SHEET_NAME
    SPREADSHEET_ID = settings.get("Spredsheet ID")
    INTERVALLI_CARTA = settings.get("Intervalli Carte")
    SHEET_NAME = settings.get("Sheet Name")
    os.environ.update({
        "SPREADSHEET_ID": SPREADSHEET_ID,
        "INTERVALLI_CARTA": str(INTERVALLI_CARTA),
        "SHEET_NAME": SHEET_NAME
    })