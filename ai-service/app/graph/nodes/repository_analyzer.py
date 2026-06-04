from app.graph.state import (
    AgenticRagState,
)
from app.mcp.filesystem_client import (
    FilesystemMcpClient,
)


async def repository_analyzer_node(
    state: AgenticRagState,
) -> AgenticRagState:

    print(
        "REPOSITORY ANALYZER NODE",
        state,
    )

    client = FilesystemMcpClient()

    #
    # Discover root files
    #

    result = await client.list_files(
        ".",
    )

    files = result.get(
        "files",
        [],
    )

    directories = [
        file["name"]
        for file in files
        if file["type"] == "directory"
    ]

    app_structure = {}

    if "app" in directories:

        app_result = await (
            client.list_files(
                "app"
            )
        )

        app_structure = app_result

    architecture_components = []

    app_dirs = [
        item["name"]
        for item in app_structure["files"]
        if item["type"] == "directory"
    ]

    if "api" in app_dirs:
        architecture_components.append(
            "API Layer"
        )

    if "graph" in app_dirs:
        architecture_components.append(
            "Workflow Orchestration Layer"
        )

    if "mcp" in app_dirs:
        architecture_components.append(
            "MCP Integration Layer"
        )

    if "services" in app_dirs:
        architecture_components.append(
            "Business Logic Layer"
        )

    if "tools" in app_dirs:
        architecture_components.append(
            "Tool Execution Layer"
        )

    #
    # Important repository files
    #

    important_files = []

    for file in files:

        if file["name"] in [
            "README.md",
            "requirements.txt",
            "package.json",
            "docker-compose.yml",
            "pom.xml",
            "build.gradle",
            "go.mod",
            "Cargo.toml",
        ]:

            important_files.append(
                file["name"]
            )

    #
    # Read important files
    #

    important_file_contents = {}

    for file_name in important_files:

        try:

            content = await (
                client.read_file(
                    file_name,
                )
            )

            if content.get(
                "success",
            ):

                important_file_contents[
                    file_name
                ] = content.get(
                    "content",
                    "",
                )

        except Exception as error:

            print(
                f"Failed to read {file_name}: {error}"
            )

    #
    # Build repository context
    #

    repository_context = {
        "root_files": [
            file["name"]
            for file in files
        ],
        "important_files":
            important_files,
        "important_file_contents":
            important_file_contents,

        "app_structure":
            app_structure,

        "architecture_components":
            architecture_components,
    }

    return {
        **state,
        "repository_context":
            repository_context,
        "workflow_events": [
            *state.get(
                "workflow_events",
                [],
            ),
            {
                "node":
                    "repository_analyzer",
                "status":
                    "completed",
            },
        ],
    }