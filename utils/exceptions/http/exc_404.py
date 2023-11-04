"""
The HTTP 404 Not Found response status code indicates that the server cannot find the requested resource.
"""

from typing import Any

import fastapi

from repository.table import Base
from utils.messages import (
    http_404_email_details,
    http_404_username_details,
)


async def http_404_exc_email_not_found_request(email: str) -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_email_details(email=email),
    )


async def http_404_exc_id_not_found_request() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail={"detail": "User doesn't exist, has been deleted, or you are not authorized!", "loc": ("queryParams", "uuid")}
    )


async def http_404_exc_username_not_found_request(username: str) -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_username_details(username=username),
    )
