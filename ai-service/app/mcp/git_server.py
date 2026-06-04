from mcp.server.fastmcp import FastMCP
import subprocess

mcp = FastMCP("git")


@mcp.tool()
def git_status() -> dict:

    result = subprocess.run(
        [
            "git",
            "status",
            "--short",
        ],
        capture_output=True,
        text=True,
    )

    return {
        "success": True,
        "output": result.stdout,
    }

@mcp.tool()
def git_log() -> dict:

    result = subprocess.run(
        [
            "git",
            "log",
            "--oneline",
            "-10",
        ],
        capture_output=True,
        text=True,
    )

    return {
        "success": True,
        "output": result.stdout,
    }

if __name__ == "__main__":
    mcp.run()