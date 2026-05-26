from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)

from langchain_openai import (
    ChatOpenAI,
)

from langchain_groq import ChatGroq

from app.core.settings import (
    get_settings,
)

settings = get_settings()


def get_llm():

    #
    # GEMINI
    #

    if settings.llm_provider == "gemini":

        return ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=(
                settings.gemini_api_key
            ),
            temperature=0,
            max_retries=0,
        )

    #
    # DEEPSEEK
    #

    elif settings.llm_provider == "deepseek":

        return ChatOpenAI(
            model=settings.deepseek_model,
            api_key=(
                settings.deepseek_api_key
            ),
            base_url=(
                "https://api.deepseek.com"
            ),
            temperature=0,
            max_retries=0,
        )
    
    elif settings.llm_provider == "groq":

        return ChatGroq(
            model=settings.groq_model,
            api_key=settings.groq_api_key,
            temperature=0,
            max_retries=0,
        )

    #
    # INVALID
    #

    raise ValueError(
        "Invalid LLM provider."
    )

try:

    llm = get_llm()

except Exception:

    llm = None