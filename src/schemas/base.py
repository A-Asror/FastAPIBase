import datetime
import typing

from pydantic import BaseModel, BaseConfig, Extra

from utils.formatters.datetime_formatter import format_datetime_into_isoformat
from utils.formatters.field_formatter import format_dict_key_to_camel_case


__all__ = ['BaseOutSchemaModel', 'BaseInSchemaModel']


class BaseOutSchemaModel(BaseModel):

    class Config(BaseConfig):
        from_attributes: bool = True
        validate_assignment: bool = True
        populate_by_name: bool = True
        json_encoders: dict = {datetime.datetime: format_datetime_into_isoformat}
        alias_generator: typing.Any = format_dict_key_to_camel_case


class BaseInSchemaModel(BaseModel):

    class Config(BaseConfig):
        extra = Extra.forbid
        populate_by_name: bool = True
        json_encoders: dict = {datetime.datetime: format_datetime_into_isoformat}
        alias_generator: typing.Any = format_dict_key_to_camel_case
