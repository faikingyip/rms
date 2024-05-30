import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

import src.app.ops.app_ops_user as app_ops_user
from src.app.ops.exceptions.app_ops_exceptions import (
    ChangePasswordError,
    CreateUserError,
    DeleteUserError,
    GetUserByIdError,
    GetUserByUsernameError,
    GetUserListError,
    LoginError,
)
from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)
from src.schemas import schema_user


def test_validate_password():
    try:
        app_ops_user.validate_password("valid")
    except ValueError:
        pytest.fail("Error was raised unexpectedly.")


def test_validate_password_empty():
    with pytest.raises(ValueError, match="No password was provided."):
        app_ops_user.validate_password("")
    with pytest.raises(ValueError, match="No password was provided."):
        app_ops_user.validate_password(None)


def test_validate_password_whitespace_only():
    with pytest.raises(ValueError, match="Invalid password format."):
        app_ops_user.validate_password("     ")


def test_validate_pin():
    try:
        app_ops_user.validate_pin("123456")
    except ValueError:
        pytest.fail("Error was raised unexpectedly.")


def test_validate_pin_empty():
    with pytest.raises(ValueError, match="No PIN was provided."):
        app_ops_user.validate_pin("")
    with pytest.raises(ValueError, match="No PIN was provided."):
        app_ops_user.validate_pin(None)


def test_validate_pin_non_digits():
    with pytest.raises(ValueError, match="Invalid PIN format."):
        app_ops_user.validate_pin("     ")
    with pytest.raises(ValueError, match="Invalid PIN format."):
        app_ops_user.validate_pin("123A5")


@pytest.mark.asyncio
async def test_create_user():
    request = schema_user.SchemaUserCreate(username="testuser", password="testuser")
    mock_insert_user_func = AsyncMock(
        return_value=schema_user.SchemaUserDisplay(
            id=uuid.uuid4(),
            username="testuser",
            created_on=datetime.now(),
            last_updated_on=datetime.now(),
        )
    )
    new_user = await app_ops_user.create_user(
        request, insert_user_func=mock_insert_user_func
    )
    mock_insert_user_func.assert_called_once()
    assert isinstance(new_user, schema_user.SchemaUserDisplay)


@pytest.mark.asyncio
async def test_create_user_invalid_password_format():
    request = schema_user.SchemaUserCreate(username="myusername", password="    ")
    mock_insert_user_func = AsyncMock(
        return_value=schema_user.SchemaUserDisplay(
            id=uuid.uuid4(),
            username="testuser",
            created_on=datetime.now(),
            last_updated_on=datetime.now(),
        )
    )
    with pytest.raises(CreateUserError, match="Invalid password format."):
        await app_ops_user.create_user(request, insert_user_func=mock_insert_user_func)
    mock_insert_user_func.assert_not_called()


@pytest.mark.asyncio
async def test_create_user_persistence_error():
    # Could be database error, including violation of unique username
    request = schema_user.SchemaUserCreate(username="testuser", password="testuser")
    mock_insert_user_func = AsyncMock(
        return_value=schema_user.SchemaUserDisplay(
            id=uuid.uuid4(),
            username="testuser",
            created_on=datetime.now(),
            last_updated_on=datetime.now(),
        )
    )
    mock_insert_user_func.side_effect = PersistenceOpsBaseError()
    with pytest.raises(CreateUserError):
        await app_ops_user.create_user(request, insert_user_func=mock_insert_user_func)
    mock_insert_user_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_user():
    mock_delete_user_func = AsyncMock(return_value=1)
    await app_ops_user.delete_user(uuid.uuid4(), delete_user_func=mock_delete_user_func)
    mock_delete_user_func.assert_called_once()


@pytest.mark.asyncio
async def test_delete_user_persistence_error():
    mock_delete_user_func = AsyncMock(return_value=1)
    mock_delete_user_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(DeleteUserError):
        await app_ops_user.delete_user(
            uuid.uuid4(), delete_user_func=mock_delete_user_func
        )
    mock_delete_user_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_user_no_rows_affected():
    mock_delete_user_func = AsyncMock(return_value=0)
    with pytest.raises(DeleteUserError, match="No rows were affected."):
        await app_ops_user.delete_user(
            uuid.uuid4(), delete_user_func=mock_delete_user_func
        )
    mock_delete_user_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_user_more_than_one_row_affected():
    mock_delete_user_func = AsyncMock(return_value=2)
    with pytest.raises(DeleteUserError, match="More than 1 row was affected."):
        await app_ops_user.delete_user(
            uuid.uuid4(), delete_user_func=mock_delete_user_func
        )
    mock_delete_user_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_change_password():
    request = schema_user.SchemaChangePassword(new_password="new_password")
    mock_update_password_func = AsyncMock(return_value=1)
    await app_ops_user.change_password(
        uuid.uuid4(), request, update_password_func=mock_update_password_func
    )
    mock_update_password_func.assert_called_once()


@pytest.mark.asyncio
async def test_change_password_invalid_password_format():
    request = schema_user.SchemaChangePassword(new_password="    ")
    mock_update_password_func = AsyncMock(return_value=1)
    with pytest.raises(ChangePasswordError):
        await app_ops_user.change_password(
            uuid.uuid4(), request, update_password_func=mock_update_password_func
        )
    mock_update_password_func.assert_not_called()


@pytest.mark.asyncio
async def test_change_password_persistence_error():
    request = schema_user.SchemaChangePassword(new_password="new_password")
    mock_update_password_func = AsyncMock(return_value=1)
    mock_update_password_func.side_effect = PersistenceOpsBaseError()
    with pytest.raises(ChangePasswordError):
        await app_ops_user.change_password(
            uuid.uuid4(), request, update_password_func=mock_update_password_func
        )
    mock_update_password_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_change_password_no_rows_affected():
    request = schema_user.SchemaChangePassword(new_password="new_password")
    mock_update_password_func = AsyncMock(return_value=0)
    with pytest.raises(ChangePasswordError, match="No rows were affected."):
        await app_ops_user.change_password(
            uuid.uuid4(), request, update_password_func=mock_update_password_func
        )
    mock_update_password_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_change_password_multiple_rows_affected():
    request = schema_user.SchemaChangePassword(new_password="new_password")
    mock_update_password_func = AsyncMock(return_value=2)
    with pytest.raises(ChangePasswordError, match="More than 1 row was affected."):
        await app_ops_user.change_password(
            uuid.uuid4(), request, update_password_func=mock_update_password_func
        )
    mock_update_password_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_user_list():

    returned_user1 = schema_user.SchemaUserDisplay(
        id=uuid.uuid4(),
        username="testuser1",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )

    returned_user2 = schema_user.SchemaUserDisplay(
        id=uuid.uuid4(),
        username="testuser2",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )

    returned_user3 = schema_user.SchemaUserDisplay(
        id=uuid.uuid4(),
        username="testuser3",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )

    mock_select_user_list_func = AsyncMock()
    mock_select_user_list_func.return_value = [
        returned_user1,
        returned_user2,
        returned_user3,
    ]

    results = await app_ops_user.get_user_list(
        0,
        10,
        "created_on DESC, username",
        select_user_list_func=mock_select_user_list_func,
    )
    mock_select_user_list_func.assert_awaited_once()
    assert len(results) == 3
    assert all(isinstance(item, schema_user.SchemaUserDisplay) for item in results)


@pytest.mark.asyncio
async def test_get_user_list_invalid_page_index():

    mock_select_user_list_func = AsyncMock()
    with pytest.raises(GetUserListError):
        await app_ops_user.get_user_list(
            -1,
            10,
            "created_on DESC, username",
            select_user_list_func=mock_select_user_list_func,
        )
    mock_select_user_list_func.assert_not_called()


@pytest.mark.asyncio
async def test_get_user_list_invalid_page_size():

    mock_select_user_list_func = AsyncMock()
    with pytest.raises(GetUserListError):
        await app_ops_user.get_user_list(
            0,
            0,
            "created_on DESC, username",
            select_user_list_func=mock_select_user_list_func,
        )
    mock_select_user_list_func.assert_not_called()


@pytest.mark.asyncio
async def test_get_user_list_persistence_error():

    mock_select_user_list_func = AsyncMock()
    mock_select_user_list_func.side_effect = PersistenceOpsBaseError()
    with pytest.raises(GetUserListError):
        await app_ops_user.get_user_list(
            0,
            10,
            "created_on DESC, username",
            select_user_list_func=mock_select_user_list_func,
        )
    mock_select_user_list_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_user_by_id():

    returned_user1 = schema_user.SchemaUserDisplay(
        id=uuid.uuid4(),
        username="testuser1",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )

    mock_select_user_by_id_func = AsyncMock()
    mock_select_user_by_id_func.return_value = returned_user1
    user = await app_ops_user.get_user_by_id(
        uuid.uuid4(), select_user_by_id_func=mock_select_user_by_id_func
    )
    mock_select_user_by_id_func.assert_awaited_once()
    assert isinstance(user, schema_user.SchemaUserDisplay)
    assert user.id == returned_user1.id


@pytest.mark.asyncio
async def test_get_user_by_id_not_found():

    mock_select_user_by_id_func = AsyncMock()
    mock_select_user_by_id_func.return_value = None
    user = await app_ops_user.get_user_by_id(
        uuid.uuid4(), select_user_by_id_func=mock_select_user_by_id_func
    )
    mock_select_user_by_id_func.assert_awaited_once()
    assert user is None


@pytest.mark.asyncio
async def test_get_user_by_id_persistence_error():

    mock_select_user_by_id_func = AsyncMock()
    mock_select_user_by_id_func.side_effect = PersistenceOpsBaseError()
    with pytest.raises(GetUserByIdError):
        await app_ops_user.get_user_by_id(
            uuid.uuid4(), select_user_by_id_func=mock_select_user_by_id_func
        )
    mock_select_user_by_id_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_user_by_username():

    returned_user1 = schema_user.SchemaUserDisplay(
        id=uuid.uuid4(),
        username="testuser1",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )

    mock_select_user_by_username_func = AsyncMock()
    mock_select_user_by_username_func.return_value = returned_user1
    user = await app_ops_user.get_user_by_username(
        "testuser1", select_user_by_username_func=mock_select_user_by_username_func
    )
    mock_select_user_by_username_func.assert_awaited_once()
    assert isinstance(user, schema_user.SchemaUserDisplay)
    assert user.id == returned_user1.id


@pytest.mark.asyncio
async def test_get_user_by_username_username_not_provided():

    mock_select_user_by_username_func = AsyncMock()
    mock_select_user_by_username_func.side_effect = PersistenceOpsBaseError()
    with pytest.raises(GetUserByUsernameError, match="No username provided."):
        await app_ops_user.get_user_by_username(
            "", select_user_by_username_func=mock_select_user_by_username_func
        )
    mock_select_user_by_username_func.assert_not_called()


@pytest.mark.asyncio
async def test_get_user_by_username_not_found():

    mock_select_user_by_username_func = AsyncMock()
    mock_select_user_by_username_func.return_value = None

    user = await app_ops_user.get_user_by_username(
        "testuser1", select_user_by_username_func=mock_select_user_by_username_func
    )
    mock_select_user_by_username_func.assert_awaited_once()
    assert user is None


@pytest.mark.asyncio
async def test_get_user_by_username_persistence_error():

    mock_select_user_by_username_func = AsyncMock()
    mock_select_user_by_username_func.side_effect = PersistenceOpsBaseError()
    with pytest.raises(GetUserByUsernameError):
        await app_ops_user.get_user_by_username(
            "testuser1", select_user_by_username_func=mock_select_user_by_username_func
        )
    mock_select_user_by_username_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_login():

    returned_user1 = schema_user.SchemaUserDisplay(
        id=uuid.uuid4(),
        username="testuser1",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )

    mock_select_user_by_username_and_password_func = AsyncMock()
    mock_select_user_by_username_and_password_func.return_value = returned_user1
    user = await app_ops_user.login(
        "testuser1",
        "testuser1",
        select_user_by_username_and_password_func=mock_select_user_by_username_and_password_func,
    )
    mock_select_user_by_username_and_password_func.assert_awaited_once()
    assert isinstance(user, schema_user.SchemaUserDisplay)
    assert user.id == returned_user1.id


@pytest.mark.asyncio
async def test_login_incorrect_creds():

    mock_select_user_by_username_and_password_func = AsyncMock()
    mock_select_user_by_username_and_password_func.return_value = None
    user = await app_ops_user.login(
        "testuser1",
        "testuser1",
        select_user_by_username_and_password_func=mock_select_user_by_username_and_password_func,
    )
    mock_select_user_by_username_and_password_func.assert_awaited_once()
    assert user is None


@pytest.mark.asyncio
async def test_login_no_username():
    mock_select_user_by_username_and_password_func = AsyncMock()
    await app_ops_user.login(
        "",
        "testuser1",
        select_user_by_username_and_password_func=mock_select_user_by_username_and_password_func,
    )
    mock_select_user_by_username_and_password_func.assert_not_called()


@pytest.mark.asyncio
async def test_login_no_password():
    mock_select_user_by_username_and_password_func = AsyncMock()
    await app_ops_user.login(
        "testuser1",
        "",
        select_user_by_username_and_password_func=mock_select_user_by_username_and_password_func,
    )
    mock_select_user_by_username_and_password_func.assert_not_called()


@pytest.mark.asyncio
async def test_login_persistence_error():
    mock_select_user_by_username_and_password_func = AsyncMock()
    mock_select_user_by_username_and_password_func.side_effect = (
        PersistenceOpsBaseError()
    )
    with pytest.raises(LoginError):
        await app_ops_user.login(
            "testuser1",
            "testuser1",
            select_user_by_username_and_password_func=mock_select_user_by_username_and_password_func,
        )
    mock_select_user_by_username_and_password_func.assert_awaited_once()
