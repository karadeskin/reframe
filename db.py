import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "reframe.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS journal_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        entry_text TEXT NOT NULL,
        sentiment_label TEXT,
        sentiment_score REAL,
        mood TEXT,
        shared_id TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mood_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        mood TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()