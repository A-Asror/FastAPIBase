import datetime as dt
import re
import uuid

from decimal import Decimal, ROUND_DOWN
from types import NoneType
from uuid import UUID

from pydantic import Field, field_validator, model_validator

from conf import settings
from .base import BaseOutSchemaModel, BaseInSchemaModel


__all__ = (
    'UserRegisterSchemaIn',
    'UserRegisterSchemaOut',
    'UserRetrieveSchemaOut',
    'UserUpdateSchemaIn',
    'UserUpdateSchemaOut',
    'UserUpdateUniqueFieldsSchemaIn',
)


class UserRegisterSchemaIn(BaseInSchemaModel):
    username: str
    fullname: str | None
    phone_number: str | None = Field(..., examples=['+998 99 123-45-67'])
    password: str = Field(..., min_length=5)

    @field_validator("username")
    def validate_username(cls, v: str):
        expected_result = re.match(r"^[a-zA-Z0-9_.-]*$", v)
        if (expected_result is None) or (len(v) < settings.USERNAME_MINIMUM_CHARACTERS):
            raise ValueError(f"You can use a-z, 0-9 and ('-', '_', '.'). Minimum {settings.USERNAME_MINIMUM_CHARACTERS} characters")
        return v

    @field_validator("phone_number")
    def validate_phone_number(cls, v: str):
        expected_result = re.sub(r'[^0-9+]', "", v)
        if len(expected_result) != settings.NUMBER_OF_DIGITS_IN_PHONE_NUMBER:
            raise ValueError('filled in incorrectly, Example: +998 99 123-45-67')
        return expected_result


class UserRegisterSchemaOut(BaseOutSchemaModel):
    id: uuid.UUID | None
    username: str | None
    fullname: str | None
    phone_number: str | None
    created_at: dt.datetime | None
    updated_at: dt.datetime | None


class UserRetrieveSchemaOut(BaseOutSchemaModel):
    id: str
    username: str
    fullname: str
    phone_number: str
    created_at: dt.datetime
    updated_at: dt.datetime


class UserUpdateSchemaIn(BaseInSchemaModel):
    fullname: str | None = Field(None)


class UserUpdateUniqueFieldsSchemaIn(BaseInSchemaModel):
    username: str | None = None
    phone_number: str | None = None

    @model_validator(mode="after")
    def validate_existing_data(self):
        if isinstance(self.username, NoneType) and isinstance(self.phone_number, NoneType):
            raise ValueError("As a minimum, you need to send one of the fields")
        return self

    @field_validator("username")
    def validate_username(cls, v: str):
        print("2"*28)
        expected_result = re.match(r"^[a-zA-Z0-9_.-]*$", v)
        if (expected_result is None) or (len(v) < settings.USERNAME_MINIMUM_CHARACTERS):
            raise ValueError(f"You can use a-z, 0-9 and ('-', '_', '.'). Minimum {settings.USERNAME_MINIMUM_CHARACTERS} characters")
        return v

    @field_validator("phone_number")
    def validate_phone_number(cls, v: str):
        expected_result = re.sub(r'[^0-9+]', "", v)
        if len(expected_result) != settings.NUMBER_OF_DIGITS_IN_PHONE_NUMBER:
            raise ValueError('filled in incorrectly, Example: +998 99 123-45-67')
        return expected_result


class UserUpdateSchemaOut(BaseOutSchemaModel):
    id: uuid.UUID
    username: str
    fullname: str
    phone_number: str
    created_at: dt.datetime
    updated_at: dt.datetime
