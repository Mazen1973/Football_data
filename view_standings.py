import sqlite3

conn = sqlite3.connect("football.db")
cur = conn.cursor()

print("Premier League Standings (2023):")
print("=" * 80)
print(f"{'Pos':<5} {'Team':<25} {'P':<4} {'W':<4} {'D':<4} {'L':<4} {'GF':<4} {'GA':<4} {'GD':<5} {'Pts':<4}")
print("-" * 80)

cur.execute("""
    SELECT position, team_name, played, wins, draws, loses, 
           goals_for, goals_against, goals_diff, points 
    FROM standings 
    ORDER BY position
""")

for row in cur.fetchall():
    pos, team, p, w, d, l, gf, ga, gd, pts = row
    print(f"{pos:<5} {team:<25} {p or 0:<4} {w or 0:<4} {d or 0:<4} {l or 0:<4} "
          f"{gf or 0:<4} {ga or 0:<4} {gd or 0:<5} {pts or 0:<4}")

print("\n" + "=" * 80)

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cur.fetchall()]
print(f"\nTables in database: {', '.join(tables)}")

conn.close()

