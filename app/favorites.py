from tools.sql_lite import toggle_favorite


def manage_favorites_ui(st, df, db_name):

    # 1. Initialiser la clé dans le session_state si elle n'existe pas
    if "main_show_only_toggle" not in st.session_state:
        st.session_state["main_show_only_toggle"] = False

    show_only = st.sidebar.toggle("Show only favorites", key="main_show_only_toggle")

    st.sidebar.header("⭐ My Favorites")

    # Récupérer la liste des attractions et leur statut
    attr_status = df.groupby("attraction_name")["is_favorite"].last().to_dict()
    all_attr = sorted(df["attraction_name"].unique())

    with st.sidebar.expander("Configure Favorites"):
        for attr in all_attr:
            is_fav = bool(attr_status.get(attr, 0))
            # On utilise une clé unique pour chaque checkbox
            new_status = st.checkbox(attr, value=is_fav, key=f"fav_{attr}")

            if new_status != is_fav:
                toggle_favorite(db_name, attr, new_status)
                # On ne touche pas au toggle ici, st.rerun() va préserver
                # la valeur de main_show_only_toggle car elle a une clé fixe
                st.rerun()

    # 2. Utiliser la clé (key) sans l'argument 'value' pour laisser Streamlit gérer la persistance

    return show_only
