"""
Don't call functionality from this modules directly.
These functions are meant to be called y the app_ops layer.
"""

from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError

import src.schemas.schema_user as schema_user
from src.persistence.database.ops import db_ops_user
from src.persistence.database.session import async_session_scope
from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)
from src.utils import bcrypt_hash


async def insert_user(
    request: schema_user.SchemaUserCreate,
    async_session_scope_func=async_session_scope,
    insert_user_func=db_ops_user.insert_user,
):
    async with async_session_scope_func() as async_session:
        try:
            new_record = await insert_user_func(async_session, request)
            await async_session.commit()
            await async_session.refresh(new_record)
        except SQLAlchemyError as sqlae:
            await async_session.rollback()
            raise PersistenceOpsBaseError(sqlae) from sqlae
        except PersistenceOpsBaseError as poe:
            await async_session.rollback()
            raise PersistenceOpsBaseError(poe) from poe
        return schema_user.SchemaUserDisplay.model_validate(new_record)


async def delete_user(
    user_id,
    async_session_scope_func=async_session_scope,
    delete_user_func=db_ops_user.delete_user,
):
    async with async_session_scope_func() as async_session:
        try:
            rowcount = await delete_user_func(async_session, user_id)
            await async_session.commit()
            return rowcount
        except SQLAlchemyError as sqlae:
            await async_session.rollback()
            raise PersistenceOpsBaseError(sqlae) from sqlae
        except PersistenceOpsBaseError as poe:
            await async_session.rollback()
            raise PersistenceOpsBaseError(poe) from poe


async def update_password(
    user_id,
    request: schema_user.SchemaChangePassword,
    async_session_scope_func=async_session_scope,
    update_password_func=db_ops_user.update_password,
):

    async with async_session_scope_func() as async_session:
        try:
            rowcount = await update_password_func(async_session, user_id, request)
            await async_session.commit()
            return rowcount
        except SQLAlchemyError as sqlae:
            await async_session.rollback()
            raise PersistenceOpsBaseError(sqlae) from sqlae
        except PersistenceOpsBaseError as poe:
            await async_session.rollback()
            raise PersistenceOpsBaseError(poe) from poe


async def select_user_list(
    page_index: int,
    page_size: int,
    sort_by: str,
    async_session_scope_func=async_session_scope,
    select_user_list_func=db_ops_user.select_user_list,
):
    async with async_session_scope_func() as async_session:
        try:
            users = await select_user_list_func(
                async_session, page_index, page_size, sort_by
            )
            return [
                schema_user.SchemaUserDisplay.model_validate(user) for user in users
            ]
        except PersistenceOpsBaseError as poe:
            raise PersistenceOpsBaseError(poe) from poe


async def select_user_by_id(
    user_id: UUID,
    async_session_scope_func=async_session_scope,
    select_user_by_id_func=db_ops_user.select_user_by_id,
):
    async with async_session_scope_func() as async_session:
        try:
            user = await select_user_by_id_func(async_session, user_id)
            if not user:
                return None
            return schema_user.SchemaUserDisplay.model_validate(user)
        except PersistenceOpsBaseError as poe:
            raise PersistenceOpsBaseError(poe) from poe


async def select_user_by_username(
    username: str,
    async_session_scope_func=async_session_scope,
    select_user_by_username_func=db_ops_user.select_user_by_username,
):
    async with async_session_scope_func() as async_session:
        try:
            user = await select_user_by_username_func(async_session, username)
            if not user:
                return None
            return schema_user.SchemaUserDisplay.model_validate(user)
        except PersistenceOpsBaseError as poe:
            raise PersistenceOpsBaseError(poe) from poe


async def select_user_by_username_and_password(
    username: str,
    password: str,
    async_session_scope_func=async_session_scope,
    select_user_by_username_func=db_ops_user.select_user_by_username,
):
    if not username or not password:
        return None

    user = None
    async with async_session_scope_func() as async_session:
        try:
            user = await select_user_by_username_func(async_session, username)
        except PersistenceOpsBaseError as poe:
            raise PersistenceOpsBaseError(poe) from poe

    if user is None:
        return None

    if not _is_password_correct(password, user.password_hash):
        return None

    return schema_user.SchemaUserDisplay.model_validate(user)


def _is_password_correct(password, password_hash):
    return bcrypt_hash.verify_bcrypt(password, password_hash)
