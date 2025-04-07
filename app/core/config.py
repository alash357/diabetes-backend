# app/core/config.py

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Email settings
    email_from: str
    sendgrid_api_key: str
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str

    frontend_url: str = "http://localhost:5173"
    debug: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
