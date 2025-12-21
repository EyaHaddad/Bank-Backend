"""Typed application settings loaded from environment variables and .env.

This module defines the `Settings` model, which centralizes configuration for
the application (e.g., secrets, DB URLs, security policies, SMTP settings). It
relies on `pydantic_settings.BaseSettings` to load and validate values from the
environment or the `.env` file, providing type safety and fail-fast startup if
required fields are missing or malformed.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str
    VERSION: str
    DEBUG: bool = True

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    DATABASE_URL: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    ALLOWED_ORIGINS: List[str]
    ALLOWED_HOSTS: List[str]

    MIN_PASSWORD_LENGTH: int
    MAX_BCRYPT_BYTES: int
    REQUIRE_UPPERCASE: bool
    REQUIRE_LOWERCASE: bool
    REQUIRE_DIGIT: bool
    REQUIRE_SPECIAL_CHAR: bool

    OTP_SECRET_LENGTH: int
    OTP_VALIDITY_PERIOD: int
    OTP_DIGITS: int

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str
    SMTP_FROM_NAME: str
    SMTP_TLS: bool

    MAX_LOGIN_ATTEMPTS: int
    LOGIN_ATTEMPT_WINDOW: int

    USE_SSL: bool
    SESSION_TIMEOUT_MINUTES: int

    MAX_TRANSACTION_AMOUNT: float
    DAILY_TRANSACTION_LIMIT: float

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

    @property
    def db_url(self):
        return f"postgresql://postgres:Postgres%401234%21@localhost:5432/{self.DATABASE_NAME}"


settings = Settings()
