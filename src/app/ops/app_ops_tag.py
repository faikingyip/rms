"""
This holds all the business logic pertaining to the tag.
You can make calls to functions directly in this module.
The business logic layer is loosely coupled with the persistence layer.
If you need to swap out the persistence layer for another, then simply
replace the existing import of the persistence layer with the implementation
you want and use the alias of persistence_batch_ops_tag.
"""

from typing import Callable
from uuid import UUID

from src.app.ops.exceptions.app_ops_exceptions import (
    CreateTagError,
    DeleteTagError,
    GetTagByIdError,
    GetTagListError,
    UpdateNameError,
)
from src.app.ops.utils import app_ops_utils
from src.persistence.database.ops import db_batch_ops_tag as persistence_batch_ops_tag
from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)
from src.schemas import schema_tag


def validate_tag_name(text: str):
    if not text:
        raise ValueError("Tag name not provided.")

    if not text.strip():
        raise ValueError("Invalid tag name format.")


async def create_tag(
    request: schema_tag.SchemaTagCreate,
    insert_tag_func=persistence_batch_ops_tag.insert_tag,
    validate_tag_name_func: Callable[[str], None] = validate_tag_name,
) -> schema_tag.SchemaTagDisplay:
    try:
        validate_tag_name_func(request.name)
    except ValueError as ve:
        raise CreateTagError(ve) from ve

    try:
        return await insert_tag_func(request)
    except PersistenceOpsBaseError as poe:
        raise CreateTagError(poe) from poe


async def delete_tag(
    tag_id,
    delete_tag_func=persistence_batch_ops_tag.delete_tag,
):
    await app_ops_utils.affect_existing_row(
        delete_tag_func, DeleteTagError, tag_id=tag_id
    )


async def update_name(
    tag_id,
    request: schema_tag.SchemaUpdateName,
    update_name_func=persistence_batch_ops_tag.update_name,
    validate_tag_name_func: Callable[[str], None] = validate_tag_name,
):
    try:
        validate_tag_name_func(request.name)
    except ValueError as ve:
        raise UpdateNameError(ve) from ve

    await app_ops_utils.affect_existing_row(
        update_name_func, UpdateNameError, tag_id=tag_id, request=request
    )


async def get_tag_list(
    page_index: int,
    page_size: int,
    sort_by: str,
    select_tag_list_func=persistence_batch_ops_tag.select_tag_list,
):
    return await app_ops_utils.get_data_list(
        page_index, page_size, sort_by, select_tag_list_func, GetTagListError
    )


async def get_tag_by_id(
    tag_id: UUID,
    select_tag_by_id_func=persistence_batch_ops_tag.select_tag_by_id,
):
    try:
        return await select_tag_by_id_func(tag_id)
    except PersistenceOpsBaseError as poe:
        raise GetTagByIdError(poe) from poe
