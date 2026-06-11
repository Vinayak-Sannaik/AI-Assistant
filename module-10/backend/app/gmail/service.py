from app.gmail.auth import get_gmail_service
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

def get_latest_email():

    service = get_gmail_service()

    results = (
        service.users()
        .messages()
        .list(
            userId="me",
            labelIds=["UNREAD"],
            maxResults=1
        )
        .execute()
    )

    messages = results.get("messages", [])

    if not messages:
        return {
            "message": "No unread emails"
        }

    message_id = messages[0]["id"]

    message = (
        service.users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format="full"
        )
        .execute()
    )

    headers = message["payload"]["headers"]

    def get_header(name):
        return next(
            (h["value"] for h in headers if h["name"].lower() == name.lower()),
            None
        )

    return {
        "subject": get_header("Subject"),
        "sender": get_header("From"),
        "snippet": message.get("snippet", "")
    }

def summarize_latest_email():
    email = get_latest_email()

    prompt = f"""
Summarize this email:

Subject: {email["subject"]}

Content:
{email["snippet"]}
"""

    response = llm.invoke(prompt)

    return response.content