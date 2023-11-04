import datetime as dt
import logging
import pathlib

from decouple import Config, RepositoryEnv
import pydantic
import pydantic_settings

ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.resolve()

decouple = Config(RepositoryEnv(r"%s\%s" % (ROOT_DIR, ".dev.env")))


class BackendDevSettings(pydantic_settings.BaseSettings):

    # Project
    TITLE: str = "FastAPI Base Project"
    DESCRIPTION: str = "FastAPI Base Project Description"
    VERSION: str = "0.1.0"
    TIMEZONE: str = "UTC"
    DEBUG: bool = True
    API_PREFIX: str = "/api"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    OPENAPI_PREFIX: str = ""
    HOST: str = decouple.get("HOST", cast=str)
    PORT: int = decouple.get("PORT", cast=int)
    WORKERS: int = decouple.get("WORKERS", cast=int)
    ALLOWED_CREDENTIALS: bool = decouple.get("ALLOWED_CREDENTIALS", cast=bool)
    ALLOWED_ORIGINS: list = decouple.get("ALLOWED_ORIGINS", cast=str).split(",")
    ALLOWED_METHODS: str = decouple.get("ALLOWED_METHODS", cast=str)
    ALLOWED_HEADERS: str = decouple.get("ALLOWED_HEADERS", cast=str)
    SECRET_KEY: str = decouple.get("SECRET_KEY", cast=str)
    ALGORITHM: str = decouple.get("ALGORITHM", cast=str)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = decouple.get("REFRESH_TOKEN_EXPIRE_MINUTES", cast=int)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = decouple.get("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
    CRYPT_CONTEXT_SCHEMA: str = decouple.get("CRYPT_CONTEXT_SCHEMA", cast=str)
    LOGGING_LEVEL: int = logging.INFO

    # User App
    USERNAME_MINIMUM_CHARACTERS: int = decouple.get("USERNAME_MINIMUM_CHARACTERS", cast=int)
    NUMBER_OF_DIGITS_IN_PHONE_NUMBER: int = decouple.get("NUMBER_OF_DIGITS_IN_PHONE_NUMBER", cast=int)

    # Redis
    REDIS_HOST: str = decouple.get("REDIS_HOST", cast=str)
    REDIS_PORT: int = decouple.get("REDIS_PORT", cast=int)
    REDIS_PASSWORD: str = decouple.get("REDIS_PASSWORD", cast=str)
    REDIS_TIMEOUT: int = decouple.get("REDIS_TIMEOUT", cast=int)  # seconds
    REDIS_BASE_KEY: str = decouple.get("REDIS_BASE_KEY", cast=str)
    REDIS_DB: int = decouple.get("REDIS_DB", cast=int)

    # Postgres
    POSTGRES_USER: str = decouple.get("DB_POSTGRES_USER", cast=str)
    POSTGRES_HOST: str = decouple.get("DB_POSTGRES_HOST", cast=str)
    POSTGRES_PORT: int = decouple.get("DB_POSTGRES_PORT", cast=int)
    POSTGRES_NAME: str = decouple.get("DB_POSTGRES_NAME", cast=str)
    POSTGRES_PASSWORD: str = decouple.get("DB_POSTGRES_PASSWORD", cast=str)
    POSTGRES_SCHEMA: str = decouple.get("DB_POSTGRES_SCHEMA", cast=str)
    POSTGRES_URI: str = f'{POSTGRES_SCHEMA}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}'

    # SQLAlchemy
    DB_MAX_POOL_CON: int = decouple.get("DB_MAX_POOL_CON", cast=int)
    DB_POOL_SIZE: int = decouple.get("DB_POOL_SIZE", cast=int)
    DB_MAX_OVERFLOW: int = decouple.get("DB_MAX_OVERFLOW", cast=int)
    DB_TIMEOUT: int = decouple.get("DB_TIMEOUT", cast=int)
    DB_ECHO_LOG: bool = decouple.get("DB_ECHO_LOG", cast=bool)
    DB_EXPIRE_ON_COMMIT: bool = decouple.get("DB_EXPIRE_ON_COMMIT", cast=bool)
    DB_FORCE_ROLLBACK: bool = decouple.get("DB_FORCE_ROLLBACK", cast=bool)

    class Config(pydantic.BaseConfig):
        case_sensitive: bool = True
        validate_assignment: bool = True

    @property
    def set_backend_app_attributes(self) -> dict:
        return {
            "title": self.TITLE,
            "version": self.VERSION,
            "debug": self.DEBUG,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "api_prefix": self.API_PREFIX,
        }
