from app.gmail.service import get_latest_email
from .state import AgentState
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)


words = [
    "summarize",
    "summary",
    "content"
]

def router_node(state: AgentState):

    message = state["message"].lower()

    if any(word in message for word in words):
        return {
            "route": "summarize"
        }
    
    if "show" in message:
        return {
            "route": "show"
        }

    return {
        "route": "chat"
    }

def summarize_email_node(state: AgentState):

    email = state["email"]

    prompt = f"""
    Summarize this email.

    Subject: {email['subject']}

    Content:
    {email['snippet']}
    """

    response = llm.invoke(prompt)

    return {
        "response": response.content
    }




def read_email_node(state: AgentState):

    email = get_latest_email()

    return {
        "email": email
    }

def chat_node(state):
    response = llm.invoke(state["message"])

    return {
        "response": response.content
    }

def show_email_node(state: AgentState):

    email = state["email"]

    return {
        "response": f"""
Subject: {email['subject']}

From: {email['sender']}

Content:
{email['snippet']}
"""
    }