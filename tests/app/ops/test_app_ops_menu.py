import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from src.app.ops import app_ops_menu
from src.app.ops.exceptions.app_ops_exceptions import (
    CreateMenuError,
    DeleteMenuError,
    GetMenuByIdError,
    GetMenuListError,
    UpdateNameError,
)
from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)
from src.schemas import schema_menu


def test_validate_menu_name():
    try:
        app_ops_menu.validate_menu_name("valid")
    except ValueError:
        pytest.fail("Error was raised unexpectedly.")


def test_validate_menu_name_not_provided():
    with pytest.raises(ValueError, match="Menu name not provided."):
        app_ops_menu.validate_menu_name("")


def test_validate_menu_name_whitespace_only():
    with pytest.raises(ValueError, match="Invalid menu name format."):
        app_ops_menu.validate_menu_name("     ")


@pytest.mark.asyncio
async def test_create_menu():
    request = schema_menu.SchemaMenuCreate(name="menu1")
    mock_insert_menu_func = AsyncMock(
        return_value=schema_menu.SchemaMenuDisplay(
            id=uuid.uuid4(),
            name="menu1",
            created_on=datetime.now(),
            last_updated_on=datetime.now(),
        )
    )
    new_menu = await app_ops_menu.create_menu(
        request, insert_menu_func=mock_insert_menu_func
    )
    mock_insert_menu_func.assert_called_once()
    assert isinstance(new_menu, schema_menu.SchemaMenuDisplay)


@pytest.mark.asyncio
async def test_create_menu_invalid_name_format():
    request = schema_menu.SchemaMenuCreate(name="    ")
    mock_insert_menu_func = AsyncMock()
    with pytest.raises(CreateMenuError, match="Invalid menu name format."):
        await app_ops_menu.create_menu(request, insert_menu_func=mock_insert_menu_func)
    mock_insert_menu_func.assert_not_called()


@pytest.mark.asyncio
async def test_create_menu_persistence_error():
    request = schema_menu.SchemaMenuCreate(name="menu1")
    mock_insert_menu_func = AsyncMock()
    mock_insert_menu_func.side_effect = PersistenceOpsBaseError()
    with pytest.raises(CreateMenuError):
        await app_ops_menu.create_menu(request, insert_menu_func=mock_insert_menu_func)
    mock_insert_menu_func.assert_called_once()


@pytest.mark.asyncio
async def test_delete_menu():
    mock_delete_menu_func = AsyncMock(return_value=1)
    await app_ops_menu.delete_menu(uuid.uuid4(), delete_menu_func=mock_delete_menu_func)
    mock_delete_menu_func.assert_called_once()


@pytest.mark.asyncio
async def test_delete_menu_persistence_error():
    mock_delete_menu_func = AsyncMock(return_value=1)
    mock_delete_menu_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(DeleteMenuError):
        await app_ops_menu.delete_menu(
            uuid.uuid4(), delete_menu_func=mock_delete_menu_func
        )
    mock_delete_menu_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_menu_no_rows_affected():
    mock_delete_menu_func = AsyncMock(return_value=0)
    with pytest.raises(DeleteMenuError, match="No rows were affected."):
        await app_ops_menu.delete_menu(
            uuid.uuid4(), delete_menu_func=mock_delete_menu_func
        )
    mock_delete_menu_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_menu_more_than_one_row_affected():
    mock_delete_menu_func = AsyncMock(return_value=2)
    with pytest.raises(DeleteMenuError, match="More than 1 row was affected."):
        await app_ops_menu.delete_menu(
            uuid.uuid4(), delete_menu_func=mock_delete_menu_func
        )
    mock_delete_menu_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_name():
    request = schema_menu.SchemaUpdateName(name="NewMenuName")
    mock_update_name_func = AsyncMock(return_value=1)
    await app_ops_menu.update_name(
        uuid.uuid4(), request, update_name_func=mock_update_name_func
    )
    mock_update_name_func.assert_called_once()


@pytest.mark.asyncio
async def test_update_name_invalid_name_format():
    request = schema_menu.SchemaUpdateName(name="     ")
    mock_update_name_func = AsyncMock(return_value=1)
    with pytest.raises(UpdateNameError, match="Invalid menu name format."):
        await app_ops_menu.update_name(
            uuid.uuid4(), request, update_name_func=mock_update_name_func
        )
    mock_update_name_func.assert_not_called()


@pytest.mark.asyncio
async def test_update_name_persistence_error():
    request = schema_menu.SchemaUpdateName(name="NewMenuName")
    mock_update_name_func = AsyncMock(return_value=1)
    mock_update_name_func.side_effect = PersistenceOpsBaseError()
    with pytest.raises(UpdateNameError):
        await app_ops_menu.update_name(
            uuid.uuid4(), request, update_name_func=mock_update_name_func
        )
    mock_update_name_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_name_no_rows_affected():
    request = schema_menu.SchemaUpdateName(name="NewMenuName")
    mock_update_name_func = AsyncMock(return_value=0)
    with pytest.raises(UpdateNameError, match="No rows were affected."):
        await app_ops_menu.update_name(
            uuid.uuid4(), request, update_name_func=mock_update_name_func
        )
    mock_update_name_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_name_multiple_rows_affected():
    request = schema_menu.SchemaUpdateName(name="NewMenuName")
    mock_update_name_func = AsyncMock(return_value=2)
    with pytest.raises(UpdateNameError, match="More than 1 row was affected."):
        await app_ops_menu.update_name(
            uuid.uuid4(), request, update_name_func=mock_update_name_func
        )
    mock_update_name_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_menu_list():

    returned_menu1 = schema_menu.SchemaMenuDisplay(
        id=uuid.uuid4(),
        name="menu1",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )

    returned_menu2 = schema_menu.SchemaMenuDisplay(
        id=uuid.uuid4(),
        name="menu2",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )

    mock_select_menu_list_func = AsyncMock()
    mock_select_menu_list_func.return_value = [
        returned_menu1,
        returned_menu2,
    ]

    results = await app_ops_menu.get_menu_list(
        0,
        10,
        "created_on DESC, name",
        select_menu_list_func=mock_select_menu_list_func,
    )
    mock_select_menu_list_func.assert_awaited_once()
    assert len(results) == 2
    assert all(isinstance(item, schema_menu.SchemaMenuDisplay) for item in results)


@pytest.mark.asyncio
async def test_get_menu_list_invalid_page_index():

    mock_select_menu_list_func = AsyncMock()
    with pytest.raises(GetMenuListError):
        await app_ops_menu.get_menu_list(
            -1,
            10,
            "created_on DESC, name",
            select_menu_list_func=mock_select_menu_list_func,
        )
    mock_select_menu_list_func.assert_not_called()


@pytest.mark.asyncio
async def test_get_menu_list_invalid_page_size():

    mock_select_menu_list_func = AsyncMock()
    with pytest.raises(GetMenuListError):
        await app_ops_menu.get_menu_list(
            0,
            0,
            "created_on DESC, name",
            select_menu_list_func=mock_select_menu_list_func,
        )
    mock_select_menu_list_func.assert_not_called()


@pytest.mark.asyncio
async def test_get_menu_list_persistence_error():

    mock_select_menu_list_func = AsyncMock()
    mock_select_menu_list_func.side_effect = PersistenceOpsBaseError()
    with pytest.raises(GetMenuListError):
        await app_ops_menu.get_menu_list(
            0,
            10,
            "created_on DESC, name",
            select_menu_list_func=mock_select_menu_list_func,
        )
    mock_select_menu_list_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_menu_by_id():

    returned_menu1 = schema_menu.SchemaMenuDisplay(
        id=uuid.uuid4(),
        name="testmenu1",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )

    mock_select_menu_by_id_func = AsyncMock()
    mock_select_menu_by_id_func.return_value = returned_menu1
    menu = await app_ops_menu.get_menu_by_id(
        uuid.uuid4(), select_menu_by_id_func=mock_select_menu_by_id_func
    )
    mock_select_menu_by_id_func.assert_awaited_once()
    assert isinstance(menu, schema_menu.SchemaMenuDisplay)
    assert menu.id == returned_menu1.id


@pytest.mark.asyncio
async def test_get_menu_by_id_not_found():

    mock_select_menu_by_id_func = AsyncMock()
    mock_select_menu_by_id_func.return_value = None
    menu = await app_ops_menu.get_menu_by_id(
        uuid.uuid4(), select_menu_by_id_func=mock_select_menu_by_id_func
    )
    mock_select_menu_by_id_func.assert_awaited_once()
    assert menu is None


@pytest.mark.asyncio
async def test_get_menu_by_id_persistence_error():

    mock_select_menu_by_id_func = AsyncMock()
    mock_select_menu_by_id_func.side_effect = PersistenceOpsBaseError()
    with pytest.raises(GetMenuByIdError):
        await app_ops_menu.get_menu_by_id(
            uuid.uuid4(), select_menu_by_id_func=mock_select_menu_by_id_func
        )
    mock_select_menu_by_id_func.assert_awaited_once()
