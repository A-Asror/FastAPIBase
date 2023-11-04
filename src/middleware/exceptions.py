from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.exc import IntegrityError
from src.schemas import RequestValidationErrorSchema


__all__ = ['ExceptionHandlerMiddleware']


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except (RequestValidationError, ResponseValidationError) as validation_error:
            errors = []

            for detail in validation_error.errors():
                errors.append(
                    RequestValidationErrorSchema(
                        url=str(request.url),
                        method=request.method,
                        message=detail.get("msg"),
                        loc=detail.get("loc"),
                        code=status.HTTP_400_BAD_REQUEST
                    ).model_dump()
                )
            return JSONResponse(status_code=400, content=errors)

        # except IntegrityError as exc:
        #     print(exc)
        #     return JSONResponse(status_code=500, content="exc")

        except Exception as e:
            print(e)
            content = RequestValidationErrorSchema(
                url=str(request.url),
                method=request.method,
                message="Internal Server Error. An unexpected error occurred.",
                loc=(),
                code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).model_dump()

            return JSONResponse(status_code=500, content=content)
