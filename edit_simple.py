import sqlite3
import sys

conn = sqlite3.connect("football.db")
cur = conn.cursor()

if len(sys.argv) < 2:
    print("Usage examples:")
    print("  python edit_simple.py view                    # View all teams")
    print("  python edit_simple.py update_name 33 'New Name'  # Update team name")
    print("  python edit_simple.py update_country 33 'Spain'  # Update country")
    print("  python edit_simple.py update_founded 33 1900     # Update founded year")
    print("  python edit_simple.py add 'Team Name' 'Country' 2020  # Add new team")
    print("  python edit_simple.py delete 33                  # Delete team")
    sys.exit(1)

command = sys.argv[1]

if command == "view":
    cur.execute("SELECT team_id, name, country, founded FROM teams ORDER BY team_id")
    teams = cur.fetchall()
    print("\nAll teams:")
    print("-" * 70)
    print(f"{'ID':<5} {'Name':<30} {'Country':<15} {'Founded':<10}")
    print("-" * 70)
    for team in teams:
        print(f"{team[0]:<5} {team[1]:<30} {team[2] or 'N/A':<15} {team[3] or 'N/A':<10}")

elif command == "update_name" and len(sys.argv) == 4:
    team_id = sys.argv[2]
    new_name = sys.argv[3]
    cur.execute("UPDATE teams SET name = ? WHERE team_id = ?", (new_name, team_id))
    conn.commit()
    print(f"✅ Updated team {team_id} name to '{new_name}'")

elif command == "update_country" and len(sys.argv) == 4:
    team_id = sys.argv[2]
    new_country = sys.argv[3]
    cur.execute("UPDATE teams SET country = ? WHERE team_id = ?", (new_country, team_id))
    conn.commit()
    print(f"✅ Updated team {team_id} country to '{new_country}'")

elif command == "update_founded" and len(sys.argv) == 4:
    team_id = sys.argv[2]
    new_year = sys.argv[3]
    cur.execute("UPDATE teams SET founded = ? WHERE team_id = ?", (new_year, team_id))
    conn.commit()
    print(f"✅ Updated team {team_id} founded year to {new_year}")

elif command == "add" and len(sys.argv) >= 4:
    name = sys.argv[2]
    country = sys.argv[3] if len(sys.argv) > 3 else None
    founded = sys.argv[4] if len(sys.argv) > 4 else None
    cur.execute("SELECT MAX(team_id) FROM teams")
    max_id = cur.fetchone()[0] or 0
    new_id = max_id + 1
    cur.execute("INSERT INTO teams (team_id, name, country, founded) VALUES (?, ?, ?, ?)",
               (new_id, name, country, founded))
    conn.commit()
    print(f"✅ Added new team: {name} (ID: {new_id})")

elif command == "delete" and len(sys.argv) == 3:
    team_id = sys.argv[2]
    cur.execute("DELETE FROM teams WHERE team_id = ?", (team_id,))
    conn.commit()
    print(f"✅ Deleted team {team_id}")

else:
    print("❌ Invalid command or missing arguments")
    print("Run 'python edit_simple.py' to see usage examples")

conn.close()

