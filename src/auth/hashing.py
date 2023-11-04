from datetime import datetime, timedelta
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from conf import settings

__all__ = ("pwd_context", "get_password_hash")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


@lru_cache
def get_pwd_context() -> CryptContext:
    return CryptContext(schemes=[settings.CRYPT_CONTEXT_SCHEMA], deprecated="auto")


pwd_context: CryptContext = get_pwd_context()
