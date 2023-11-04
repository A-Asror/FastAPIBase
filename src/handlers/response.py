import json

from fastapi import Request, status

from fastapi.responses import JSONResponse

from starlette.middleware.base import _StreamingResponse
from starlette.concurrency import iterate_in_threadpool

from conf import settings
from src.schemas import ResponseMiddlewareSchema, RequestValidationErrorSchema

__all__ = ['update_response_schema']


async def update_response_schema(request: Request, call_next):
    # check request not for docs api
    request_url = str(request.url)
    for path in [settings.DOCS_URL, settings.OPENAPI_URL, settings.REDOC_URL, '/docs/oauth2-redirect']:
        application_generic_urls = True if path not in request_url else None
        if application_generic_urls is None:
            break

    response: _StreamingResponse = await call_next(request)
    # process_time = dt.datetime.utcnow()  # end_time

    if application_generic_urls:

        response_body_decode = await get_response_body_decode(response=response)

        if response.status_code in (status.HTTP_200_OK, status.HTTP_201_CREATED):
            response_data = await get_status_20x(request, response, response_body_decode)
        elif response.status_code in (status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND):
            response_data = await get_status_400(request, response, response_body_decode)
        elif response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            response_data = await get_status_422(request, response, response_body_decode)
        elif response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            response_data = await get_status_500(request, response, response_body_decode)
        else:
            response_data = response_body_decode
        if not isinstance(response_data, dict):
            response.headers.update({"Content-Length": str(len(response_data.model_dump_json()))})
            return JSONResponse(
                content=response_data.model_dump(), status_code=status.HTTP_200_OK, headers=dict(response.headers), media_type=response.media_type
            )

    return response


async def get_response_body_decode(response):
    response_body = [chunk async for chunk in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))
    response_body_decode = json.loads(response_body[0].decode())
    return response_body_decode


async def get_status_20x(request, response, response_body):
    return ResponseMiddlewareSchema(code=response.status_code, data=response_body, method=request.method, url=str(request.url))


async def get_status_400(request, response, response_body):
    return ResponseMiddlewareSchema(code=response.status_code, data=response_body, success=False, method=request.method, url=str(request.url))


async def get_status_422(request, response, response_body):
    errors = []

    for exc in response_body.get("detail", []):
        errors.append(RequestValidationErrorSchema(
            message=exc.get('msg'),
            loc=exc.get('loc'),
        ).model_dump())
    return ResponseMiddlewareSchema(code=response.status_code, data=errors, success=False, method=request.method, url=str(request.url))


async def get_status_500(request, response, response_body):
    return ResponseMiddlewareSchema(code=response.status_code, data=response_body, success=False, method=request.method, url=str(request.url))
