# MIT License
# Copyright (c) 2026 Romathi


import time
from datetime import datetime

from tools.api_themeparks import collect
from tools.sql_lite import close_db_connection, get_db_connection, init_db, insert_data

# --- CONFIGURATION ---
## SQL
DB_NAME = "disney_data.db"

## API Theme Parks
PARK_ID = "e8d0207f-da8a-4048-bec8-117aa946b2c2"
PARK_NAME = "Disneyland Paris"

## Refresh
INTERVAL = 300  # 5 minutes

## Mode
TEST_MODE = True


def main():
    try:
        attractions = collect()
        conn = get_db_connection(DB_NAME)
        cursor = conn.cursor()
        insert_data(cursor, attractions, PARK_NAME)
        close_db_connection(conn)
    except Exception as e:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] Error during SQL writing: {e}")


if __name__ == "__main__":
    init_db(DB_NAME)
    if TEST_MODE:
        main()
    else:
        while True:
            # On peut laisser tourner 24h/24, le script filtrera de lui-même
            # ou enregistrera les statuts "CLOSED" ce qui est utile pour l'analyse
            print("Collecting data for Disneyland Paris attractions. Press Ctrl+C to stop...")
            main()
            time.sleep(INTERVAL)
