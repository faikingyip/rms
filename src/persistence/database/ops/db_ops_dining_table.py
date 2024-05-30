"""
Don't call functionality from this module directly.
These functions are meant to be called by the persistence_batch_ops layer.
"""

# from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.persistence.database.models.db_dining_table import DbDiningTable
from src.persistence.database.utils import query_utils
from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)
from src.schemas.schema_dining_table import (
    SchemaDiningTableCreate,
    SchemaUpdateName,
    SchemaUpdatePosition,
    SchemaUpdateSize,
)


async def insert_dining_table(
    async_session: AsyncSession, request: SchemaDiningTableCreate
):
    new_record = DbDiningTable(
        name=request.name,
        x=request.x,
        y=request.y,
        width=request.width,
        height=request.height,
    )
    try:
        async_session.add(new_record)
        return new_record
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae


async def delete_dining_table(async_session: AsyncSession, dining_table_id):
    stmt = delete(DbDiningTable).where(DbDiningTable.id == dining_table_id)
    try:
        return (await async_session.execute(stmt)).rowcount
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae


async def update_position(
    async_session: AsyncSession, dining_table_id, request: SchemaUpdatePosition
):
    stmt = (
        update(DbDiningTable)
        .where(DbDiningTable.id == dining_table_id)
        .values(x=request.x, y=request.y)
    )
    try:
        return (await async_session.execute(stmt)).rowcount
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae


async def update_size(
    async_session: AsyncSession, dining_table_id, request: SchemaUpdateSize
):
    stmt = (
        update(DbDiningTable)
        .where(DbDiningTable.id == dining_table_id)
        .values(width=request.width, height=request.height)
    )
    try:
        return (await async_session.execute(stmt)).rowcount
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae


async def update_name(
    async_session: AsyncSession, dining_table_id, request: SchemaUpdateName
):
    stmt = (
        update(DbDiningTable)
        .where(DbDiningTable.id == dining_table_id)
        .values(name=request.name)
    )
    try:
        return (await async_session.execute(stmt)).rowcount
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae


async def select_dining_table_list(
    async_session: AsyncSession, page_index: int, page_size: int, sort_by: str
):
    query = select(DbDiningTable)
    query = query_utils.apply_sorting_and_paging_to_list_query(
        query, DbDiningTable, page_index, page_size, sort_by
    )
    try:
        results = await async_session.execute(query)
        dining_tables = results.scalars().all()
        return dining_tables
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae
