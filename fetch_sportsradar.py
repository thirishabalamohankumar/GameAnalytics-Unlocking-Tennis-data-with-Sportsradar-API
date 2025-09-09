import requests
import psycopg2
import json

# -------------------
# 1. API CONFIG
# -------------------
API_KEY = "ZKVxrIooAl3GcSMHCfUqocsuSeSBdMFSahtqjfGL"   # Replace with your Sportradar API key
BASE_URL = "https://api.sportradar.com/tennis/trial/v3/en"

ENDPOINTS = {
    "competitions": f"{BASE_URL}/competitions.json?api_key={API_KEY}",
    "complexes": f"{BASE_URL}/complexes.json?api_key={API_KEY}",
    "doubles_competitor_rankings": f"{BASE_URL}/double_competitors_rankings.json?api_key={API_KEY}",  # doubles
    "rankings": f"{BASE_URL}/rankings.json?api_key={API_KEY}",  # singles (ATP/WTA)
}

# -------------------
# 2. DATABASE CONFIG
# -------------------
DB_CONFIG = {
    "dbname": "tennis_db",
    "user": "postgres",
    "password": "Tthiri!21@003",
    "host": "localhost",
    "port": "5432"
}

# -------------------
# 3. FETCH FUNCTION
# -------------------
def fetch_data(endpoint_name, url):
    print(f"Fetching {endpoint_name}...")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching {endpoint_name}: {e}")
        return None

# -------------------
# 4A. SAVE RAW JSON (into raw_* tables)
# -------------------
def save_raw_json(table, data):
    raw_table = f"raw_{table}"   # avoid collision with structured tables
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {raw_table} (
            id SERIAL PRIMARY KEY,
            data JSONB
        );
    """)

    cur.execute(f"TRUNCATE TABLE {raw_table};")
    cur.execute(f"INSERT INTO {raw_table} (data) VALUES (%s)", [json.dumps(data)])

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Saved {table} data to {raw_table} (JSON, refreshed)")

# -------------------
# 4B. SAVE COMPETITORS + PLAYERS
# -------------------
def save_competitors(data):
    if "rankings" not in data:
        print("⚠️ No competitor ranking data found")
        return

    competitors = []
    players = []

    for tour in data["rankings"]:   # ATP / WTA / Doubles
        for competitor in tour.get("competitor_rankings", []):
            comp_id = competitor.get("competitor", {}).get("id")
            comp_name = competitor.get("competitor", {}).get("name")
            comp_country = competitor.get("competitor", {}).get("country")

            competitors.append((
                comp_id,
                comp_name,
                comp_country,
                tour.get("type"),              # tour_type (ATP/WTA/DOUBLES)
                competitor.get("rank"),
                competitor.get("movement"),
                competitor.get("points")
            ))

            for player in competitor.get("players", []):
                players.append((
                    comp_id,  
                    player.get("id"),
                    player.get("name"),
                    player.get("country")
                ))

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Competitors table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS competitors (
            id SERIAL PRIMARY KEY,
            competitor_id TEXT UNIQUE,
            name TEXT,
            country TEXT,
            tour_type TEXT,
            rank INT,
            movement TEXT,
            points INT
        );
    """)

    # Competitor players (for doubles teams)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS competitor_players (
            id SERIAL PRIMARY KEY,
            competitor_id TEXT REFERENCES competitors(competitor_id),
            player_id TEXT,
            name TEXT,
            country TEXT
        );
    """)

    # UPSERT competitors
    for comp in competitors:
        cur.execute("""
            INSERT INTO competitors (competitor_id, name, country, tour_type, rank, movement, points)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (competitor_id) DO UPDATE SET
                name = EXCLUDED.name,
                country = EXCLUDED.country,
                tour_type = EXCLUDED.tour_type,
                rank = EXCLUDED.rank,
                movement = EXCLUDED.movement,
                points = EXCLUDED.points;
        """, comp)

    # UPSERT players
    for pl in players:
        cur.execute("""
            INSERT INTO competitor_players (competitor_id, player_id, name, country)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, pl)

    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ Saved/Updated {len(competitors)} competitors and {len(players)} players to database")

# -------------------
# 5. MAIN SCRIPT
# -------------------
if __name__ == "__main__":
    for name, url in ENDPOINTS.items():
        data = fetch_data(name, url)
        if not data:
            continue

        if name in ["doubles_competitor_rankings", "rankings"]:
            save_competitors(data)     # structured competitors + players
            save_raw_json(name, data)  # raw JSON backup
        else:
            save_raw_json(name, data)
