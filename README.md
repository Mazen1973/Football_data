# Football_data

Fetch football data from API-Football v3 (via RapidAPI) and save it to SQLite. Includes a modern web frontend to view the data.

## Setup

### Backend Setup

1. Create a virtual environment:
```bash
python3 -m venv .venv
```

2. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your RapidAPI key:
```
RAPIDAPI_KEY=YOUR_X_RAPIDAPI_KEY
```

Alternatively, you can set it as an environment variable:
   - Windows (PowerShell): `$env:RAPIDAPI_KEY="YOUR_X_RAPIDAPI_KEY"`
   - Windows (CMD): `set RAPIDAPI_KEY=YOUR_X_RAPIDAPI_KEY`
   - macOS/Linux: `export RAPIDAPI_KEY="YOUR_X_RAPIDAPI_KEY"`

### Frontend Setup

1. Install Node.js dependencies:
```bash
npm install
```

## Usage

### Fetching Data

Run the fetch scripts to populate the database:
```bash
python fetch.py              # Fetch teams
python fetch_standings.py    # Fetch standings
python fetch_fixtures.py     # Fetch fixtures
python fetch_top_scorers.py  # Fetch top scorers
```

This will:
- Fetch Premier League data (league=39, season=2023) from API-Football v3
- Create a SQLite database file `football.db`
- Create tables and insert the fetched data

### Running the Application

1. Start the Flask API backend (in one terminal):
```bash
python app.py
```
The API will run on `http://localhost:5000`

2. Start the React frontend (in another terminal):
```bash
npm run dev
```
The frontend will run on `http://localhost:3000`

Open your browser and navigate to `http://localhost:3000` to view the dashboard.

## Features

The web dashboard includes:
- **Standings**: View league table with position, points, goals, and form
- **Teams**: Browse all teams with country and founding year
- **Fixtures**: See upcoming and past matches with scores
- **Top Scorers**: View top goal scorers with detailed statistics

## Database Schema

The database includes the following tables:
- `teams` - Team information (team_id, name, country, founded)
- `standings` - League standings (position, points, goals, form)
- `fixtures` - Match fixtures (date, teams, scores, status)
- `top_scorers` - Player statistics (goals, assists, appearances)

## Viewing Data in DBeaver

1. Open DBeaver
2. Go to Database → New Database Connection
3. Choose SQLite
4. In "Database file", select `football.db` from this directory
5. Finish → expand the DB → expand tables → right-click any table → Read data
