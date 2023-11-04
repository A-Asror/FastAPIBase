import uuid

import sqlalchemy as sa
import sqlalchemy.orm as so

from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as column

from repository.base import Base

from .enum import UserRoles

__all__ = [
    'UserTable',
    'UserDeviceTable',
    'TokenTable',
]


class UserTable(Base):
    __tablename__ = "users"
    __mapper_args__ = {'eager_defaults': True}

    username: SQLAlchemyMapped[str] = column(sa.String(length=128), nullable=False, unique=True)
    fullname: SQLAlchemyMapped[str] = column(sa.String(length=128), nullable=True)
    phone_number: SQLAlchemyMapped[str] = column(sa.String(length=13), nullable=True, unique=True)
    is_blocked: SQLAlchemyMapped[bool] = False
    is_active: SQLAlchemyMapped[bool] = True
    password: SQLAlchemyMapped[str]
    role: SQLAlchemyMapped[UserRoles] = UserRoles.user.value

    tokens: SQLAlchemyMapped[list["TokenTable"]] = so.relationship(back_populates="user", cascade="all, delete-orphan", uselist=True)
    devices: SQLAlchemyMapped[list["UserDeviceTable"]] = so.relationship(back_populates="user", cascade="all, delete-orphan", uselist=True)


class UserDeviceTable(Base):
    __tablename__ = "user_devices"

    host: SQLAlchemyMapped[str | None]
    device: SQLAlchemyMapped[str | None]

    user_uuid: SQLAlchemyMapped[uuid.UUID] = column(sa.ForeignKey("users.id"))

    user: SQLAlchemyMapped["UserTable"] = so.relationship(back_populates="devices", uselist=False)
    token: SQLAlchemyMapped["TokenTable"] = so.relationship(back_populates="device", uselist=False)


class TokenTable(Base):
    __tablename__ = "tokens"
    __table_args__ = (sa.UniqueConstraint("device_uuid"),)

    access_token: SQLAlchemyMapped[str]
    refresh_token: SQLAlchemyMapped[str]

    user_uuid: SQLAlchemyMapped[uuid.UUID] = column(sa.ForeignKey("users.id"))
    device_uuid: SQLAlchemyMapped[uuid.UUID] = column(sa.ForeignKey("user_devices.id"))

    user: SQLAlchemyMapped["UserTable"] = so.relationship(back_populates="tokens", uselist=False)
    device: SQLAlchemyMapped["UserDeviceTable"] = so.relationship(back_populates="token", uselist=False)
