from app.graph.state import AgenticRagState
from app.mcp.filesystem_client import FilesystemMcpClient

ACTION_WORDS = [
    "explain",
    "read",
    "refactor",
    "delete",
    "analyze",
]
def extract_file_path(
    query: str,
) -> str:
    cleaned = query.lower()

    for word in ACTION_WORDS:
        cleaned = cleaned.replace(
            word,
            "",
        )

    return cleaned.strip()

async def retriever_node(
    state: AgenticRagState,
) -> AgenticRagState:
    
    print("Retriever node received state:")
    # print(state)

    retrieved_documents = []
    client = FilesystemMcpClient()

    retrieval_query = state.get(
        "retrieval_query",
        "",
    )

    retrieved_documents = []

    #
    # SIMPLE FILE RETRIEVAL
    #

    if ".py" in retrieval_query:

        file_path = extract_file_path(
            retrieval_query,
        )

        result = await client.read_file(
            file_path,
        )

        if result["success"]:

            retrieved_documents.append(
                {
                    "source": file_path,
                    "content": result["content"],
                }
            )

    return {
        **state,

        "retrieved_documents": (
            retrieved_documents
        ),

        "workflow_events": [
            *state.get(
                "workflow_events",
                [],
            ),
            {
                "node": "retriever",
                "status": "completed",
            },
        ],
    }
