import sqlite3

conn = sqlite3.connect("football.db")
cur = conn.cursor()

print("=" * 80)
print("TOP SCORERS (Premier League 2023)")
print("=" * 80)
print(f"{'Rank':<6} {'Player':<25} {'Team':<20} {'Goals':<7} {'Assists':<8} {'Apps':<5}")
print("-" * 80)

cur.execute("""
    SELECT player_name, team_name, goals, assists, appearances
    FROM top_scorers
    ORDER BY goals DESC, assists DESC
    LIMIT 15
""")

rank = 1
for row in cur.fetchall():
    player, team, goals, assists, apps = row
    print(f"{rank:<6} {player:<25} {team or 'N/A':<20} {goals or 0:<7} {assists or 0:<8} {apps or 0:<5}")
    rank += 1

print("\n" + "=" * 80)
print("UPCOMING FIXTURES")
print("=" * 80)
print(f"{'Date':<12} {'Time':<8} {'Home Team':<25} {'vs':<5} {'Away Team':<25} {'Status':<15}")
print("-" * 80)

cur.execute("""
    SELECT date, time, home_team_name, away_team_name, home_goals, away_goals, status
    FROM fixtures
    ORDER BY date, time
    LIMIT 10
""")

for row in cur.fetchall():
    date, time, home, away, home_goals, away_goals, status = row
    date_str = date if date else "TBD"
    time_str = time if time else ""
    
    if home_goals is not None and away_goals is not None:
        match_str = f"{home} {home_goals}-{away_goals} {away}"
    else:
        match_str = f"{home} vs {away}"
    
    status_str = status or "Scheduled"
    print(f"{date_str:<12} {time_str:<8} {match_str:<55} {status_str:<15}")

print("\n" + "=" * 80)

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cur.fetchall()]
print(f"\nAll tables in database: {', '.join(tables)}")

conn.close()

