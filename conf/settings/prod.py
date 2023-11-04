import datetime as dt
import logging
import pathlib

from decouple import Config, RepositoryEnv
import pydantic
import pydantic_settings

ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.resolve()


decouple = Config(RepositoryEnv(r"%s\%s" % (ROOT_DIR, ".prod.env")))


class BackendProdSettings(pydantic_settings.BaseSettings):

    # Project
    TITLE: str = "Base FastAPI Project"
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
    LOGGING_LEVEL: int = logging.INFO

    # Redis
    REDIS_HOST: str = decouple.get("REDIS_HOST", cast=str)
    REDIS_PORT: int = decouple.get("REDIS_PORT", cast=int)
    REDIS_PASSWORD: str = decouple.get("REDIS_PASSWORD", cast=str)
    REDIS_TIMEOUT: int = decouple.get("REDIS_TIMEOUT", cast=int)  # seconds
    REDIS_BASE_KEY: str = decouple.get("REDIS_BASE_KEY", cast=str)
    REDIS_DB: int = decouple.get("REDIS_DB", cast=int)

    class Config(pydantic.BaseConfig):
        case_sensitive: bool = True
        validate_assignment: bool = True
