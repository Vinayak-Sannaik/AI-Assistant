import json
from pathlib import Path

from repositories.todo_repository import TodoRepository


class JsonTodoRepository(TodoRepository):

    def __init__(self):
        # Use absolute path relative to the script location
        script_dir = Path(__file__).parent.parent.parent
        self.file_path = script_dir / "data" / "todos.json"

    def get_all(self) -> list:
        with open(self.file_path, "r") as file:
            return json.load(file)

    def create(self, todo: dict) -> dict:
        todos = self.get_all()
        todos.append(todo)

        with open(self.file_path, "w") as file:
            json.dump(todos, file, indent=2)

        return todo
    
    def get_by_id(self, todo_id: int) -> dict | None:
        todos = self.get_all()

        for todo in todos:
            if todo["id"] == todo_id:
                return todo

        return None
    
    def update(self, updated_todo: dict) -> dict:
        todos = self.get_all()

        for index, todo in enumerate(todos):
            if todo["id"] == updated_todo["id"]:
                todos[index] = updated_todo
                break

        with open(self.file_path, "w") as file:
            json.dump(todos, file, indent=2)

        return updated_todo
    
    def delete(self, todo_id: int) -> None:
        todos = self.get_all()

        todos = [
            todo
            for todo in todos
            if todo["id"] != todo_id
        ]

        with open(self.file_path, "w") as file:
            json.dump(todos, file, indent=2)