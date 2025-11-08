import sqlite3

conn = sqlite3.connect("football.db")
cur = conn.cursor()

print("=== Football Database Editor ===\n")

while True:
    print("\nWhat would you like to do?")
    print("1. View all teams")
    print("2. Update a team name")
    print("3. Update a team's country")
    print("4. Update a team's founded year")
    print("5. Add a new team")
    print("6. Delete a team")
    print("7. Exit")
    
    choice = input("\nEnter your choice (1-7): ").strip()
    
    if choice == "1":
        cur.execute("SELECT team_id, name, country, founded FROM teams ORDER BY team_id")
        teams = cur.fetchall()
        print("\nAll teams:")
        print("-" * 60)
        for team in teams:
            print(f"ID: {team[0]}, Name: {team[1]}, Country: {team[2]}, Founded: {team[3]}")
    
    elif choice == "2":
        team_id = input("Enter team ID to update: ").strip()
        new_name = input("Enter new team name: ").strip()
        cur.execute("UPDATE teams SET name = ? WHERE team_id = ?", (new_name, team_id))
        conn.commit()
        print(f"✅ Updated team {team_id} name to '{new_name}'")
    
    elif choice == "3":
        team_id = input("Enter team ID to update: ").strip()
        new_country = input("Enter new country: ").strip()
        cur.execute("UPDATE teams SET country = ? WHERE team_id = ?", (new_country, team_id))
        conn.commit()
        print(f"✅ Updated team {team_id} country to '{new_country}'")
    
    elif choice == "4":
        team_id = input("Enter team ID to update: ").strip()
        new_year = input("Enter new founded year: ").strip()
        cur.execute("UPDATE teams SET founded = ? WHERE team_id = ?", (new_year, team_id))
        conn.commit()
        print(f"✅ Updated team {team_id} founded year to {new_year}")
    
    elif choice == "5":
        name = input("Enter team name: ").strip()
        country = input("Enter country: ").strip()
        founded = input("Enter founded year (or press Enter to skip): ").strip()
        founded = int(founded) if founded else None
        cur.execute("SELECT MAX(team_id) FROM teams")
        max_id = cur.fetchone()[0] or 0
        new_id = max_id + 1
        cur.execute("INSERT INTO teams (team_id, name, country, founded) VALUES (?, ?, ?, ?)",
                   (new_id, name, country, founded))
        conn.commit()
        print(f"✅ Added new team: {name} (ID: {new_id})")
    
    elif choice == "6":
        team_id = input("Enter team ID to delete: ").strip()
        cur.execute("SELECT name FROM teams WHERE team_id = ?", (team_id,))
        team = cur.fetchone()
        if team:
            confirm = input(f"Are you sure you want to delete '{team[0]}'? (yes/no): ").strip().lower()
            if confirm == "yes":
                cur.execute("DELETE FROM teams WHERE team_id = ?", (team_id,))
                conn.commit()
                print(f"✅ Deleted team {team_id}")
            else:
                print("❌ Deletion cancelled")
        else:
            print(f"❌ Team with ID {team_id} not found")
    
    elif choice == "7":
        print("👋 Goodbye!")
        break
    
    else:
        print("❌ Invalid choice. Please enter 1-7.")

conn.close()

