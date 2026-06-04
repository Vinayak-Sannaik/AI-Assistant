import asyncio

from app.mcp.git_client import (
    GitMcpClient,
)


async def main():

    client = GitMcpClient()

    result = await (
        client.git_status()
    )

    print(result)


asyncio.run(
    main()
)