from fastmcp import FastMCP
# from repositories.json_todo_repository import JsonTodoRepository
from repositories.postgres_todo_repository import PostgresTodoRepository
from services.todo_service import TodoService

# repository = JsonTodoRepository()
repository = PostgresTodoRepository()
service = TodoService(repository)
mcp = FastMCP("Todo MCP Server")


@mcp.tool
def ping() -> str:
    return "Hi From Me too"

@mcp.tool
def create_todo(
    title: str,
    description: str = "",
    priority: str = "medium",
    tags: list[str] | None = None
) -> dict:
    """
    Create a new todo item and save it permanently.

    Use this tool when the user wants to:
    - create a task
    - add a todo
    - remember something
    - track work

    Args:
        title: Short title of the task.
        description: Additional task details.
        priority: Task priority. Allowed values:
            low, medium, high, critical.

    Returns:
        Created todo including generated id.
    """
    return service.create_todo(
        title=title,
        description=description,
        priority=priority,
        tags=tags
    )

@mcp.tool
def list_todos() -> list:
    """
    Retrieve all existing todo items.

    Use this tool when the user wants to:
    - see all todos
    - list tasks
    - show pending work
    - review current tasks

    Returns:
        List of all stored todos.
    """
    return service.get_all_todos()

@mcp.tool
def get_todo(todo_id: int) -> dict:
    """
    Retrieve a single todo by id.

    Use this tool when the user wants:
    - details of a specific todo
    - information about a task
    - to inspect a todo item

    Args:
        todo_id: Unique todo identifier.

    Returns:
        Matching todo item.
    """
    return service.get_todo(todo_id)

@mcp.tool
def update_todo(
    todo_id: int,
    title: str,
    description: str
) -> dict:
    """
    Update an existing todo.

    Use this tool when the user wants to:
    - edit a task
    - rename a todo
    - change task details

    Args:
        todo_id: Todo identifier.
        title: Updated title.
        description: Updated description.

    Returns:
        Updated todo item.
    """
    return service.update_todo(
        todo_id=todo_id,
        title=title,
        description=description
    )

@mcp.tool
def delete_todo(todo_id: int) -> dict:
    """
    Delete a todo permanently.

    Use this tool when the user wants to:
    - remove a task
    - delete a todo
    - discard a completed item

    Args:
        todo_id: Todo identifier.

    Returns:
        Success confirmation.
    """
    service.delete_todo(todo_id)
    return {
        "success": True,
        "message": f"Todo {todo_id} deleted"
    }

@mcp.tool
def search_todos(
    query: str = "",
    tag: str = ""
) -> list:
    """
    Search todos by text or tag.

    Use this tool only when the user wants to:
    - find specific todos
    - search tasks
    - filter tasks by keyword
    - locate todos by tag

    Args:
        query: Optional text to search in title and description.
        tag: Optional tag filter.

    Returns:
        Matching todo items.
    """
    return service.search_todos(query, tag)

@mcp.resource("resource://todos")
def todos_resource() -> list:
    """
    Read all todos.
    """
    return service.get_all_todos()

@mcp.resource("resource://tags")
def tags_resource() -> list:
    """
    Return all unique tags.
    """
    todos = service.get_all_todos()

    tags = set()

    for todo in todos:
        for tag in todo.get("tags", []):
            tags.add(tag)

    return sorted(list(tags))


@mcp.prompt
def plan_my_day() -> str:
    """
    Generate a daily plan from current todos.
    """

    todos = service.get_all_todos()

    return f"""
    You are a productivity assistant.

    Create a plan for today based on these todos:

    {todos}

    Prioritize high priority items first.
    Group related work together.
    Suggest a realistic order of execution.
    """

@mcp.prompt
def hello_prompt() -> str:
    return "Hello from MCP Prompt"

@mcp.resource("resource://todos/{todo_id}")
def get_todo_resource(todo_id: int) -> dict:
    """
    Get a single todo by id.
    """
    return service.get_todo(todo_id)

@mcp.resource("resource://todos/status/{status}")
def todos_by_status(status: str) -> list:
    todos = service.get_all_todos()

    return [
        todo
        for todo in todos
        if todo.get("status") == status
    ]

@mcp.resource("resource://tags/{tag}")
def todos_by_tag(tag: str) -> list:
    todos = service.get_all_todos()

    return [
        todo
        for todo in todos
        if tag.lower() in [
            t.lower()
            for t in todo.get("tags", [])
        ]
    ]

if __name__ == "__main__":
    print(mcp)
    mcp.run()