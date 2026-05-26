from app.tools.filesystem import (
    read_file_tool,
    list_files_tool,
)

TOOLS = {
    # "read_file": {
    #     "handler": read_file_tool,
    #     "description": "Read file content",
    #     "input_schema": {
    #         "path": "string",
    #     },
    # },
    "read_file": read_file_tool,
    "list_files": list_files_tool,
}