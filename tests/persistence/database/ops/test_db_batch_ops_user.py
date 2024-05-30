import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from src.persistence.database.models.db_user import DbUser
from src.persistence.database.ops import db_batch_ops_user
from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)
from src.schemas import schema_user
from src.utils import bcrypt_hash
from tests.persistence.database.ops.mock_utils import mock_async_session_scope_factory


@pytest.mark.asyncio
async def test_insert_user():
    request = schema_user.SchemaUserCreate(username="testuser", password="testuser")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_insert_user_func = AsyncMock(
        return_value=DbUser(
            id=uuid.uuid4(),
            username=request.username,
            password_hash=bcrypt_hash.bcrypt(request.password),
            created_on=datetime.now(),
            last_updated_on=datetime.now(),
        )
    )

    new_user = await db_batch_ops_user.insert_user(
        request,
        async_session_scope_func=mock_async_session_scope,
        insert_user_func=mock_insert_user_func,
    )
    assert isinstance(new_user, schema_user.SchemaUserDisplay)
    mock_insert_user_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_awaited_once()
    mock_async_session.rollback.assert_not_called()


@pytest.mark.asyncio
async def test_insert_user_db_error():
    request = schema_user.SchemaUserCreate(username="testuser", password="testuser")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()
    mock_insert_user_func = AsyncMock()
    mock_insert_user_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_user.insert_user(
            request,
            async_session_scope_func=mock_async_session_scope,
            insert_user_func=mock_insert_user_func,
        )

    mock_insert_user_func.assert_awaited_once()
    mock_async_session.commit.assert_not_called()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_user():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_delete_user_func = AsyncMock(return_value=1)

    rowcount = await db_batch_ops_user.delete_user(
        uuid.uuid4(),
        async_session_scope_func=mock_async_session_scope,
        delete_user_func=mock_delete_user_func,
    )
    mock_delete_user_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 1


@pytest.mark.asyncio
async def test_delete_user_db_error():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_delete_user_func = AsyncMock(return_value=1)
    mock_delete_user_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_user.delete_user(
            uuid.uuid4(),
            async_session_scope_func=mock_async_session_scope,
            delete_user_func=mock_delete_user_func,
        )
    mock_delete_user_func.assert_awaited_once()
    mock_async_session.commit.assert_not_called()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_user_no_rows_affected():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_delete_user_func = AsyncMock(return_value=0)

    rowcount = await db_batch_ops_user.delete_user(
        uuid.uuid4(),
        async_session_scope_func=mock_async_session_scope,
        delete_user_func=mock_delete_user_func,
    )
    mock_delete_user_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 0


@pytest.mark.asyncio
async def test_delete_user_multiple_rows_affected():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_delete_user_func = AsyncMock(return_value=5)

    rowcount = await db_batch_ops_user.delete_user(
        uuid.uuid4(),
        async_session_scope_func=mock_async_session_scope,
        delete_user_func=mock_delete_user_func,
    )
    mock_delete_user_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 5


@pytest.mark.asyncio
async def test_update_password():
    request = schema_user.SchemaChangePassword(new_password="new_password")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_password_func = AsyncMock(return_value=1)

    rowcount = await db_batch_ops_user.update_password(
        uuid.uuid4(),
        request,
        async_session_scope_func=mock_async_session_scope,
        update_password_func=mock_update_password_func,
    )
    mock_update_password_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 1


@pytest.mark.asyncio
async def test_update_password_db_error():
    request = schema_user.SchemaChangePassword(new_password="new_password")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_password_func = AsyncMock(return_value=1)
    mock_update_password_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_user.update_password(
            uuid.uuid4(),
            request,
            async_session_scope_func=mock_async_session_scope,
            update_password_func=mock_update_password_func,
        )
    mock_update_password_func.assert_awaited_once()
    mock_async_session.commit.assert_not_called()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_password_no_rows_affected():
    request = schema_user.SchemaChangePassword(new_password="new_password")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_password_func = AsyncMock(return_value=0)

    rowcount = await db_batch_ops_user.update_password(
        uuid.uuid4(),
        request,
        async_session_scope_func=mock_async_session_scope,
        update_password_func=mock_update_password_func,
    )
    mock_update_password_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 0


@pytest.mark.asyncio
async def test_update_password_multiple_rows_affected():
    request = schema_user.SchemaChangePassword(new_password="new_password")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_password_func = AsyncMock(return_value=5)

    rowcount = await db_batch_ops_user.update_password(
        uuid.uuid4(),
        request,
        async_session_scope_func=mock_async_session_scope,
        update_password_func=mock_update_password_func,
    )
    mock_update_password_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 5


@pytest.mark.asyncio
async def test_select_user_list():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    returned_user1 = DbUser(
        id=uuid.uuid4(),
        username="testuser1",
        password_hash="$2b$12$T3FpoaPSJEdOzWgNvsw24e.cXsTDyh0hme//6VD0qhpKXzmq52FWy",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )
    returned_user2 = DbUser(
        id=uuid.uuid4(),
        username="testuser1",
        password_hash="$2b$12$T3FpoaPSJEdOzWgNvsw24e.cXsTDyh0hme//6VD0qhpKXzmq52FWy",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )
    mock_select_user_list_func = AsyncMock()
    mock_select_user_list_func = AsyncMock(
        return_value=[returned_user1, returned_user2]
    )

    users = await db_batch_ops_user.select_user_list(
        0,
        3,
        "created_on DESC, username",
        async_session_scope_func=mock_async_session_scope,
        select_user_list_func=mock_select_user_list_func,
    )
    mock_select_user_list_func.assert_awaited_once()
    assert len(users) == 2
    assert all(isinstance(user, schema_user.SchemaUserDisplay) for user in users)


@pytest.mark.asyncio
async def test_select_user_list_db_error():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_select_user_list_func = AsyncMock()
    mock_select_user_list_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_user.select_user_list(
            0,
            3,
            "created_on DESC, username",
            async_session_scope_func=mock_async_session_scope,
            select_user_list_func=mock_select_user_list_func,
        )
    mock_select_user_list_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_select_user_by_id():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    returned_user1 = DbUser(
        id=uuid.uuid4(),
        username="testuser1",
        password_hash="$2b$12$T3FpoaPSJEdOzWgNvsw24e.cXsTDyh0hme//6VD0qhpKXzmq52FWy",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )
    mock_select_user_by_id_func = AsyncMock()
    mock_select_user_by_id_func.return_value = returned_user1

    user = await db_batch_ops_user.select_user_by_id(
        uuid.uuid4(),
        async_session_scope_func=mock_async_session_scope,
        select_user_by_id_func=mock_select_user_by_id_func,
    )
    mock_select_user_by_id_func.assert_awaited_once()
    assert isinstance(user, schema_user.SchemaUserDisplay)
    assert user.id == returned_user1.id


@pytest.mark.asyncio
async def test_select_user_by_id_not_found():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_select_user_by_id_func = AsyncMock()
    mock_select_user_by_id_func.return_value = None

    user = await db_batch_ops_user.select_user_by_id(
        uuid.uuid4(),
        async_session_scope_func=mock_async_session_scope,
        select_user_by_id_func=mock_select_user_by_id_func,
    )
    mock_select_user_by_id_func.assert_awaited_once()
    assert user is None


@pytest.mark.asyncio
async def test_select_user_by_id_db_error():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_select_user_by_id_func = AsyncMock()
    mock_select_user_by_id_func.return_value = None
    mock_select_user_by_id_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_user.select_user_by_id(
            uuid.uuid4(),
            async_session_scope_func=mock_async_session_scope,
            select_user_by_id_func=mock_select_user_by_id_func,
        )
    mock_select_user_by_id_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_select_user_by_username():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    returned_user1 = DbUser(
        id=uuid.uuid4(),
        username="testuser1",
        password_hash="$2b$12$T3FpoaPSJEdOzWgNvsw24e.cXsTDyh0hme//6VD0qhpKXzmq52FWy",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )
    mock_select_user_by_username_func = AsyncMock()
    mock_select_user_by_username_func.return_value = returned_user1

    user = await db_batch_ops_user.select_user_by_username(
        "testuser",
        async_session_scope_func=mock_async_session_scope,
        select_user_by_username_func=mock_select_user_by_username_func,
    )
    mock_select_user_by_username_func.assert_awaited_once()
    assert isinstance(user, schema_user.SchemaUserDisplay)
    assert user.id == returned_user1.id


@pytest.mark.asyncio
async def test_select_user_by_username_not_found():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_select_user_by_username_func = AsyncMock()
    mock_select_user_by_username_func.return_value = None

    user = await db_batch_ops_user.select_user_by_username(
        "testuser",
        async_session_scope_func=mock_async_session_scope,
        select_user_by_username_func=mock_select_user_by_username_func,
    )
    mock_select_user_by_username_func.assert_awaited_once()
    assert user is None


@pytest.mark.asyncio
async def test_select_user_by_username_db_error():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_select_user_by_username_func = AsyncMock()
    mock_select_user_by_username_func.return_value = None
    mock_select_user_by_username_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_user.select_user_by_username(
            "testuser",
            async_session_scope_func=mock_async_session_scope,
            select_user_by_username_func=mock_select_user_by_username_func,
        )
    mock_select_user_by_username_func.assert_awaited_once()


PASSWORD_1 = "testuser"
PASSWORD_HASH_1 = "$2b$12$W2mtHgJw7s0JOvQgyqG.w.uK90ZgkTQbAEGRXjbYbc6RNxG0akOOK"


@pytest.mark.asyncio
async def test_select_user_by_username_and_password():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    returned_user1 = DbUser(
        id=uuid.uuid4(),
        username="testuser",
        password_hash=PASSWORD_HASH_1,
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )
    mock_select_user_by_username_func = AsyncMock()
    mock_select_user_by_username_func.return_value = returned_user1

    user = await db_batch_ops_user.select_user_by_username_and_password(
        "testuser",
        PASSWORD_1,
        async_session_scope_func=mock_async_session_scope,
        select_user_by_username_func=mock_select_user_by_username_func,
    )
    mock_select_user_by_username_func.assert_awaited_once()
    assert isinstance(user, schema_user.SchemaUserDisplay)
    assert user.id == returned_user1.id


@pytest.mark.asyncio
async def test_select_user_by_username_and_password_incorrect_password():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    returned_user1 = DbUser(
        id=uuid.uuid4(),
        username="testuser",
        password_hash=PASSWORD_HASH_1,
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )
    mock_select_user_by_username_func = AsyncMock()
    mock_select_user_by_username_func.return_value = returned_user1

    user = await db_batch_ops_user.select_user_by_username_and_password(
        "testuser",
        "wrong_password",
        async_session_scope_func=mock_async_session_scope,
        select_user_by_username_func=mock_select_user_by_username_func,
    )
    mock_select_user_by_username_func.assert_awaited_once()
    assert user is None


@pytest.mark.asyncio
async def test_select_user_by_username_and_password_incorrect_username():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()
    mock_select_user_by_username_func = AsyncMock()
    mock_select_user_by_username_func.return_value = None

    user = await db_batch_ops_user.select_user_by_username_and_password(
        "testuser",
        PASSWORD_1,
        async_session_scope_func=mock_async_session_scope,
        select_user_by_username_func=mock_select_user_by_username_func,
    )
    mock_select_user_by_username_func.assert_awaited_once()
    assert user is None


@pytest.mark.asyncio
async def test_select_user_by_username_and_password_no_username():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()
    mock_select_user_by_username_func = AsyncMock()
    mock_select_user_by_username_func.return_value = None

    user = await db_batch_ops_user.select_user_by_username_and_password(
        "",
        PASSWORD_1,
        async_session_scope_func=mock_async_session_scope,
        select_user_by_username_func=mock_select_user_by_username_func,
    )
    mock_select_user_by_username_func.assert_not_called()
    assert user is None


@pytest.mark.asyncio
async def test_select_user_by_username_and_password_no_password():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()
    mock_select_user_by_username_func = AsyncMock()
    mock_select_user_by_username_func.return_value = None

    user = await db_batch_ops_user.select_user_by_username_and_password(
        "testuser",
        "",
        async_session_scope_func=mock_async_session_scope,
        select_user_by_username_func=mock_select_user_by_username_func,
    )
    mock_select_user_by_username_func.assert_not_called()
    assert user is None


@pytest.mark.asyncio
async def test_select_user_by_username_and_password_db_error():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()
    mock_select_user_by_username_func = AsyncMock()
    mock_select_user_by_username_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_user.select_user_by_username_and_password(
            "testuser",
            PASSWORD_1,
            async_session_scope_func=mock_async_session_scope,
            select_user_by_username_func=mock_select_user_by_username_func,
        )
    mock_select_user_by_username_func.assert_awaited_once()
