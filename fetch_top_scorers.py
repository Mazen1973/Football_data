import os
import sqlite3
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
if not API_KEY:
    print("Error: RAPIDAPI_KEY not found in .env file")
    exit(1)

if len(API_KEY) == 32:
    HOST = "v3.football.api-sports.io"
    url = f"https://{HOST}/players/topscorers"
    headers = {
        "x-apisports-key": API_KEY
    }
else:
    HOST = "api-football-v1.p.rapidapi.com"
    url = f"https://{HOST}/v3/players/topscorers"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": HOST
    }

params = {"league": "39", "season": "2023"}

print("Fetching top scorers...")
resp = requests.get(url, headers=headers, params=params, timeout=30)
if resp.status_code != 200:
    print(f"Error {resp.status_code}: {resp.text}")
    exit(1)

data = resp.json()

conn = sqlite3.connect("football.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS top_scorers (
  player_id INTEGER PRIMARY KEY,
  player_name TEXT NOT NULL,
  team_id INTEGER,
  team_name TEXT,
  position TEXT,
  nationality TEXT,
  age INTEGER,
  goals INTEGER,
  assists INTEGER,
  appearances INTEGER,
  shots_total INTEGER,
  shots_on_target INTEGER
)
""")

count = 0
if "response" in data:
    for item in data["response"]:
        player = item.get("player", {})
        player_id = player.get("id")
        player_name = player.get("name")
        position = player.get("position")
        nationality = player.get("nationality")
        age = player.get("age")
        
        team_info = item.get("statistics", [{}])[0].get("team", {}) if item.get("statistics") else {}
        team_id = team_info.get("id")
        team_name = team_info.get("name")
        
        stats = item.get("statistics", [{}])[0] if item.get("statistics") else {}
        goals = stats.get("goals", {}).get("total")
        assists = stats.get("goals", {}).get("assists")
        appearances = stats.get("games", {}).get("appearences")
        shots_total = stats.get("shots", {}).get("total")
        shots_on_target = stats.get("shots", {}).get("on")
        
        if player_id and player_name:
            cur.execute(
                """INSERT OR REPLACE INTO top_scorers 
                (player_id, player_name, team_id, team_name, position, nationality, 
                 age, goals, assists, appearances, shots_total, shots_on_target) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (player_id, player_name, team_id, team_name, position, nationality,
                 age, goals, assists, appearances, shots_total, shots_on_target)
            )
            count += 1

conn.commit()
conn.close()
print(f"Saved {count} rows into top_scorers table")

