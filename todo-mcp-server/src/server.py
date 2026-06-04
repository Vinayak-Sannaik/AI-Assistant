from fastmcp import FastMCP
from repositories.json_todo_repository import JsonTodoRepository
from services.todo_service import TodoService

repository = JsonTodoRepository()
service = TodoService(repository)
mcp = FastMCP("Todo MCP Server")


@mcp.tool
def ping() -> str:
    return "Vinayak"

@mcp.tool
def add_todo(
    title: str,
    description: str = ""
) -> dict:
    return service.create_todo(
        title=title,
        description=description
    )

@mcp.tool
def list_todos() -> list:
    return service.get_all_todos()

@mcp.tool
def get_todo(todo_id: int) -> dict:
    return service.get_todo(todo_id)

@mcp.tool
def update_todo(
    todo_id: int,
    title: str,
    description: str
) -> dict:
    return service.update_todo(
        todo_id=todo_id,
        title=title,
        description=description
    )

@mcp.tool
def delete_todo(todo_id: int) -> dict:
    service.delete_todo(todo_id)

    return {
        "success": True,
        "message": f"Todo {todo_id} deleted"
    }

if __name__ == "__main__":
    print(mcp)
    mcp.run()