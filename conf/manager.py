import enum
import pathlib

from functools import lru_cache

import decouple

from .settings.dev import BackendDevSettings
from .settings.prod import BackendProdSettings


__all__ = ['settings']


class Environment(str, enum.Enum):
    PRODUCTION: str = "PROD"
    DEVELOPMENT: str = "DEV"


class BackendSettingsFactory:
    def __init__(self, environment: str):
        self.environment = environment

    def __call__(self) -> BackendDevSettings | BackendProdSettings:
        if self.environment == Environment.DEVELOPMENT.value:
            return BackendDevSettings()
        return BackendProdSettings()


@lru_cache()
def get_settings() -> BackendDevSettings | BackendProdSettings:
    return BackendSettingsFactory(environment=decouple.config("ENVIRONMENT", default="DEV", cast=str))()  # type: ignore


settings: BackendDevSettings | BackendProdSettings = get_settings()
