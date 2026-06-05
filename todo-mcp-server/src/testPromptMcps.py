import asyncio
from fastmcp import FastMCP

mcp = FastMCP("Test")


@mcp.prompt
def hello():
    return "Hello from prompt"


async def main():
    prompts = await mcp.list_prompts()
    print(prompts)


asyncio.run(main())