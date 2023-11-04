from pydantic import BaseModel


__all__ = [
    "ResponseMiddlewareSchema",
]


class ResponseMiddlewareSchema(BaseModel):
    url: str
    method: str
    code: int
    success: bool = True
    message: str | None = None
    data: dict | list
