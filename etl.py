"""
etl.py
Fetches NFL player and team data from RapidAPI
and loads into SQLite for analysis.
"""

import os
import sqlite3
import requests
import pandas as pd
import datetime
from dotenv import load_dotenv

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")
DB_PATH = os.getenv("DB_PATH", "nfl.db")

if not RAPIDAPI_KEY or not RAPIDAPI_HOST:
    print("FATAL ERROR: RAPIDAPI_KEY and RAPIDAPI_HOST environment variables must be set.")
    print("Please set these variables to your actual credentials.")
    exit(1)

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}

BASE_URL = f"https://{RAPIDAPI_HOST}"


def get(endpoint, params=None):
    """Generic function to make the authenticated API call."""
    r = requests.get(f"{BASE_URL}/{endpoint}", headers=HEADERS, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def run_schema(conn):
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())

def extract_teams():
    data = get("nfl-team-listing/v1/data")
    extracted = []
    for item in data:
        team = item.get("team", {})
        extracted.append({
            "team_id": int(team.get("id")),
            "name": team.get("displayName"),
            "abbreviation": team.get("abbreviation"),
            "location": team.get("location")
        })
    return pd.DataFrame(extracted)

def getPlayers(team_id):
    data = get(f"nfl-player-listing/v1/data?id={team_id}")
    extracted = []
    athletes = data.get('athletes', [])
    for athlete in athletes:
        position = athlete.get('position')
        for player_info in athlete.get('items', []):
            format_string = '%Y-%m-%dT%H:%MZ'
            date_object = datetime.datetime.strptime(player_info.get("dateOfBirth"), format_string)
            extracted.append({
                "player_id": int(player_info.get("id")),
                "team_id": int(team_id),
                "firstName": player_info.get("firstName"),
                "lastName": player_info.get("lastName"),
                "unit": position,
                "position": player_info.get('position', {}).get('abbreviation'),
                "weight": int(player_info.get("weight")),
                "height": player_info.get("displayHeight"),
                "age": int(player_info.get("age")),
                "dob": date_object.strftime('%Y-%m-%d'),
                "college": player_info.get('college', {}).get('name')
            })
    return pd.DataFrame(extracted)

def upsert_df(conn, df, table):
    if table == "players":
        pk_col = "player_id"
    elif table == "teams":
        pk_col = "team_id"
    else:
        pk_col = df.columns[0]
    df.to_sql(f"_{table}_staging", conn, if_exists="replace", index=False)
    cols = ",".join(df.columns)
    set_clause = ",".join([f"{c}=excluded.{c}" for c in df.columns])
    conn.execute(f"""
        DELETE FROM {table} 
        WHERE {pk_col} IN (SELECT {pk_col} FROM _{table}_staging)
    """)
    conn.execute(f"INSERT INTO {table} ({cols}) SELECT {cols} FROM _{table}_staging")
    conn.execute(f"DROP TABLE _{table}_staging")


def main():
    print(f"Starting ETL process. DB Path: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    run_schema(conn)

    # 1. Load Teams
    print("Extracting and Loading Teams...")
    teams_df = extract_teams()
    upsert_df(conn, teams_df, "teams")
    print(f"Successfully loaded {len(teams_df)} teams.")
    conn.commit()

    # 2. Load Players
    all_players_df = pd.DataFrame()

    print("Extracting and Loading Players...")
    for team_id in teams_df['team_id']:
        try:
            players_df = getPlayers(team_id)
            all_players_df = pd.concat([all_players_df, players_df], ignore_index=True)
            print(f" -> Loaded {len(players_df)} players for Team ID {team_id}.")
            
        except Exception as e:
            print(f"An error occurred while fetching roster for team ID {team_id}: {e}")
            continue

    all_players_df.drop_duplicates(subset=['player_id'], inplace=True) 
    upsert_df(conn, all_players_df, "players")
    print(f"Successfully loaded {len(all_players_df)} unique players into the 'players' table.")

    conn.commit()
    conn.close()
    print("data loaded into nfl.db")

if __name__ == "__main__":
    main()