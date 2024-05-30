"""
Don't call functionality from this module directly.
These functions are meant to be called by the persistence_batch_ops layer.
"""

# from uuid import UUID

from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.persistence.database.models.db_menu import DbMenu
from src.persistence.database.utils import query_utils
from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)
from src.schemas.schema_menu import SchemaMenuCreate, SchemaUpdateName


async def insert_menu(async_session: AsyncSession, request: SchemaMenuCreate):
    new_record = DbMenu(name=request.name)
    try:
        async_session.add(new_record)
        return new_record
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae


async def delete_menu(async_session: AsyncSession, menu_id):
    stmt = delete(DbMenu).where(DbMenu.id == menu_id)
    try:
        return (await async_session.execute(stmt)).rowcount
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae


async def update_name(async_session: AsyncSession, menu_id, request: SchemaUpdateName):
    stmt = update(DbMenu).where(DbMenu.id == menu_id).values(name=request.name)
    try:
        return (await async_session.execute(stmt)).rowcount
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae


async def select_menu_list(
    async_session: AsyncSession, page_index: int, page_size: int, sort_by: str
):
    query = select(DbMenu)
    query = query_utils.apply_sorting_and_paging_to_list_query(
        query, DbMenu, page_index, page_size, sort_by
    )
    try:
        results = await async_session.execute(query)
        menus = results.scalars().all()
        return menus
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae


async def select_menu_by_id(async_session: AsyncSession, menu_id: UUID):
    query = select(DbMenu).where(DbMenu.id == menu_id)
    try:
        return (await async_session.execute(query)).scalar_one_or_none()
    except SQLAlchemyError as sqlae:
        raise PersistenceOpsBaseError(sqlae) from sqlae
