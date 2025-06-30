import sqlite3

def init_db():
    conn = sqlite3.connect("voice_data.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS voice_data (
            user_id TEXT PRIMARY KEY,
            total_minutes INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def add_voice_minutes(user_id, minutes):
    conn = sqlite3.connect("voice_data.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO voice_data (user_id, total_minutes)
        VALUES (?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET total_minutes = total_minutes + ?
    """, (user_id, minutes, minutes))
    conn.commit()
    conn.close()

def get_voice_minutes(user_id):
    conn = sqlite3.connect("voice_data.db")
    c = conn.cursor()
    c.execute("SELECT total_minutes FROM voice_data WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0
