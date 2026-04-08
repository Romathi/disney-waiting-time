# MIT License
# Copyright (c) 2026 Romathi

import pandas as pd
import plotly.express as px


def get_graphs(st, df: pd.DataFrame) -> None:
    """Generates the graphs for the dashboard.

    Args:
        st (Streamlit): Streamlit object.
        df (pd.DataFrame): DataFrame containing the data to display.

    Returns:
        None
    """
    st.subheader("📈 Temporal evolution")

    all_attractions = sorted(df[df["wait_time"].notna()]["attraction_name"].unique())
    target = st.selectbox("Select an attraction to display its historical data", all_attractions)

    attr_df = df[df["attraction_name"] == target]
    fig = px.line(
        attr_df,
        x="timestamp",
        y="wait_time",
        title=f"History : {target}",
        labels={"wait_time": "Minutes", "timestamp": "Hour"},
        color_discrete_sequence=["#00d4ff"],
        # FORCE l'affichage des données au survol
        hover_data={"timestamp": "|%H:%M", "wait_time": True},
        markers=True,  # Optionnel : aide à survoler des points précis
    )

    # Améliore le comportement de l'étiquette (tooltip)
    fig.update_traces(mode="lines+markers")
    fig.update_layout(hovermode="x unified")  # Affiche une barre verticale au survol

    st.plotly_chart(fig, use_container_width=True)
