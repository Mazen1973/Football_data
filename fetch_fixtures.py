import os
import sqlite3
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
if not API_KEY:
    print("Error: RAPIDAPI_KEY not found in .env file")
    exit(1)

if len(API_KEY) == 32:
    HOST = "v3.football.api-sports.io"
    url = f"https://{HOST}/fixtures"
    headers = {
        "x-apisports-key": API_KEY
    }
else:
    HOST = "api-football-v1.p.rapidapi.com"
    url = f"https://{HOST}/v3/fixtures"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": HOST
    }

params = {
    "league": "39", 
    "season": "2023",
    "round": "Regular Season - 38"
}

print("Fetching upcoming fixtures...")
resp = requests.get(url, headers=headers, params=params, timeout=30)
if resp.status_code != 200:
    print(f"Error {resp.status_code}: {resp.text}")
    exit(1)

data = resp.json()

conn = sqlite3.connect("football.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS fixtures (
  fixture_id INTEGER PRIMARY KEY,
  date TEXT NOT NULL,
  time TEXT,
  venue_name TEXT,
  venue_city TEXT,
  home_team_id INTEGER,
  home_team_name TEXT NOT NULL,
  away_team_id INTEGER,
  away_team_name TEXT NOT NULL,
  home_goals INTEGER,
  away_goals INTEGER,
  status TEXT,
  round TEXT
)
""")

count = 0
if "response" in data:
    for fixture in data["response"]:
        fixture_id = fixture.get("fixture", {}).get("id")
        fixture_date = fixture.get("fixture", {}).get("date")
        fixture_time = fixture.get("fixture", {}).get("time")
        venue = fixture.get("fixture", {}).get("venue", {})
        venue_name = venue.get("name")
        venue_city = venue.get("city")
        
        home_team = fixture.get("teams", {}).get("home", {})
        home_team_id = home_team.get("id")
        home_team_name = home_team.get("name")
        home_goals = fixture.get("goals", {}).get("home")
        
        away_team = fixture.get("teams", {}).get("away", {})
        away_team_id = away_team.get("id")
        away_team_name = away_team.get("name")
        away_goals = fixture.get("goals", {}).get("away")
        
        status = fixture.get("fixture", {}).get("status", {}).get("long")
        round_info = fixture.get("league", {}).get("round")
        
        if fixture_id and home_team_name and away_team_name:
            date_str = fixture_date[:10] if fixture_date else None
            time_str = fixture_time if fixture_time else None
            
            cur.execute(
                """INSERT OR REPLACE INTO fixtures 
                (fixture_id, date, time, venue_name, venue_city, 
                 home_team_id, home_team_name, away_team_id, away_team_name,
                 home_goals, away_goals, status, round) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (fixture_id, date_str, time_str, venue_name, venue_city,
                 home_team_id, home_team_name, away_team_id, away_team_name,
                 home_goals, away_goals, status, round_info)
            )
            count += 1

conn.commit()
conn.close()
print(f"Saved {count} rows into fixtures table")

