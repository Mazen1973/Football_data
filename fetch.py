import os
import sqlite3
import requests
from dotenv import load_dotenv

load_dotenv()

# 1) API setup (replace with your actual key)
API_KEY = os.getenv("RAPIDAPI_KEY")
if not API_KEY or API_KEY == "YOUR_X_RAPIDAPI_KEY":
    print("Warning: RAPIDAPI_KEY not found in environment. Please check your .env file.")
    API_KEY = "YOUR_X_RAPIDAPI_KEY"

# Try API-Football direct API first (if key is 32 chars, it's likely direct API)
if len(API_KEY) == 32:
    HOST = "v3.football.api-sports.io"
    url = f"https://{HOST}/teams"
    headers = {
        "x-apisports-key": API_KEY
    }
else:
    # RapidAPI format
    HOST = "api-football-v1.p.rapidapi.com"
    url = f"https://{HOST}/v3/teams"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": HOST
    }

# 2) Choose something specific to keep it simple
# Premier League: league=39, season=2023 (example values from docs)
params = {"league": "39", "season": "2023"}

print("Fetching teams...")
resp = requests.get(url, headers=headers, params=params, timeout=30)
if resp.status_code != 200:
    print(f"Error {resp.status_code}: {resp.text}")
    print("\nPlease verify:")
    print("1. You have subscribed to 'API-Football v3' on RapidAPI")
    print("2. Your subscription is active (not expired)")
    print("3. The API key is correct")
    resp.raise_for_status()
data = resp.json()

# 3) Prepare SQLite
conn = sqlite3.connect("football.db")
cur = conn.cursor()

# One table, 4+ columns. We'll store: team_id, name, country, founded_year
cur.execute("""
CREATE TABLE IF NOT EXISTS teams (
  team_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  country TEXT,
  founded INTEGER
)
""")

# 4) Insert rows
count = 0
for item in data.get("response", []):
    team = item.get("team", {})
    team_id = team.get("id")
    name = team.get("name")
    country = team.get("country")
    founded = team.get("founded")
    if team_id and name:
        cur.execute(
            "INSERT OR REPLACE INTO teams (team_id, name, country, founded) VALUES (?, ?, ?, ?)",
            (team_id, name, country, founded)
        )
        count += 1

conn.commit()
conn.close()
print(f"Saved {count} rows into football.db")

