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
        description: str = "",
        priority: str = "medium",
        tags: list[str] | None = None
    ) -> dict:
        allowed_priorities = [
            "low",
            "medium",
            "high",
            "critical"
        ]

        if priority not in allowed_priorities:
            raise ValueError(
                f"Invalid priority. Allowed values: {allowed_priorities}"
            )
        
        if tags is None:
            tags = []

        todos = self.repository.get_all()

        next_id = 1

        if todos:
            next_id = max(todo["id"] for todo in todos) + 1

        todo = {
            "id": next_id,
            "title": title,
            "description": description,
            "status": "pending",
            "priority":priority,
            "tags": tags
        }

        todo =  self.repository.create(todo)
        return {
            "success": True,
            "message": f"Todo created successfully with id {todo['id']}",
            "data": todo
        }
    
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

    def search_todos(self, query: str = "", tag: str = "") -> list:
        todos = self.repository.get_all()

        results = []

        for todo in todos:
            matches_query = (
                not query
                or query.lower() in todo.get("title", "").lower()
                or query.lower() in todo.get("description", "").lower()
            )

            matches_tag = (
                not tag
                or tag.lower() in [t.lower() for t in todo.get("tags", [])]
            )

            if matches_query and matches_tag:
                results.append(todo)

        return results