import enum


__all__ = [
    "BaseEnum",
    "UserRoles",
]


class BaseEnum(enum.Enum):

    @classmethod
    def get_name_by_value(cls, value: int | str | None):
        try:
            return cls(value).name
        except ValueError:
            raise ValueError("%s not found 'choice value'" % value)

    @classmethod
    def get_choice(cls):
        return [(attr.value, attr.name) for attr in cls]

    @classmethod
    def get_list_values(cls):
        return [attr.value for attr in cls]

    @classmethod
    def get_list_names(cls):
        return [attr.name for attr in cls]

    @classmethod
    def get_max_value(cls):
        return max([attr.value for attr in cls])

    @classmethod
    def get_min_value(cls):
        return min([attr.value for attr in cls])


class UserRoles(BaseEnum):
    admin = "admin"
    manager = "manager"
    staff = "staff"
    user = "user"
