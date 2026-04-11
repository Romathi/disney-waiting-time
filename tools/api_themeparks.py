# MIT License
# Copyright (c) 2026 Romathi


from datetime import datetime

import requests

# --- CONFIGURATION ---
PARK_ID = "e8d0207f-da8a-4048-bec8-117aa946b2c2"


def collect():
    url = f"https://api.themeparks.wiki/v1/entity/{PARK_ID}/live"
    attraction_datas = {}
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()

        for attraction in data.get("liveData", []):
            last_up = attraction.get("lastUpdated")
            name = attraction.get("name")
            park_id = attraction.get("parkId")
            queue = attraction.get("queue")
            status = attraction.get("status")

            wait = None
            if queue and "STANDBY" in queue:
                wait = queue["STANDBY"].get("waitTime")

            attraction_datas[name] = {
                "last_up": last_up,
                "park_id": park_id,
                "status": status,
                "wait_time": wait,
            }

    except Exception as e:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] Error during retrieval: {e}")

    return attraction_datas
