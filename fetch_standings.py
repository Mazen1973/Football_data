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
    url = f"https://{HOST}/standings"
    headers = {
        "x-apisports-key": API_KEY
    }
else:
    HOST = "api-football-v1.p.rapidapi.com"
    url = f"https://{HOST}/v3/standings"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": HOST
    }

params = {"league": "39", "season": "2023"}

print("Fetching league standings...")
resp = requests.get(url, headers=headers, params=params, timeout=30)
if resp.status_code != 200:
    print(f"Error {resp.status_code}: {resp.text}")
    exit(1)

data = resp.json()

conn = sqlite3.connect("football.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS standings (
  position INTEGER,
  team_id INTEGER,
  team_name TEXT NOT NULL,
  played INTEGER,
  wins INTEGER,
  draws INTEGER,
  loses INTEGER,
  goals_for INTEGER,
  goals_against INTEGER,
  goals_diff INTEGER,
  points INTEGER,
  form TEXT,
  PRIMARY KEY (team_id)
)
""")

count = 0
if "response" in data and len(data["response"]) > 0:
    standings_data = data["response"][0].get("league", {}).get("standings", [])
    
    if standings_data and len(standings_data) > 0:
        for team_standing in standings_data[0]:
            position = team_standing.get("rank")
            team_info = team_standing.get("team", {})
            team_id = team_info.get("id")
            team_name = team_info.get("name")
            
            all_stats = team_standing.get("all", {})
            played = all_stats.get("played")
            wins = all_stats.get("win")
            draws = all_stats.get("draw")
            loses = all_stats.get("lose")
            
            goals = team_standing.get("goals", {})
            goals_for = goals.get("for")
            goals_against = goals.get("against")
            goals_diff = team_standing.get("goalsDiff")
            points = team_standing.get("points")
            form = team_standing.get("form")
            
            if team_id and team_name:
                cur.execute(
                    """INSERT OR REPLACE INTO standings 
                    (position, team_id, team_name, played, wins, draws, loses, 
                     goals_for, goals_against, goals_diff, points, form) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (position, team_id, team_name, played, wins, draws, loses,
                     goals_for, goals_against, goals_diff, points, form)
                )
                count += 1

conn.commit()
conn.close()
print(f"Saved {count} rows into standings table")

