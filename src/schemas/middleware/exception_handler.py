from pydantic import BaseModel


__all__ = [
    "RequestValidationErrorSchema",
]


class RequestValidationErrorSchema(BaseModel):
    message: str
    loc: tuple
