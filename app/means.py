# MIT License
# Copyright (c) 2026 Romathi

import pandas as pd

def get_means(st, df: pd.DataFrame, open_attractions: pd.DataFrame) -> None:
    st.subheader("📊 Reliability & Statistics")

    # 1. Calcul de la fiabilité (Uptime vs Downtime)
    df["is_down"] = df["status"].apply(lambda x: int(x == "DOWN"))
    df["is_up"] = df["status"].apply(lambda x: int(x == "OPERATING"))

    stats = df.groupby("attraction_name").agg(Down_Events=("is_down", "sum"), Up_Events=("is_up", "sum")).reset_index()

    # Conversion en minutes (intervalle de 5 min)
    stats["Downtime (min)"] = stats["Down_Events"] * 5
    stats["Uptime (min)"] = stats["Up_Events"] * 5
    total_obs = stats["Downtime (min)"] + stats["Uptime (min)"]

    # Calcul du ratio (on gère la division par zéro avec .where)
    stats["Availability %"] = (stats["Uptime (min)"] / total_obs * 100).fillna(0).round(1)

    # 2. Statistiques de temps (Moyenne, Min, Max)
    time_stats = (
        open_attractions.groupby("attraction_name")
        .agg(Avg_Wait=("wait_time", "mean"), Min=("wait_time", "min"), Max=("wait_time", "max"))
        .reset_index()
    )

    time_stats["Avg_Wait"] = time_stats["Avg_Wait"].round(1)

    # 3. Fusion et nettoyage
    final_df = pd.merge(time_stats, stats, on="attraction_name", how="left")

    # Sélection des colonnes utiles pour l'utilisateur
    display_df = final_df[
        ["attraction_name", "Avg_Wait", "Min", "Max", "Availability %"]
    ].copy()

    # Renommer pour un affichage propre
    display_df.columns = [
        "Attraction",
        "Avg Wait (min)",
        "Min",
        "Max",
        "Availability %",
    ]

    # 4. Affichage avec coloration (Gradient)
    # On définit le dégradé : Rouge (mauvais) -> Jaune -> Vert (bon)
    # vmin/vmax permettent de fixer les bornes pour que le vert commence à 95% par ex.
    # 4. TRIER d'abord le DataFrame
    df_sorted = display_df.sort_values("Avg Wait (min)", ascending=False)

    # 5. APPLIQUER le style ensuite sur le DataFrame trié
    styled_df = df_sorted.style.background_gradient(subset=["Availability %"], cmap="RdYlGn", vmin=70, vmax=100).format(
        precision=1
    )

    # 6. AFFICHER l'objet stylisé
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    st.info(
        "💡 **Avg Wait, Min, Max** are calculated only when the ride is OPERATING. "
        "**Availability** represents the percentage of time the ride was operating "
        "(formula: `(uptime / (downtime + uptime)) * 100)`)."
    )
