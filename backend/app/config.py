from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    app_name: str = "DocFeed"
    debug: bool = False

    # GitHub personal access token (optional, raises rate limit from 60 to 5000 req/h)
    github_token: str = ""

    # CORS origins allowed to access the API
    cors_origins: list[str] = ["*"]


@lru_cache
def get_settings() -> Settings:
    return Settings()