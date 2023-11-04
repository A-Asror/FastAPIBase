from fastapi import Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from src.schemas import RequestValidationErrorSchema


__all__ = ["validation_http_exception_handler"]


async def validation_http_exception_handler(request: Request, http_exception: HTTPException):
    content = RequestValidationErrorSchema(
                url=str(request.url),
                method=request.method,
                message=http_exception.detail.get('detail'),
                loc=http_exception.detail.get('loc'),
            ).model_dump()
    return JSONResponse(status_code=400, content=content)
