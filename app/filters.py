# MIT License
# Copyright (c) 2026 Romathi

import pandas as pd


def get_filters(st, df: pd.DataFrame):
    st.sidebar.header("Filters")
    parcs_dispos = df["park_name"].unique()
    selected_park = st.sidebar.multiselect("Parks", parcs_dispos, default=parcs_dispos)

    filtered_df = df[df["park_name"].isin(selected_park)]
    return selected_park, filtered_df
