import json
import sys
from pathlib import Path

from mcp import ClientSession
from mcp.client.stdio import (
    stdio_client,
    StdioServerParameters,
)


class GitMcpClient:
    async def git_status(
        self,
    ) -> dict:

        project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )

        server_params = (
            StdioServerParameters(
                command=sys.executable,
                args=[
                    "-m",
                    "app.mcp.git_server",
                ],
                cwd=str(
                    project_root,
                ),
            )
        )

        async with stdio_client(
            server_params,
        ) as (
            read_stream,
            write_stream,
        ):

            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:

                await session.initialize()

                result = (
                    await session.call_tool(
                        "git_status",
                        {},
                    )
                )

                return json.loads(
                    result.content[0].text
                )
            
    async def git_log(
        self,
    ) -> dict:

        project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )

        server_params = (
            StdioServerParameters(
                command=sys.executable,
                args=[
                    "-m",
                    "app.mcp.git_server",
                ],
                cwd=str(
                    project_root,
                ),
            )
        )

        async with stdio_client(
            server_params,
        ) as (
            read_stream,
            write_stream,
        ):

            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:

                await session.initialize()

                result = (
                    await session.call_tool(
                        "git_log",
                        {},
                    )
                )

                return json.loads(
                    result.content[0].text
                )