import sqlite3

import pandas as pd

DB_NAME = "disney_data.db"


def read_raw_data(limit=10):
    """Lecture simple en utilisant le curseur SQLite (rapide)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print(f"\n--- {limit} dernières entrées enregistrées ---")
    query = "SELECT * FROM wait_times ORDER BY id DESC LIMIT ?"
    cursor.execute(query, (limit,))

    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()


def analyze_with_pandas():
    """Lecture et analyse rapide avec Pandas."""
    conn = sqlite3.connect(DB_NAME)

    # On charge toute la table dans un DataFrame
    df = pd.read_sql_query("SELECT * FROM wait_times", conn)
    conn.close()

    # Conversion du timestamp en objet datetime pour Pandas
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    print("\n--- Aperçu du DataFrame Pandas ---")
    print(df.head())  # Affiche les 5 premières lignes

    print("\n--- Statistiques rapides ---")
    # On filtre uniquement les attractions ouvertes pour la moyenne
    stats = df[df["status"] == "OPERATING"].groupby("attraction_name")["wait_time"].mean().sort_values(ascending=False)
    print("Top 5 des attentes moyennes enregistrées :")
    print(stats.head(5))


if __name__ == "__main__":
    # Vérifie d'abord les données brutes
    read_raw_data(5)

    # Lance l'analyse si tu as déjà fait plusieurs captures
    try:
        analyze_with_pandas()
    except Exception as e:
        print(f"\nPandas n'a pas pu analyser : {e}")
