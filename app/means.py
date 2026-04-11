# MIT License
# Copyright (c) 2026 Romathi

import pandas as pd


def get_means(st, df: pd.DataFrame, open_attractions: pd.DataFrame) -> None:
    """Compute and display reliability statistics for attractions.

    Args:
        st: Streamlit object
        df (pd.DataFrame): DataFrame containing attraction data
        open_attractions (pd.DataFrame): DataFrame of currently open attractions

    Returns:
        None
    """
    st.subheader("📊 Reliability & Statistics")

    # 1. Compute reliability (Uptime vs Downtime).
    df["is_down"] = df["status"].apply(lambda x: int(x == "DOWN"))
    df["is_up"] = df["status"].apply(lambda x: int(x == "OPERATING"))

    stats = df.groupby("attraction_name").agg(Down_Events=("is_down", "sum"), Up_Events=("is_up", "sum")).reset_index()

    # Convert in minutes (5 min per observation).
    stats["Downtime (min)"] = stats["Down_Events"] * 5
    stats["Uptime (min)"] = stats["Up_Events"] * 5
    total_obs = stats["Downtime (min)"] + stats["Uptime (min)"]

    # Compute ratio.
    stats["Availability %"] = (stats["Uptime (min)"] / total_obs * 100).fillna(0).round(1)

    # 2. Statistiques de temps (Moyenne, Min, Max)
    time_stats = (
        open_attractions.groupby("attraction_name")
        .agg(Avg_Wait=("wait_time", "mean"), Min=("wait_time", "min"), Max=("wait_time", "max"))
        .reset_index()
    )

    time_stats["Avg_Wait"] = time_stats["Avg_Wait"].round(1)

    # 3. Merge and cleaning.
    final_df = pd.merge(time_stats, stats, on="attraction_name", how="left")

    # Select user columns.
    display_df = final_df[["attraction_name", "Avg_Wait", "Min", "Max", "Availability %"]].copy()

    # Rename for clean display.
    display_df.columns = [
        "Attraction",
        "Avg Wait (min)",
        "Min",
        "Max",
        "Availability %",
    ]

    # 4. Sort by Avg Wait.
    df_sorted = display_df.sort_values("Avg Wait (min)", ascending=False)

    # 5. Display with color gradient.
    # Gradient color are: Red (for bad) to Green (for good).
    # vmin/vmax fix the range of the gradient.
    styled_df = df_sorted.style.background_gradient(subset=["Availability %"], cmap="RdYlGn", vmin=70, vmax=100).format(
        precision=1
    )

    # 6. Display the styled DataFrame.
    st.dataframe(styled_df, width="stretch", hide_index=True)

    st.info(
        "💡 **Avg Wait, Min, Max** are calculated only when the ride is OPERATING. "
        "**Availability** represents the percentage of time the ride was operating "
        "(formula: `(uptime / (downtime + uptime)) * 100)`)."
    )
