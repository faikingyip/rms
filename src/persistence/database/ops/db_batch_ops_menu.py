"""
Don't call functionality from this modules directly.
These functions are meant to be called y the app_ops layer.
"""

from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError

from src.persistence.database.ops import db_ops_menu
from src.persistence.database.session import async_session_scope
from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)
from src.schemas import schema_menu


async def insert_menu(
    request: schema_menu.SchemaMenuCreate,
    async_session_scope_func=async_session_scope,
    insert_menu_func=db_ops_menu.insert_menu,
):
    async with async_session_scope_func() as async_session:
        try:
            new_record = await insert_menu_func(async_session, request)
            await async_session.commit()
            await async_session.refresh(new_record)
        except SQLAlchemyError as sqlae:
            await async_session.rollback()
            raise PersistenceOpsBaseError(sqlae) from sqlae
        except PersistenceOpsBaseError as poe:
            await async_session.rollback()
            raise PersistenceOpsBaseError(poe) from poe
        return schema_menu.SchemaMenuDisplay.model_validate(new_record)


async def delete_menu(
    menu_id,
    async_session_scope_func=async_session_scope,
    delete_menu_func=db_ops_menu.delete_menu,
):
    async with async_session_scope_func() as async_session:
        try:
            rowcount = await delete_menu_func(async_session, menu_id)
            await async_session.commit()
            return rowcount
        except SQLAlchemyError as sqlae:
            await async_session.rollback()
            raise PersistenceOpsBaseError(sqlae) from sqlae
        except PersistenceOpsBaseError as poe:
            await async_session.rollback()
            raise PersistenceOpsBaseError(poe) from poe


async def update_name(
    menu_id,
    request: schema_menu.SchemaUpdateName,
    async_session_scope_func=async_session_scope,
    update_name_func=db_ops_menu.update_name,
):
    async with async_session_scope_func() as async_session:
        try:
            rowcount = await update_name_func(async_session, menu_id, request)
            await async_session.commit()
            return rowcount
        except SQLAlchemyError as sqlae:
            await async_session.rollback()
            raise PersistenceOpsBaseError(sqlae) from sqlae
        except PersistenceOpsBaseError as poe:
            await async_session.rollback()
            raise PersistenceOpsBaseError(poe) from poe


async def select_menu_list(
    page_index: int,
    page_size: int,
    sort_by: str,
    async_session_scope_func=async_session_scope,
    select_menu_list_func=db_ops_menu.select_menu_list,
):
    async with async_session_scope_func() as async_session:
        try:
            menus = await select_menu_list_func(
                async_session, page_index, page_size, sort_by
            )
            return [
                schema_menu.SchemaMenuDisplay.model_validate(menu) for menu in menus
            ]
        except PersistenceOpsBaseError as poe:
            raise PersistenceOpsBaseError(poe) from poe


async def select_menu_by_id(
    menu_id: UUID,
    async_session_scope_func=async_session_scope,
    select_menu_by_id_func=db_ops_menu.select_menu_by_id,
):
    async with async_session_scope_func() as async_session:
        try:
            menu = await select_menu_by_id_func(async_session, menu_id)
            if not menu:
                return None
            return schema_menu.SchemaMenuDisplay.model_validate(menu)
        except PersistenceOpsBaseError as poe:
            raise PersistenceOpsBaseError(poe) from poe
