from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as so

from sqlalchemy.engine.cursor import CursorResult

from repository import filter_or_dict_to_object
from src.models import UserTable
from src.schemas import UserRegisterSchemaIn, UserUpdateSchemaIn, UserUpdateUniqueFieldsSchemaIn

from utils.exceptions.http import exc_404, exc_400
from src.auth.hashing import get_password_hash
from .base import BaseCRUDRepository

__all__ = [
    'UserCrudRepository',
]


class UserCrudRepository(BaseCRUDRepository):

    async def check_exists_username_or_phone_number(self, username: str, phone_number: str) -> bool:
        stmt = (
            sa.exists(UserTable.id)
            .where(sa.or_(UserTable.username == username, UserTable.phone_number == phone_number))
            .select()
        )

        query = await self.async_session.execute(stmt)
        return query.scalar()

    async def register_user(self, instance: UserRegisterSchemaIn) -> UserTable:

        if await self.check_exists_username_or_phone_number(instance.username, instance.phone_number):
            raise await exc_400.http_exc_400_phone_number_or_username_allow_exists(
                phone_number=instance.phone_number, username=instance.username
            )

        user = UserTable(
            username=instance.username,
            fullname=instance.fullname,
            phone_number=instance.phone_number,
            password=get_password_hash(instance.password),
        )

        self.async_session.add(instance=user)
        await self.async_session.commit()
        await self.async_session.refresh(instance=user)
        return user

    async def retrieve_user(self, uuid: UUID):
        stmt = (
            sa.select(
                UserTable.id,
                UserTable.username,
                UserTable.fullname,
                UserTable.phone_number,
                UserTable.created_at,
                UserTable.updated_at,
            )
            .where(UserTable.id == uuid)
        )
        query = await self.async_session.execute(statement=stmt)
        user = query.one_or_none()

        if not user:
            raise await exc_404.http_404_exc_id_not_found_request()

        return user

    async def update_user_by_id(self, uuid: UUID, payload: UserUpdateSchemaIn):

        stmt = (
            sa.update(UserTable)
            .filter_by(id=uuid)
            .values(**payload.model_dump(exclude_defaults=True))
            .returning(
                UserTable.id,
                UserTable.username,
                UserTable.fullname,
                UserTable.phone_number,
                UserTable.created_at,
                UserTable.updated_at,
            )
        )

        result = await self.async_session.execute(stmt)

        user = result.one_or_none()

        if not user:
            raise await exc_404.http_404_exc_id_not_found_request()

        await self.async_session.commit()

        return user

    async def update_user_unique_fields_by_id(self, uuid: UUID, payload: UserUpdateUniqueFieldsSchemaIn):

        payload_dict = payload.model_dump(exclude_defaults=True)

        stmt_exists_uniq_data = (
            sa.exists(UserTable.id)
            .where(filter_or_dict_to_object(UserTable, payload_dict))
            .select()
        )

        exists_uniq_data = await self.async_session.execute(stmt_exists_uniq_data)

        if exists_uniq_data.scalar():
            raise await exc_400.http_exc_400_phone_number_or_username_allow_exists(**payload_dict)

        stmt = (
            sa.update(UserTable)
            .filter_by(id=uuid)
            .values(**payload_dict)
            .returning(
                UserTable.id,
                UserTable.username,
                UserTable.fullname,
                UserTable.phone_number,
                UserTable.created_at,
                UserTable.updated_at,
            )
        )

        result = await self.async_session.execute(stmt)

        user = result.one_or_none()

        if not user:
            raise await exc_404.http_404_exc_id_not_found_request()

        await self.async_session.commit()

        return user
