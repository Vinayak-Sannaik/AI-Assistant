import sqlite3

DB_PATH = "memory/database.db"


def init_semantic_db():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fact TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_fact(fact: str):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO facts(fact)
        VALUES(?)
        """,
        (fact,)
    )

    conn.commit()
    conn.close()


def get_all_facts():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT fact
        FROM facts
    """)

    rows = cursor.fetchall()

    conn.close()

    return [row[0] for row in rows]



def get_fact_by_id(fact_id):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT fact
        FROM facts
        WHERE id=?
        """,
        (
            fact_id + 1,
        ),
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None