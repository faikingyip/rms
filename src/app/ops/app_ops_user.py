"""
This holds all the business logic pertaining to the user.
You can make calls to functions directly in this module.
The business logic layer is loosely coupled with the persistence layer.
If you need to swap out the persistence layer for another, then simply
replace the existing import of the persistence layer with the implementation
you want and use the alias of persistence_batch_ops_user.
"""

from typing import Callable
from uuid import UUID

import src.schemas.schema_user as schema_user
from src.app.ops.exceptions.app_ops_exceptions import (
    ChangePasswordError,
    CreateUserError,
    DeleteUserError,
    GetUserByIdError,
    GetUserByUsernameError,
    GetUserListError,
    LoginError,
)
from src.app.ops.utils import app_ops_utils
from src.persistence.database.ops import db_batch_ops_user as persistence_batch_ops_user
from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)


def validate_password(text: str):
    if not text:
        raise ValueError("No password was provided.")

    if not text.strip():
        raise ValueError("Invalid password format.")


def validate_pin(text: str):
    if not text:
        raise ValueError("No PIN was provided.")

    if not text.isdigit():
        raise ValueError("Invalid PIN format.")


async def create_user(
    request: schema_user.SchemaUserCreate,
    insert_user_func=persistence_batch_ops_user.insert_user,
    validate_password_func: Callable[[str], None] = validate_password,
) -> schema_user.SchemaUserDisplay:
    try:
        validate_password_func(request.password)
    except ValueError as ve:
        raise CreateUserError(ve) from ve

    try:
        return await insert_user_func(request)
    except PersistenceOpsBaseError as poe:
        raise CreateUserError(poe) from poe


async def delete_user(user_id, delete_user_func=persistence_batch_ops_user.delete_user):
    await app_ops_utils.affect_existing_row(
        delete_user_func, DeleteUserError, user_id=user_id
    )


async def change_password(
    user_id,
    request: schema_user.SchemaChangePassword,
    update_password_func=persistence_batch_ops_user.update_password,
    validate_password_func: Callable[[str], None] = validate_password,
):
    try:
        validate_password_func(request.new_password)
    except ValueError as ve:
        raise ChangePasswordError(ve) from ve

    await app_ops_utils.affect_existing_row(
        update_password_func, ChangePasswordError, user_id=user_id, request=request
    )


async def get_user_list(
    page_index: int,
    page_size: int,
    sort_by: str,
    select_user_list_func=persistence_batch_ops_user.select_user_list,
):
    return await app_ops_utils.get_data_list(
        page_index, page_size, sort_by, select_user_list_func, GetUserListError
    )


async def get_user_by_id(
    user_id: UUID,
    select_user_by_id_func=persistence_batch_ops_user.select_user_by_id,
):
    try:
        return await select_user_by_id_func(user_id)
    except PersistenceOpsBaseError as poe:
        raise GetUserByIdError(poe) from poe


async def get_user_by_username(
    username: str,
    select_user_by_username_func=persistence_batch_ops_user.select_user_by_username,
):
    if not username:
        raise GetUserByUsernameError("No username provided.")

    try:
        return await select_user_by_username_func(username)
    except PersistenceOpsBaseError as poe:
        raise GetUserByUsernameError(poe) from poe


async def login(
    username: str,
    password: str,
    select_user_by_username_and_password_func=persistence_batch_ops_user.select_user_by_username_and_password,
):
    if not username or not password:
        return None

    try:
        return await select_user_by_username_and_password_func(username, password)
    except PersistenceOpsBaseError as poe:
        raise LoginError(poe) from poe
