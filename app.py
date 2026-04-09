# MIT License
# Copyright (c) 2026 Romathi

import sqlite3

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from app.filters import get_filters
from app.graphs import get_graphs
from app.key_numbers import get_key_numbers
from app.means import get_means

# Actualise toutes les 5 minutes (300 000 millisecondes)
st_autorefresh(interval=300000, key="datarefresh")

# Configuration de la page
st.set_page_config(page_title="Disney Analytics", layout="wide")


def load_data():
    conn = sqlite3.connect("disney_data.db")
    _df = pd.read_sql_query("SELECT * FROM wait_times", conn)
    conn.close()
    _df["timestamp"] = pd.to_datetime(_df["timestamp"])
    _df["timestamp"] = _df["timestamp"].dt.tz_localize("UTC").dt.tz_convert("Europe/Paris")
    # On garde OPERATING pour les moyennes, mais on garde tout pour l'historique
    return _df


st.title("🎢 Disneyland Paris - Optimization Dashboard")

try:
    df = load_data()

    # Set the filters in the left sidebar.
    selected_park, filtered_df = get_filters(st, df)

    # --- SECTION 1: KEY NUMBERS ---
    open_attractions = df[(df["status"] == "OPERATING") & (df["wait_time"].notna())]
    get_key_numbers(st, filtered_df, open_attractions)

    # --- SECTION 2: MEANS ---
    get_means(st, filtered_df, open_attractions)
    st.divider()

    # --- SECTION 3: TENDENCY GRAPHS ---
    get_graphs(st, filtered_df)

    st.divider()

    st.warning(
        "⚠️ The data is updated every 5 minutes. "
        "It does not display the '''real''' wait time, as the source is not official. "
        "Some differences may occur."
    )

    st.caption("💧 Source: https://themeparks.wiki/browse/e8d0207f-da8a-4048-bec8-117aa946b2c2/live")
except Exception as e:
    st.error(f"Error: {e}")
    st.info("Check that the disney_data.db file is present in the same folder as this script.")
