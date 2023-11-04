import datetime as dt
import typing
import uuid

import sqlalchemy as sa

from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import DeclarativeBase, Mapped as SQLAlchemyMapped, mapped_column as column


__all__ = ["Base"]


class DBTable(DeclarativeBase):
    metadata: sa.MetaData = sa.MetaData()


class Base(DBTable):
    __abstract__ = True

    id: SQLAlchemyMapped[uuid.UUID] = column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: SQLAlchemyMapped[dt.datetime] = column(sa.DateTime(timezone=True), default=dt.datetime.utcnow)
    updated_at: SQLAlchemyMapped[dt.datetime] = column(
        sa.DateTime(timezone=True), default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow
    )

    @classmethod
    def get_alembic_base_declarative(cls) -> typing.Type[DeclarativeBase]:
        return DBTable

    @classmethod
    def str_to_uuid(cls, pk: str):
        return uuid.UUID(pk)
