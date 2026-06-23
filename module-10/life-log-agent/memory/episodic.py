import sqlite3

DB_PATH = "memory/database.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            assistant_message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_conversation(
    user_message: str,
    assistant_message: str,
):
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO conversations (
            user_message,
            assistant_message
        )
        VALUES (?, ?)
        """,
        (
            user_message,
            assistant_message,
        )
    )

    conn.commit()
    conn.close()


def get_recent_conversations(
    limit: int = 5,
):
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            user_message,
            assistant_message
        FROM conversations
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )

    rows = cursor.fetchall()

    conn.close()

    # Reverse because we selected newest first
    return rows[::-1]

def get_conversation_count():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM conversations
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count