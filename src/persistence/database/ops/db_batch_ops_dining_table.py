"""
Don't call functionality from this modules directly.
These functions are meant to be called y the app_ops layer.
"""

from sqlalchemy.exc import SQLAlchemyError

from src.persistence.database.ops import db_ops_dining_table
from src.persistence.database.session import async_session_scope
from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)
from src.schemas import schema_dining_table


async def insert_dining_table(
    request: schema_dining_table.SchemaDiningTableCreate,
    async_session_scope_func=async_session_scope,
    insert_dining_table_func=db_ops_dining_table.insert_dining_table,
):
    async with async_session_scope_func() as async_session:
        try:
            new_record = await insert_dining_table_func(async_session, request)
            await async_session.commit()
            await async_session.refresh(new_record)
        except SQLAlchemyError as sqlae:
            await async_session.rollback()
            raise PersistenceOpsBaseError(sqlae) from sqlae
        except PersistenceOpsBaseError as poe:
            await async_session.rollback()
            raise PersistenceOpsBaseError(poe) from poe
        return schema_dining_table.SchemaDiningTableDisplay.model_validate(new_record)


async def delete_dining_table(
    dining_table_id,
    async_session_scope_func=async_session_scope,
    delete_dining_table_func=db_ops_dining_table.delete_dining_table,
):
    async with async_session_scope_func() as async_session:
        try:
            rowcount = await delete_dining_table_func(async_session, dining_table_id)
            await async_session.commit()
            return rowcount
        except SQLAlchemyError as sqlae:
            await async_session.rollback()
            raise PersistenceOpsBaseError(sqlae) from sqlae
        except PersistenceOpsBaseError as poe:
            await async_session.rollback()
            raise PersistenceOpsBaseError(poe) from poe


async def update_position(
    dining_table_id,
    request: schema_dining_table.SchemaUpdatePosition,
    async_session_scope_func=async_session_scope,
    update_position_func=db_ops_dining_table.update_position,
):
    async with async_session_scope_func() as async_session:
        try:
            rowcount = await update_position_func(
                async_session, dining_table_id, request
            )
            await async_session.commit()
            return rowcount
        except SQLAlchemyError as sqlae:
            await async_session.rollback()
            raise PersistenceOpsBaseError(sqlae) from sqlae
        except PersistenceOpsBaseError as poe:
            await async_session.rollback()
            raise PersistenceOpsBaseError(poe) from poe


async def update_size(
    dining_table_id,
    request: schema_dining_table.SchemaUpdateSize,
    async_session_scope_func=async_session_scope,
    update_size_func=db_ops_dining_table.update_size,
):
    async with async_session_scope_func() as async_session:
        try:
            rowcount = await update_size_func(async_session, dining_table_id, request)
            await async_session.commit()
            return rowcount
        except SQLAlchemyError as sqlae:
            await async_session.rollback()
            raise PersistenceOpsBaseError(sqlae) from sqlae
        except PersistenceOpsBaseError as poe:
            await async_session.rollback()
            raise PersistenceOpsBaseError(poe) from poe


async def update_name(
    dining_table_id,
    request: schema_dining_table.SchemaUpdateName,
    async_session_scope_func=async_session_scope,
    update_name_func=db_ops_dining_table.update_name,
):
    async with async_session_scope_func() as async_session:
        try:
            rowcount = await update_name_func(async_session, dining_table_id, request)
            await async_session.commit()
            return rowcount
        except SQLAlchemyError as sqlae:
            await async_session.rollback()
            raise PersistenceOpsBaseError(sqlae) from sqlae
        except PersistenceOpsBaseError as poe:
            await async_session.rollback()
            raise PersistenceOpsBaseError(poe) from poe


async def select_dining_table_list(
    page_index: int,
    page_size: int,
    sort_by: str,
    async_session_scope_func=async_session_scope,
    select_dining_table_list_func=db_ops_dining_table.select_dining_table_list,
):
    async with async_session_scope_func() as async_session:
        try:
            dining_tables = await select_dining_table_list_func(
                async_session, page_index, page_size, sort_by
            )
            return [
                schema_dining_table.SchemaDiningTableDisplay.model_validate(
                    dining_table
                )
                for dining_table in dining_tables
            ]
        except PersistenceOpsBaseError as poe:
            raise PersistenceOpsBaseError(poe) from poe
