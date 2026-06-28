import sqlite3
import json
from datetime import datetime

DB_NAME = "wardroai.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id TEXT PRIMARY KEY,
            image_name TEXT,
            style TEXT,
            occasion TEXT,
            confidence INTEGER,
            created_at TEXT,
            data TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_analysis(result):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO analyses
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        result["analysis_id"],
        result["image_name"],
        result["fashion_metadata"]["style"],
        result["fashion_metadata"]["occasion"],
        result["confidence_score"],
        datetime.now().isoformat(),
        json.dumps(result)
    ))

    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, image_name, style, occasion, confidence, created_at
        FROM analyses
        ORDER BY created_at DESC
    """)
    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "image_name": r[1],
            "style": r[2],
            "occasion": r[3],
            "confidence": r[4],
            "created_at": r[5]
        }
        for r in rows
    ]