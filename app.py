# MIT License
# Copyright (c) 2026 Romathi

import sqlite3

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from app.best_per_slot import get_detailed_best_picks
from app.favorites import manage_favorites_ui
from app.filters import get_filters
from app.graphs import get_graphs
from app.key_numbers import get_key_numbers
from app.means import get_means
from main import DB_NAME

# Actualise toutes les 5 minutes (300 000 millisecondes)
st_autorefresh(interval=300000, key="datarefresh")

# Configuration de la page
st.set_page_config(page_title="Disney Analytics", layout="wide")


def load_data():
    conn = sqlite3.connect(DB_NAME)
    query = """
            SELECT w.*,
                   COALESCE(s.is_favorite, 0) as is_favorite
            FROM wait_times w
                     LEFT JOIN attractions_settings s ON w.attraction_name = s.attraction_name \
            """
    _df = pd.read_sql_query(query, conn)
    conn.close()
    _df["timestamp"] = pd.to_datetime(_df["timestamp"])
    _df["timestamp"] = _df["timestamp"].dt.tz_localize("UTC").dt.tz_convert("Europe/Paris")
    # On garde OPERATING pour les moyennes, mais on garde tout pour l'historique
    return _df


st.title("🎢 Disneyland Paris - Optimization Dashboard")
try:
    # 1. Chargement initial
    df = load_data()

    # 2. Application des filtres de base (Parc, etc.)
    selected_park, filtered_df = get_filters(st, df)


    # 4. Définition des attractions ouvertes MAINTENANT
    open_attractions = filtered_df[
        (filtered_df["status"] == "OPERATING")
        & (filtered_df["wait_time"].notna())  # Pas de NULL
        & (filtered_df["wait_time"] > 0)  # Pas de 0 si tu considères que c'est une erreur
    ]

    # 3. Gestion des favoris (Checkboxes + Toggle)
    # IMPORTANT : Ta fonction manage_favorites_ui doit utiliser la clé "show_only_favs"
    # pour son st.sidebar.toggle(..., key="show_only_favs")
    show_only = manage_favorites_ui(st, open_attractions, DB_NAME)

    # 5. LE FILTRE FINAL (Correction de la logique)
    # On utilise directement show_only qui est renvoyé par ton composant
    if show_only:
        has_favs = not filtered_df[filtered_df["is_favorite"] == 1].empty
        if has_favs:
            # On réassigne les deux variables pour tout le reste du script
            filtered_df = filtered_df[filtered_df["is_favorite"] == 1].copy()
            open_attractions = open_attractions[open_attractions["is_favorite"] == 1].copy()
        else:
            st.sidebar.warning("No favorites selected!")

    # --- SECTION 1: KEY NUMBERS ---
    # Ici, filtered_df et open_attractions sont déjà potentiellement filtrés
    get_key_numbers(st, filtered_df, open_attractions)

    # --- SECTION 2: MEANS ---
    get_means(st, filtered_df, open_attractions)

    st.divider()

    # --- SECTION 3: TENDENCY GRAPHS ---
    # Le graphique n'affichera que les favoris si show_only est actif
    get_graphs(st, filtered_df)

    st.divider()

    # --- SECTION 4: OPTIMIZATION ---
    # Le Top 10 ne montrera que les favoris si show_only est actif
    get_detailed_best_picks(st, open_attractions)


    st.warning(
        "⚠️ The data is updated every 5 minutes. "
        "It does not display the '''real''' wait time, as the source is not official. "
        "Some differences may occur."
    )

    st.caption("💧 Source: https://themeparks.wiki/browse/e8d0207f-da8a-4048-bec8-117aa946b2c2/live")
except Exception as e:
    st.error(f"Error: {e}")
    st.info("Check that the disney_data.db file is present in the same folder as this script.")
