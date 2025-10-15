import os
import sqlite3
import requests
import pandas as pd
from datetime import datetime

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")
DB_PATH = os.getenv("DB_PATH", "nfl.db")

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}
BASE_URL = f"https://{RAPIDAPI_HOST}/"


def get(endpoint, params=None):
    r = requests.get(f"{BASE_URL}/{endpoint}", headers=HEADERS, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def extract_teams():
    data = get("nfl-team-listing/v1/data")
    extracted = []
    for item in data:
        team = item.get("team", {})
        extracted.append({
            "team_id": team.get("id"),
            "display_name": team.get("displayName"),
            "name": team.get("name"),
            "nickname": team.get("nickname"),
            "location": team.get("location")
        })
    return pd.DataFrame(extracted)
