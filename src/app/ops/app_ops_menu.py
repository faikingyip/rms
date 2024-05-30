"""
This holds all the business logic pertaining to the menu.
You can make calls to functions directly in this module.
The business logic layer is loosely coupled with the persistence layer.
If you need to swap out the persistence layer for another, then simply
replace the existing import of the persistence layer with the implementation
you want and use the alias of persistence_batch_ops_menu.
"""

from typing import Callable
from uuid import UUID

from src.app.ops.exceptions.app_ops_exceptions import (
    CreateMenuError,
    DeleteMenuError,
    GetMenuByIdError,
    GetMenuListError,
    UpdateNameError,
)
from src.app.ops.utils import app_ops_utils
from src.persistence.database.ops import db_batch_ops_menu as persistence_batch_ops_menu
from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)
from src.schemas import schema_menu


def validate_menu_name(text: str):
    if not text:
        raise ValueError("Menu name not provided.")

    if not text.strip():
        raise ValueError("Invalid menu name format.")


async def create_menu(
    request: schema_menu.SchemaMenuCreate,
    insert_menu_func=persistence_batch_ops_menu.insert_menu,
    validate_menu_name_func: Callable[[str], None] = validate_menu_name,
) -> schema_menu.SchemaMenuDisplay:
    try:
        validate_menu_name_func(request.name)
    except ValueError as ve:
        raise CreateMenuError(ve) from ve

    try:
        return await insert_menu_func(request)
    except PersistenceOpsBaseError as poe:
        raise CreateMenuError(poe) from poe


async def delete_menu(
    menu_id,
    delete_menu_func=persistence_batch_ops_menu.delete_menu,
):
    await app_ops_utils.affect_existing_row(
        delete_menu_func, DeleteMenuError, menu_id=menu_id
    )


async def update_name(
    menu_id,
    request: schema_menu.SchemaUpdateName,
    update_name_func=persistence_batch_ops_menu.update_name,
    validate_menu_name_func: Callable[[str], None] = validate_menu_name,
):
    try:
        validate_menu_name_func(request.name)
    except ValueError as ve:
        raise UpdateNameError(ve) from ve

    await app_ops_utils.affect_existing_row(
        update_name_func, UpdateNameError, menu_id=menu_id, request=request
    )


async def get_menu_list(
    page_index: int,
    page_size: int,
    sort_by: str,
    select_menu_list_func=persistence_batch_ops_menu.select_menu_list,
):
    return await app_ops_utils.get_data_list(
        page_index, page_size, sort_by, select_menu_list_func, GetMenuListError
    )


async def get_menu_by_id(
    menu_id: UUID,
    select_menu_by_id_func=persistence_batch_ops_menu.select_menu_by_id,
):
    try:
        return await select_menu_by_id_func(menu_id)
    except PersistenceOpsBaseError as poe:
        raise GetMenuByIdError(poe) from poe
