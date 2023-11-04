# import datetime
# import json
# import socket
#
# from starlette.types import ASGIApp, Receive, Scope, Send, Message
# from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, _StreamingResponse as StreamingResponse
# # from starlette.responses import StreamingResponse
# from fastapi import Request
# from src.schemas import ResponseMiddlewareSchema
#
# __all__ = [
#     "GlobalResponseMiddleware",
# ]
#
#
# class GlobalResponseMiddleware(BaseHTTPMiddleware):
#     _headers = None
#
#     # class GlobalResponseMiddleware(BaseHTTPMiddleware):
#     # def __init__(self, app: ASGIApp, dispatch: DispatchFunction = None):
#     #     super().__init__(app, dispatch)
#     #
#     # async def dispatch(self, request: Request, call_next):
#     #     # process the request and get the response
#     #     response: StreamingResponse = await call_next(request)  # type: ignore
#     #     print(response.body)
#     #
#     #     return response
#
#     def __init__(self, app: ASGIApp) -> None:
#         self.app = app
#
#     async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
#         start_time = datetime.datetime.utcnow()
#
#         async def send_wrapper(message: Message) -> None:
#             print(type(message))
#             application_generic_urls = ['/openapi.json', '/docs', '/docs/oauth2-redirect', '/redoc']
#
#             if ((message["type"] == "http.response.body") and len(message["body"]) and not any(
#                     [scope["path"].startswith(endpoint) for endpoint in application_generic_urls]
#             )):
#                 response_body = json.loads(message["body"].decode())
#
#                 end_time = datetime.datetime.utcnow()
#
#
#                 # data = {}
#                 # data["data"] = response_body
#
#                 # data_to_be_sent_to_user = json.dumps(data, default=str).encode("utf-8")
#                 data_to_be_sent_to_user = ResponseMiddlewareSchema(code=200, data=response_body).model_dump_json()
#                 data_to_be_sent_to_user = str(data_to_be_sent_to_user).encode()
#                 # data_to_be_sent_to_user = json.dumps(data_to_be_sent_to_user)
#                 # print(data_to_be_sent_to_user)
#                 # print(type(data_to_be_sent_to_user.encode("utf-8")))
#                 message["body"] = data_to_be_sent_to_user
#             # elif message["type"] == "http.response.start":
#             #     self._headers = message
#             await send(message)
#
#         await self.app(scope, receive, send_wrapper)
