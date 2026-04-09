# MIT License
# Copyright (c) 2026 Romathi


import sqlite3
from datetime import UTC, datetime


# -------------------------------------------------------------------
# Database initialization
# -------------------------------------------------------------------
def init_db(db_name: str) -> None:
    """Initialize a database with a table for wait times.
    The primary purpose if to aggregate data for Disneyland Paris.
    The database is created with the following columns:
        - id: An auto-incrementing integer.
        - timestamp: The date and time of the wait time request.
        - park_name: The name of the park.
        - attraction_name: The name of the attraction.
        - wait_time: The wait time in minutes to do the attraction.
        - status: The status of the attraction.
        - last_updated_at: The date and time of the last update.

    Args:
        db_name (str): The name of the database to initialize.

    Return:
        None
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS wait_times (
                                                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                             timestamp DATETIME,
                                                             park_name TEXT,
                                                             attraction_name TEXT,
                                                             wait_time INTEGER,
                                                             status TEXT,
                                                             last_updated_at TEXT
                   )
                   """)
    conn.commit()
    conn.close()


# -------------------------------------------------------------------
# Database connection
# -------------------------------------------------------------------
def get_db_connection(db_name: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_name)
    return conn


def close_db_connection(conn: sqlite3.Connection, commit: bool = True) -> None:
    if commit:
        conn.commit()
    conn.close()


# -------------------------------------------------------------------
# Insert data
# -------------------------------------------------------------------
def insert_data(cursor: sqlite3.Cursor, data_dict: dict[str, dict[str, str]], park_name: str) -> None:
    """Insert data into the database.

    Args:
        cursor (sqlite3.Cursor): Cursor object to execute SQL queries.
        data_dict (dict[str, dict[str, str]]): Dictionary containing data to be inserted.
        park_name (str): Name of the park.

    Returns:
        None
    """
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    for name, values in data_dict.items():
        cursor.execute(
            """
            INSERT INTO wait_times (timestamp, park_name, attraction_name, wait_time, status, last_updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                now,
                park_name,
                name,
                values.get("wait_time"),
                values.get("status"),
                values.get("last_up"),
            ),
        )
