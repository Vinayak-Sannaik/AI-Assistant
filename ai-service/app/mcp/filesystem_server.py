from mcp.server.fastmcp import FastMCP
from app.tools.filesystem import read_file_tool, list_files_tool

mcp = FastMCP("filesystem")
from pathlib import Path

@mcp.tool()
def read_file(path: str) -> dict:
    return read_file_tool(path)
    # return {
    #     "type": str(type(path)),
    #     "value": path,
    # }

@mcp.tool()
def list_files(
    path: str,
) -> dict:
    return list_files_tool(path)

if __name__ == "__main__":
    mcp.run()