import datetime as dt
from jose import JWTError, jwt

from conf import settings


__all__ = (
    'create_token',
)


def create_token(data: dict, exp: int):
    to_encode = data.copy()
    expire = dt.datetime.utcnow() + dt.timedelta(minutes=exp)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_user():
    pass
