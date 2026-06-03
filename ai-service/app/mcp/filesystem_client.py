import json
import sys
from pathlib import Path

from mcp import ClientSession
from mcp.client.stdio import (
    stdio_client,
    StdioServerParameters,
)


class FilesystemMcpClient:

    async def read_file(
        self,
        path: str,
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
                    "app.mcp.filesystem_server",
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
                        "read_file",
                        {
                            "path": path,
                        },
                    )
                )

                return json.loads(
                    result.content[0].text
                )