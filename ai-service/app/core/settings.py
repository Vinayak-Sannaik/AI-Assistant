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
    gemini_api_key: str
    gemini_model: str

    def __init__(self) -> None:
        self.gemini_api_key = getenv("GEMINI_API_KEY") or getenv("GOOGLE_API_KEY") or ""
        self.gemini_model = getenv("GEMINI_MODEL", "gemini-2.5-flash")
 

@lru_cache
def get_settings() -> Settings:
    return Settings()
