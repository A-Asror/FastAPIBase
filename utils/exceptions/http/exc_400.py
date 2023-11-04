import fastapi

from utils.messages import (
    http_400_email_details,
    http_400_sigin_credentials_details,
    http_400_signup_credentials_details,
    http_400_username_details,
)


async def http_exc_400_phone_number_or_username_allow_exists(phone_number: str = None, username: str = None) -> Exception:

    status_code = fastapi.status.HTTP_400_BAD_REQUEST

    if isinstance(phone_number, str) and isinstance(username, str):
        loc = ("body", "phoneNumber", "username")
        details = f"this phone number: '{phone_number}' or username: '{username}' already exists"
    elif isinstance(phone_number, str):
        loc = ("body", "phoneNumber")
        details = f"this phone number: '{phone_number}' already exists"
    elif isinstance(username, str):
        loc = ("body", "username")
        details = f"this username: '{username}' already exists"
    else:
        loc = ()
        details = f"Not Handled Error"
        status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR

    return fastapi.HTTPException(status_code=status_code, detail={"detail": details, "loc": loc})


async def http_400_exc_bad_username_request(username: str) -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=http_400_username_details(username=username),
    )


async def http_400_exc_bad_email_request(email: str) -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=http_400_email_details(email=email),
    )


async def http_400_question_request_details() -> str:
    return "Received incorrect data from external services in response"
