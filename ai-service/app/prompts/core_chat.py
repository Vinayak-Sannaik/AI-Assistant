from langchain_core.prompts import ChatPromptTemplate

from app.parsers.engineering_response import engineering_response_parser


CORE_CHAT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI software engineering assistant. Produce practical, structured guidance "
            "for architecture, repository analysis, documentation, and workflow planning requests. "
            "Return only JSON matching the requested schema.\n\n{format_instructions}",
        ),
        ("human", "{query}"),
    ]
).partial(format_instructions=engineering_response_parser.get_format_instructions())
