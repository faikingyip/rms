"""
This holds all the business logic pertaining to the dining_table.
You can make calls to functions directly in this module.
The business logic layer is loosely coupled with the persistence layer.
If you need to swap out the persistence layer for another, then simply
replace the existing import of the persistence layer with the implementation
you want and use the alias of persistence_batch_ops_dining_table.
"""

from typing import Callable

from src.app.ops.exceptions.app_ops_exceptions import (
    CreateDiningTableError,
    DeleteDiningTableError,
    GetDiningTableListError,
    UpdateNameError,
    UpdatePositionError,
    UpdateSizeError,
)
from src.app.ops.utils import app_ops_utils
from src.persistence.database.ops import (
    db_batch_ops_dining_table as persistence_batch_ops_dining_table,
)
from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)
from src.schemas import schema_dining_table


def validate_dining_table_name(text: str):
    if not text:
        raise ValueError("Dining table name not provided.")

    if not text.strip():
        raise ValueError("Invalid dining table name format.")


async def create_dining_table(
    request: schema_dining_table.SchemaDiningTableCreate,
    insert_dining_table_func=persistence_batch_ops_dining_table.insert_dining_table,
    validate_dining_table_name_func: Callable[[str], None] = validate_dining_table_name,
) -> schema_dining_table.SchemaDiningTableDisplay:
    try:
        validate_dining_table_name_func(request.name)
    except ValueError as ve:
        raise CreateDiningTableError(ve) from ve

    try:
        return await insert_dining_table_func(request)
    except PersistenceOpsBaseError as poe:
        raise CreateDiningTableError(poe) from poe


async def delete_dining_table(
    dining_table_id,
    delete_dining_table_func=persistence_batch_ops_dining_table.delete_dining_table,
):
    await app_ops_utils.affect_existing_row(
        delete_dining_table_func,
        DeleteDiningTableError,
        dining_table_id=dining_table_id,
    )


async def update_position(
    dining_table_id,
    request: schema_dining_table.SchemaUpdatePosition,
    update_position_func=persistence_batch_ops_dining_table.update_position,
):
    await app_ops_utils.affect_existing_row(
        update_position_func,
        UpdatePositionError,
        dining_table_id=dining_table_id,
        request=request,
    )


async def update_size(
    dining_table_id,
    request: schema_dining_table.SchemaUpdateSize,
    update_size_func=persistence_batch_ops_dining_table.update_size,
):
    await app_ops_utils.affect_existing_row(
        update_size_func,
        UpdateSizeError,
        dining_table_id=dining_table_id,
        request=request,
    )


async def update_name(
    dining_table_id,
    request: schema_dining_table.SchemaUpdateName,
    update_name_func=persistence_batch_ops_dining_table.update_name,
    validate_dining_table_name_func: Callable[[str], None] = validate_dining_table_name,
):
    try:
        validate_dining_table_name_func(request.name)
    except ValueError as ve:
        raise UpdateNameError(ve) from ve

    await app_ops_utils.affect_existing_row(
        update_name_func,
        UpdateNameError,
        dining_table_id=dining_table_id,
        request=request,
    )


async def get_dining_table_list(
    page_index: int,
    page_size: int,
    sort_by: str,
    select_dining_table_list_func=persistence_batch_ops_dining_table.select_dining_table_list,
):
    return await app_ops_utils.get_data_list(
        page_index,
        page_size,
        sort_by,
        select_dining_table_list_func,
        GetDiningTableListError,
    )
