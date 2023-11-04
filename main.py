import uvicorn

from fastapi import Request, FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from conf import settings
from src.api.endpoints import router as api_endpoint_router
from conf.events import execute_backend_server_event_handler, terminate_backend_server_event_handler
from src.middleware import ExceptionHandlerMiddleware
from src.handlers import validation_http_exception_handler, update_response_schema


# from src.celery.settings.celery import celery as celery_app


def initialize_backend_application() -> FastAPI:
    app = FastAPI(**settings.set_backend_app_attributes)  # type: Ignore

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.ALLOWED_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )
    app.add_middleware(ExceptionHandlerMiddleware)
    app.middleware("http")(update_response_schema)

    # Event Handlers
    app.add_event_handler("startup", execute_backend_server_event_handler(backend_app=app))
    app.add_event_handler("shutdown", terminate_backend_server_event_handler(backend_app=app))

    # Routes
    app.include_router(router=api_endpoint_router, prefix=settings.API_PREFIX)

    # Middlewares
    # app.add_middleware(GlobalResponseMiddleware)

    # app.mount('/api/celery', celery_app)

    return app


backend_app: FastAPI = initialize_backend_application()


@backend_app.exception_handler(HTTPException)
async def _validation_http_exception_handler(request: Request, exc: HTTPException):
    return await validation_http_exception_handler(request, exc)


# @backend_app.middleware("http")
# async def _update_response_schema(request: Request, call_next):
#     return await update_response_schema(request, call_next)


if __name__ == "__main__":
    uvicorn.run(
        app="main:backend_app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        # reload=settings.DEBUG,
        workers=settings.WORKERS,
        log_level=settings.LOGGING_LEVEL
    )
