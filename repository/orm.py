import sqlalchemy as sa


__all__ = [
    'filter_or_dict_to_object',
]


def filter_or_dict_to_object(cls, payload: dict):
    return sa.or_(*[getattr(cls, attr) == value for attr, value in payload.items()])
