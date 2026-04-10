# MIT License
# Copyright (c) 2026 Romathi

import pandas as pd


def get_detailed_best_picks(st, df: pd.DataFrame):
    st.subheader("📍 What's the best move right now?")

    # 1. Préparation temporelle
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    # Création des tranches de 30 min (ex: 14:00, 14:30)
    df["Slot"] = df["timestamp"].dt.floor("30min").dt.strftime("%H:%M")

    # 2. Calcul des moyennes par Slot et Attraction
    # On filtre les temps > 2 min pour éviter les bugs/fermetures
    stats = df[df["wait_time"] > 2].groupby(["Slot", "attraction_name"])["wait_time"].mean().reset_index()

    # 3. Récupérer la liste des créneaux disponibles pour le picker
    available_slots = sorted(stats["Slot"].unique())

    if not available_slots:
        st.info("No data available for slots yet.")
        return

    # 4. LE PICKER (Le menu déroulant)
    # Par défaut, on sélectionne le dernier créneau enregistré
    selected_slot = st.selectbox("Select a time window:", available_slots, index=len(available_slots) - 1)

    # 5. Filtrer et récupérer le Top 5 pour ce créneau
    top_10 = stats[stats["Slot"] == selected_slot].sort_values("wait_time").head(10)

    # Mise en forme
    top_10.columns = ["Time", "Attraction", "Avg Wait"]
    top_10["Avg Wait"] = top_10["Avg Wait"].map(lambda x: f"{int(x)} min")

    # 6. Affichage propre
    st.write(f"🏆 **Top 10 fastest attractions at {selected_slot}**")

    # On injecte un peu de CSS pour styliser les lignes
    st.markdown(
        """
        <style>
            .stVerticalBlock div[data-testid="stVerticalBlock"] > div:nth-child(odd) {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 5px;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Conteneur pour grouper les lignes et appliquer le style
    with st.container():
        for _, row in top_10.iterrows():
            col_name, col_time = st.columns([3, 1])
            # On ajoute un petit padding interne pour que le texte ne colle pas au bord
            col_name.markdown(f"&nbsp; **{row['Attraction']}**")
            col_time.write(f"⏳ {row['Avg Wait']}")
