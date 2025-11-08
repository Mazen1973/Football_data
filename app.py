from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_PATH = "football.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/api/teams", methods=["GET"])
def get_teams():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM teams ORDER BY name")
    teams = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(teams)

@app.route("/api/standings", methods=["GET"])
def get_standings():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM standings ORDER BY position")
    standings = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(standings)

@app.route("/api/fixtures", methods=["GET"])
def get_fixtures():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM fixtures ORDER BY date, time")
    fixtures = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(fixtures)

@app.route("/api/top-scorers", methods=["GET"])
def get_top_scorers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM top_scorers ORDER BY goals DESC, assists DESC")
    scorers = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(scorers)

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True, port=5500)

