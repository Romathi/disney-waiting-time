# MIT License
# Copyright (c) 2026 Romathi

import pandas as pd


def get_key_numbers(st, df: pd.DataFrame, open_attractions: pd.DataFrame):
    """Generate the key numbers of the dashboard.

    Args:
        st (Streamlit): Streamlit object.
        df (pd.DataFrame): DataFrame containing the data.
        open_attractions (pd.DataFrame): DataFrame containing the open attractions.

    Returns:
        None
    """
    col1, col2, col3 = st.columns(3)

    col1.metric("Attractions", len(df["attraction_name"].unique()))

    if not open_attractions.empty:
        col2.metric("Global mean time", f"{int(open_attractions['wait_time'].mean())} min")

        # In case the write action did not happen at the exact same time, we take the latest timestamp.
        latest_ts = open_attractions["timestamp"].max()

        # Get a 10 seconds margin to be sure to group all the last "poll".
        current_batch = open_attractions[open_attractions["timestamp"] >= (latest_ts - pd.Timedelta(seconds=10))]

        current_max = current_batch.sort_values("wait_time", ascending=False)

        if not current_max.empty:
            top_name = current_max.iloc[0]["attraction_name"]
            top_wait = current_max.iloc[0]["wait_time"]
            col3.metric("Actual record", f"{int(top_wait)} min", top_name, delta_color="inverse")
    else:
        col2.metric("Globale Mean Time", "0 min")
        col3.metric("Actual Record", "N/A")
