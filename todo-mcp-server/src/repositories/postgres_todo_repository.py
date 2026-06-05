import os
import psycopg
from dotenv import load_dotenv
from repositories.todo_repository import TodoRepository

class PostgresTodoRepository(TodoRepository):

    def __init__(self):
        load_dotenv()

        self.connection = psycopg.connect(
            os.getenv("DATABASE_URL")
        )

    def get_all(self) -> list:
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    title,
                    description,
                    status,
                    priority,
                    tags
                FROM todos
                ORDER BY id
            """)

            rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "status": row[3],
                "priority": row[4],
                "tags": row[5]
            }
            for row in rows
        ]

    def create(self, todo: dict) -> dict:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO todos
                (
                    title,
                    description,
                    status,
                    priority,
                    tags
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    todo["title"],
                    todo["description"],
                    todo["status"],
                    todo["priority"],
                    todo["tags"]
                )
            )

            todo_id = cursor.fetchone()[0]

        self.connection.commit()

        todo["id"] = todo_id

        return todo

    def get_by_id(self, todo_id: int) -> dict | None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    title,
                    description,
                    status,
                    priority,
                    tags
                FROM todos
                WHERE id = %s
                """,
                (todo_id,)
            )

            row = cursor.fetchone()

        if not row:
            return None

        return {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3],
            "priority": row[4],
            "tags": row[5]
        }

    def update(self, todo: dict) -> dict:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE todos
                SET
                    title = %s,
                    description = %s,
                    status = %s,
                    priority = %s,
                    tags = %s
                WHERE id = %s
                """,
                (
                    todo["title"],
                    todo["description"],
                    todo["status"],
                    todo["priority"],
                    todo["tags"],
                    todo["id"]
                )
            )

        self.connection.commit()

        return todo

    def delete(self, todo_id: int) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM todos
                WHERE id = %s
                """,
                (todo_id,)
            )

        self.connection.commit()