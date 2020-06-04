"""Settings for {{ cookiecutter.project_name }} Project."""
import pathlib
import sys
from typing import List

from loguru import logger
from passlib.context import CryptContext
from pydantic import BaseSettings

BASE_DIR = pathlib.Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    """Base settings for {{ cookiecutter.project_name }}."""

    PROJECT_NAME: str = "{{ cookiecutter.project_name }}"

    PROJECT_DESCRIPTION: str = "{{ cookiecutter.description }}"

    DOCS_URL: str = "/docs"

    REDOC_URL: str = "/redoc"

    OPENAPI_URL: str = "/openapi.json"

    ALLOWED_HOSTS: List[str] = ["*"]

    DEBUG: bool

    CORS_ORIGINS: List[str] = ["*"]

    CORS_ALLOW_CREDENTIALS: bool = True

    CORS_ALLOW_METHODS: List[str] = ["*"]

    CORS_ALLOW_HEADERS: List[str] = ["*"]

    DATABASE_URL: str = "sqlite://./db.sqlite3"

    DB_MODELS: List[str] = ["{{ cookiecutter.project_slug }}.users.models"]

    PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    User_MODEL: str = "{{ cookiecutter.project_slug }}.users.models.User"

    class Config:
        """Base Config for Settings."""

        env_file = BASE_DIR.joinpath(".env")


settings = Settings()

logger.add(sys.stderr, format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
