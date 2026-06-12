from langchain.tools import tool

from app.gmail.service import get_latest_email


@tool
def read_latest_email():
    """
    Read the latest unread email.
    """

    return get_latest_email()