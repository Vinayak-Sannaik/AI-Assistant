# Purpose: same as config in nestjs, to manage all settings related to the app in one place. This includes
# environment variables,
# app config,
# shared settings,
# constants.
from functools import lru_cache
from os import getenv
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


class Settings:
    llm_provider: str = ""
    gemini_api_key: str = ""
    gemini_model: str = ""
    deepseek_api_key: str = ""
    deepseek_model: str = ""
    groq_api_key: str = ""
    groq_model: str = ""
    debug: bool = False

    def __init__(self) -> None:

        # PROVIDER
        self.llm_provider = getenv(
            "LLM_PROVIDER",
            "gemini",
        ).lower()

        # VALIDATE PROVIDER
        supported = [
            "gemini",
            "deepseek",
            "groq",
        ]

        if self.llm_provider not in supported:

            raise ValueError(
                (
                    "Unsupported "
                    "LLM provider."
                )
            )

        # GEMINI
        self.gemini_api_key = getenv(
            "GEMINI_API_KEY",
            "",
        )

        self.gemini_model = getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash",
        )

        # DEEPSEEK
        self.deepseek_api_key = getenv(
            "DEEPSEEK_API_KEY",
            "",
        )

        self.deepseek_model = getenv(
            "DEEPSEEK_MODEL",
            "deepseek-chat",
        )

        # GROQ
        self.groq_api_key = getenv(
            "GROQ_API_KEY",
            "",
        )

        self.groq_model = getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile",
        )

        # DEBUG
        self.debug = (
            getenv(
                "DEBUG",
                "false",
            ).lower()
            == "true"
        )


# CACHED SETTINGS INSTANCE
@lru_cache
def get_settings() -> Settings:
    return Settings()