import asyncio

from app.mcp.filesystem_client import (
    FilesystemMcpClient,
)

# python test_mcp_client.py

async def main():
    client = FilesystemMcpClient()

    result = await client.read_file(
        "app/tools/registry.py",
    )

    print(result)

asyncio.run(main())