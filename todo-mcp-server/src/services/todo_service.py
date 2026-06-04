from repositories.todo_repository import TodoRepository


class TodoService:

    def __init__(self, repository: TodoRepository):
        self.repository = repository

    def get_all_todos(self) -> list:
        return self.repository.get_all()
    
    def get_todo(self, todo_id: int) -> dict:
        todos = self.repository.get_all()
        for todo in todos:
            if todo.get("id") == todo_id:
                return todo
        return {"error": f"Todo with id {todo_id} not found"}
    
    def create_todo(
        self,
        title: str,
        description: str = ""
    ) -> dict:
        todos = self.repository.get_all()

        next_id = 1

        if todos:
            next_id = max(todo["id"] for todo in todos) + 1

        todo = {
            "id": next_id,
            "title": title,
            "description": description
        }

        return self.repository.create(todo)
    
    def update_todo(
        self,
        todo_id: int,
        title: str,
        description: str
    ) -> dict:
        todo = self.repository.get_by_id(todo_id)

        if not todo:
            raise ValueError(f"Todo with id {todo_id} not found")

        todo["title"] = title
        todo["description"] = description

        return self.repository.update(todo)
    
    def delete_todo(self, todo_id: int) -> None:
        todo = self.repository.get_by_id(todo_id)

        if not todo:
            raise ValueError(f"Todo with id {todo_id} not found")

        self.repository.delete(todo_id)