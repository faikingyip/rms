"""
Don't call functionality from this module directly.
These functions are meant to be called by the persistence_batch_ops layer.
"""

# from uuid import UUID

from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.persistence.database.models.db_tag import DbTag
from src.persistence.database.utils import query_utils
from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)
from src.schemas.schema_tag import SchemaTagCreate, SchemaUpdateName


async def insert_tag(async_session: AsyncSession, request: SchemaTagCreate):
    new_record = DbTag(name=request.name)
    try:
        async_session.add(new_record)
        return new_record
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae


async def delete_tag(async_session: AsyncSession, tag_id):
    stmt = delete(DbTag).where(DbTag.id == tag_id)
    try:
        return (await async_session.execute(stmt)).rowcount
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae


async def update_name(async_session: AsyncSession, tag_id, request: SchemaUpdateName):
    stmt = update(DbTag).where(DbTag.id == tag_id).values(name=request.name)
    try:
        return (await async_session.execute(stmt)).rowcount
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae


async def select_tag_list(
    async_session: AsyncSession, page_index: int, page_size: int, sort_by: str
):
    query = select(DbTag)
    query = query_utils.apply_sorting_and_paging_to_list_query(
        query, DbTag, page_index, page_size, sort_by
    )
    try:
        results = await async_session.execute(query)
        tags = results.scalars().all()
        return tags
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae


async def select_tag_by_id(async_session: AsyncSession, tag_id: UUID):
    query = select(DbTag).where(DbTag.id == tag_id)
    try:
        return (await async_session.execute(query)).scalar_one_or_none()
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae
