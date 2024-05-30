import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from src.persistence.database.models.db_menu import DbMenu
from src.persistence.database.ops import db_batch_ops_menu
from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)
from src.schemas import schema_menu
from tests.persistence.database.ops.mock_utils import mock_async_session_scope_factory


@pytest.mark.asyncio
async def test_insert_menu():
    request = schema_menu.SchemaMenuCreate(name="testmenu")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_insert_menu_func = AsyncMock(
        return_value=DbMenu(
            id=uuid.uuid4(),
            name=request.name,
            created_on=datetime.now(),
            last_updated_on=datetime.now(),
        )
    )

    new_menu = await db_batch_ops_menu.insert_menu(
        request,
        async_session_scope_func=mock_async_session_scope,
        insert_menu_func=mock_insert_menu_func,
    )
    assert isinstance(new_menu, schema_menu.SchemaMenuDisplay)
    mock_insert_menu_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_awaited_once()
    mock_async_session.rollback.assert_not_called()


@pytest.mark.asyncio
async def test_insert_menu_db_error():
    request = schema_menu.SchemaMenuCreate(name="testmenu")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()
    mock_insert_menu_func = AsyncMock()
    mock_insert_menu_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_menu.insert_menu(
            request,
            async_session_scope_func=mock_async_session_scope,
            insert_menu_func=mock_insert_menu_func,
        )

    mock_insert_menu_func.assert_awaited_once()
    mock_async_session.commit.assert_not_called()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_menu():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_delete_menu_func = AsyncMock(return_value=1)

    rowcount = await db_batch_ops_menu.delete_menu(
        uuid.uuid4(),
        async_session_scope_func=mock_async_session_scope,
        delete_menu_func=mock_delete_menu_func,
    )
    mock_delete_menu_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 1


@pytest.mark.asyncio
async def test_delete_menu_db_error():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_delete_menu_func = AsyncMock(return_value=1)
    mock_delete_menu_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_menu.delete_menu(
            uuid.uuid4(),
            async_session_scope_func=mock_async_session_scope,
            delete_menu_func=mock_delete_menu_func,
        )
    mock_delete_menu_func.assert_awaited_once()
    mock_async_session.commit.assert_not_called()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_menu_no_rows_affected():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_delete_menu_func = AsyncMock(return_value=0)

    rowcount = await db_batch_ops_menu.delete_menu(
        uuid.uuid4(),
        async_session_scope_func=mock_async_session_scope,
        delete_menu_func=mock_delete_menu_func,
    )
    mock_delete_menu_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 0


@pytest.mark.asyncio
async def test_delete_menu_multiple_rows_affected():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_delete_menu_func = AsyncMock(return_value=5)

    rowcount = await db_batch_ops_menu.delete_menu(
        uuid.uuid4(),
        async_session_scope_func=mock_async_session_scope,
        delete_menu_func=mock_delete_menu_func,
    )
    mock_delete_menu_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 5


@pytest.mark.asyncio
async def test_update_name():
    request = schema_menu.SchemaUpdateName(name="NewMenu")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_name_func = AsyncMock(return_value=1)

    rowcount = await db_batch_ops_menu.update_name(
        uuid.uuid4(),
        request,
        async_session_scope_func=mock_async_session_scope,
        update_name_func=mock_update_name_func,
    )
    mock_update_name_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 1


@pytest.mark.asyncio
async def test_update_name_db_error():
    request = schema_menu.SchemaUpdateName(name="NewMenu")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_name_func = AsyncMock(return_value=1)
    mock_update_name_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_menu.update_name(
            uuid.uuid4(),
            request,
            async_session_scope_func=mock_async_session_scope,
            update_name_func=mock_update_name_func,
        )
    mock_update_name_func.assert_awaited_once()
    mock_async_session.commit.assert_not_called()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_name_no_rows_affected():
    request = schema_menu.SchemaUpdateName(name="NewMenu")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_name_func = AsyncMock(return_value=0)

    rowcount = await db_batch_ops_menu.update_name(
        uuid.uuid4(),
        request,
        async_session_scope_func=mock_async_session_scope,
        update_name_func=mock_update_name_func,
    )
    mock_update_name_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 0


@pytest.mark.asyncio
async def test_update_name_multiple_rows_affected():
    request = schema_menu.SchemaUpdateName(name="NewMenu")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_name_func = AsyncMock(return_value=5)

    rowcount = await db_batch_ops_menu.update_name(
        uuid.uuid4(),
        request,
        async_session_scope_func=mock_async_session_scope,
        update_name_func=mock_update_name_func,
    )
    mock_update_name_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 5


@pytest.mark.asyncio
async def test_select_menu_list():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    returned_menu1 = DbMenu(
        id=uuid.uuid4(),
        name="menu1",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )
    returned_menu2 = DbMenu(
        id=uuid.uuid4(),
        name="menu2",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )
    mock_select_menu_list_func = AsyncMock()
    mock_select_menu_list_func = AsyncMock(
        return_value=[returned_menu1, returned_menu2]
    )

    menus = await db_batch_ops_menu.select_menu_list(
        0,
        3,
        "created_on DESC, name",
        async_session_scope_func=mock_async_session_scope,
        select_menu_list_func=mock_select_menu_list_func,
    )
    mock_select_menu_list_func.assert_awaited_once()
    assert len(menus) == 2
    assert all(isinstance(menu, schema_menu.SchemaMenuDisplay) for menu in menus)


@pytest.mark.asyncio
async def test_select_menu_list_db_error():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_select_menu_list_func = AsyncMock()
    mock_select_menu_list_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_menu.select_menu_list(
            0,
            3,
            "created_on DESC, name",
            async_session_scope_func=mock_async_session_scope,
            select_menu_list_func=mock_select_menu_list_func,
        )
    mock_select_menu_list_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_select_menu_by_id():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    returned_menu1 = DbMenu(
        id=uuid.uuid4(),
        name="testmenu1",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )
    mock_select_menu_by_id_func = AsyncMock()
    mock_select_menu_by_id_func.return_value = returned_menu1

    menu = await db_batch_ops_menu.select_menu_by_id(
        uuid.uuid4(),
        async_session_scope_func=mock_async_session_scope,
        select_menu_by_id_func=mock_select_menu_by_id_func,
    )
    mock_select_menu_by_id_func.assert_awaited_once()
    assert isinstance(menu, schema_menu.SchemaMenuDisplay)
    assert menu.id == returned_menu1.id


@pytest.mark.asyncio
async def test_select_menu_by_id_not_found():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_select_menu_by_id_func = AsyncMock()
    mock_select_menu_by_id_func.return_value = None

    menu = await db_batch_ops_menu.select_menu_by_id(
        uuid.uuid4(),
        async_session_scope_func=mock_async_session_scope,
        select_menu_by_id_func=mock_select_menu_by_id_func,
    )
    mock_select_menu_by_id_func.assert_awaited_once()
    assert menu is None


@pytest.mark.asyncio
async def test_select_menu_by_id_db_error():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_select_menu_by_id_func = AsyncMock()
    mock_select_menu_by_id_func.return_value = None
    mock_select_menu_by_id_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_menu.select_menu_by_id(
            uuid.uuid4(),
            async_session_scope_func=mock_async_session_scope,
            select_menu_by_id_func=mock_select_menu_by_id_func,
        )
    mock_select_menu_by_id_func.assert_awaited_once()
