"""
Don't call functionality from this modules directly.
These functions are meant to be called y the app_ops layer.
"""

from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError

from src.persistence.database.ops import db_ops_tag
from src.persistence.database.session import async_session_scope
from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)
from src.schemas import schema_tag


async def insert_tag(
    request: schema_tag.SchemaTagCreate,
    async_session_scope_func=async_session_scope,
    insert_tag_func=db_ops_tag.insert_tag,
):
    async with async_session_scope_func() as async_session:
        try:
            new_record = await insert_tag_func(async_session, request)
            await async_session.commit()
            await async_session.refresh(new_record)
        except SQLAlchemyError as sqlae:
            await async_session.rollback()
            raise PersistenceOpsBaseError(sqlae) from sqlae
        except PersistenceOpsBaseError as poe:
            await async_session.rollback()
            raise PersistenceOpsBaseError(poe) from poe
        return schema_tag.SchemaTagDisplay.model_validate(new_record)


async def delete_tag(
    tag_id,
    async_session_scope_func=async_session_scope,
    delete_tag_func=db_ops_tag.delete_tag,
):
    async with async_session_scope_func() as async_session:
        try:
            rowcount = await delete_tag_func(async_session, tag_id)
            await async_session.commit()
            return rowcount
        except SQLAlchemyError as sqlae:
            await async_session.rollback()
            raise PersistenceOpsBaseError(sqlae) from sqlae
        except PersistenceOpsBaseError as poe:
            await async_session.rollback()
            raise PersistenceOpsBaseError(poe) from poe


async def update_name(
    tag_id,
    request: schema_tag.SchemaUpdateName,
    async_session_scope_func=async_session_scope,
    update_name_func=db_ops_tag.update_name,
):
    async with async_session_scope_func() as async_session:
        try:
            rowcount = await update_name_func(async_session, tag_id, request)
            await async_session.commit()
            return rowcount
        except SQLAlchemyError as sqlae:
            await async_session.rollback()
            raise PersistenceOpsBaseError(sqlae) from sqlae
        except PersistenceOpsBaseError as poe:
            await async_session.rollback()
            raise PersistenceOpsBaseError(poe) from poe


async def select_tag_list(
    page_index: int,
    page_size: int,
    sort_by: str,
    async_session_scope_func=async_session_scope,
    select_tag_list_func=db_ops_tag.select_tag_list,
):
    async with async_session_scope_func() as async_session:
        try:
            tags = await select_tag_list_func(
                async_session, page_index, page_size, sort_by
            )
            return [schema_tag.SchemaTagDisplay.model_validate(tag) for tag in tags]
        except PersistenceOpsBaseError as poe:
            raise PersistenceOpsBaseError(poe) from poe


async def select_tag_by_id(
    tag_id: UUID,
    async_session_scope_func=async_session_scope,
    select_tag_by_id_func=db_ops_tag.select_tag_by_id,
):
    async with async_session_scope_func() as async_session:
        try:
            tag = await select_tag_by_id_func(async_session, tag_id)
            if not tag:
                return None
            return schema_tag.SchemaTagDisplay.model_validate(tag)
        except PersistenceOpsBaseError as poe:
            raise PersistenceOpsBaseError(poe) from poe
