from langgraph.graph import StateGraph
from langgraph.graph import START, END

from .state import AgentState

from .nodes import (
    router_node,
    chat_node,
    read_email_node,
    summarize_email_node,
    show_email_node,
    draft_reply_node,
    send_draft_node,
    approve_send_node
)

builder = StateGraph(AgentState)

builder.add_node("router", router_node)
builder.add_node("chat", chat_node)

builder.add_node("read_email", read_email_node)
builder.add_node("draft_reply", draft_reply_node)
builder.add_node("send_draft", send_draft_node)
builder.add_node("summarize_email", summarize_email_node)
builder.add_node("show_email", show_email_node)
builder.add_node("approve_send",approve_send_node)


def route_decision(state: AgentState):
    return state["route"]

def email_action(state: AgentState):
    return state["route"]

builder.add_edge(START, "router")

builder.add_conditional_edges(
    "router",
    route_decision,
    {
        "summarize": "read_email",
        "show": "read_email",
        "reply": "read_email",
        "send": "send_draft",
        "approve": "approve_send",
        "chat": "chat"
    }
)

builder.add_conditional_edges(
    "read_email",
    email_action,
    {
        "show": "show_email",
        "summarize": "summarize_email",
        "reply": "draft_reply"
    }
)

builder.add_edge("summarize_email", END)
builder.add_edge("show_email", END)
builder.add_edge("draft_reply", END)
builder.add_edge("send_draft", END)
builder.add_edge("approve_send", END)
builder.add_edge("chat", END)

graph = builder.compile()