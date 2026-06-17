from services.vector_store import similarity_search


def retrieve(query: str):

    docs = similarity_search(query)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    return context, docs