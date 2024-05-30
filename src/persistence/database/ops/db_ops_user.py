"""
Don't call functionality from this module directly.
These functions are meant to be called by the persistence_batch_ops layer.
"""

from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.persistence.database.models.db_user import DbUser
from src.persistence.database.utils import query_utils
from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)
from src.schemas.schema_user import SchemaChangePassword, SchemaUserCreate
from src.utils import bcrypt_hash


async def insert_user(async_session: AsyncSession, request: SchemaUserCreate):
    new_record = DbUser(
        username=request.username, password_hash=bcrypt_hash.bcrypt(request.password)
    )
    try:
        async_session.add(new_record)
        return new_record
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae


async def delete_user(async_session: AsyncSession, user_id):
    stmt = delete(DbUser).where(DbUser.id == user_id)
    try:
        return (await async_session.execute(stmt)).rowcount
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae


async def update_password(
    async_session: AsyncSession, user_id, request: SchemaChangePassword
):
    stmt = (
        update(DbUser)
        .where(DbUser.id == user_id)
        .values(password_hash=bcrypt_hash.bcrypt(request.new_password))
    )
    try:
        return (await async_session.execute(stmt)).rowcount
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae


async def select_user_list(
    async_session: AsyncSession, page_index: int, page_size: int, sort_by: str
):
    query = select(DbUser)
    query = query_utils.apply_sorting_and_paging_to_list_query(
        query, DbUser, page_index, page_size, sort_by
    )
    try:
        results = await async_session.execute(query)
        users = results.scalars().all()
        return users
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae


async def select_user_by_id(async_session: AsyncSession, user_id: UUID):
    query = select(DbUser).where(DbUser.id == user_id)
    try:
        return (await async_session.execute(query)).scalar_one_or_none()
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae


async def select_user_by_username(async_session: AsyncSession, username: str):
    query = select(DbUser).where(DbUser.username == username)
    try:
        return (await async_session.execute(query)).scalar_one_or_none()
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae
