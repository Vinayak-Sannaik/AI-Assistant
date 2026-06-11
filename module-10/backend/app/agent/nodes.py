from app.gmail.service import get_latest_email
from .state import AgentState
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import app.store.draft_store as draft_store


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
    
    if "reply" in message:
        return {
            "route": "reply"
        }
    
    if "send" in message:
        return {
            "route": "send"
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


def draft_reply_node(state: AgentState):

    email = state["email"]

    prompt = f"""
        Write ONLY the email body.

        Do not include:
        - Subject line
        - To field
        - From field

        Original Email Subject:
        {email["subject"]}

        Email Content:
        {email["snippet"]}
        """

    response = llm.invoke(prompt)

    draft = {
        "to": email["sender"],
        "subject": f"Re: {email['subject']}",
        "body": response.content
    }

    draft_store.current_draft = draft

    return {
        "draft": draft
    }


def send_draft_node(state: AgentState):

    if not draft_store.current_draft:
        return {
            "response": "No draft available to send."
        }

    draft = draft_store.current_draft

    return {
        "response": f"""
        To: {draft['to']}

        Subject: {draft['subject']}

        Body:
        {draft['body']}
        """
    }

