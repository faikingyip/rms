import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from src.app.ops import app_ops_dining_table
from src.app.ops.exceptions.app_ops_exceptions import (
    CreateDiningTableError,
    DeleteDiningTableError,
    GetDiningTableListError,
    UpdateNameError,
    UpdatePositionError,
    UpdateSizeError,
)
from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)
from src.schemas import schema_dining_table


def test_validate_dining_table_name():
    try:
        app_ops_dining_table.validate_dining_table_name("valid")
    except ValueError:
        pytest.fail("Error was raised unexpectedly.")


def test_validate_dining_table_name_not_provided():
    with pytest.raises(ValueError, match="Dining table name not provided."):
        app_ops_dining_table.validate_dining_table_name("")


def test_validate_dining_table_name_whitespace_only():
    with pytest.raises(ValueError, match="Invalid dining table name format."):
        app_ops_dining_table.validate_dining_table_name("     ")


@pytest.mark.asyncio
async def test_create_dining_table():
    request = schema_dining_table.SchemaDiningTableCreate(
        name="table1", x=2, y=3, width=50, height=60
    )
    mock_insert_dining_table_func = AsyncMock(
        return_value=schema_dining_table.SchemaDiningTableDisplay(
            id=uuid.uuid4(),
            name="table1",
            x=2,
            y=3,
            width=50,
            height=60,
            created_on=datetime.now(),
            last_updated_on=datetime.now(),
        )
    )
    new_dining_table = await app_ops_dining_table.create_dining_table(
        request, insert_dining_table_func=mock_insert_dining_table_func
    )
    mock_insert_dining_table_func.assert_called_once()
    assert isinstance(new_dining_table, schema_dining_table.SchemaDiningTableDisplay)


@pytest.mark.asyncio
async def test_create_dining_table_invalid_name_format():
    request = schema_dining_table.SchemaDiningTableCreate(
        name="    ", x=2, y=3, width=50, height=60
    )
    mock_insert_dining_table_func = AsyncMock()
    with pytest.raises(
        CreateDiningTableError, match="Invalid dining table name format."
    ):
        await app_ops_dining_table.create_dining_table(
            request, insert_dining_table_func=mock_insert_dining_table_func
        )
    mock_insert_dining_table_func.assert_not_called()


@pytest.mark.asyncio
async def test_create_dining_table_persistence_error():
    request = schema_dining_table.SchemaDiningTableCreate(
        name="table1", x=2, y=3, width=50, height=60
    )
    mock_insert_dining_table_func = AsyncMock()
    mock_insert_dining_table_func.side_effect = PersistenceOpsBaseError()
    with pytest.raises(CreateDiningTableError):
        await app_ops_dining_table.create_dining_table(
            request, insert_dining_table_func=mock_insert_dining_table_func
        )
    mock_insert_dining_table_func.assert_called_once()


@pytest.mark.asyncio
async def test_delete_dining_table():
    mock_delete_dining_table_func = AsyncMock(return_value=1)
    await app_ops_dining_table.delete_dining_table(
        uuid.uuid4(), delete_dining_table_func=mock_delete_dining_table_func
    )
    mock_delete_dining_table_func.assert_called_once()


@pytest.mark.asyncio
async def test_delete_dining_table_persistence_error():
    mock_delete_dining_table_func = AsyncMock(return_value=1)
    mock_delete_dining_table_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(DeleteDiningTableError):
        await app_ops_dining_table.delete_dining_table(
            uuid.uuid4(), delete_dining_table_func=mock_delete_dining_table_func
        )
    mock_delete_dining_table_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_dining_table_no_rows_affected():
    mock_delete_dining_table_func = AsyncMock(return_value=0)
    with pytest.raises(DeleteDiningTableError, match="No rows were affected."):
        await app_ops_dining_table.delete_dining_table(
            uuid.uuid4(), delete_dining_table_func=mock_delete_dining_table_func
        )
    mock_delete_dining_table_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_dining_table_more_than_one_row_affected():
    mock_delete_dining_table_func = AsyncMock(return_value=2)
    with pytest.raises(DeleteDiningTableError, match="More than 1 row was affected."):
        await app_ops_dining_table.delete_dining_table(
            uuid.uuid4(), delete_dining_table_func=mock_delete_dining_table_func
        )
    mock_delete_dining_table_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_position():
    request = schema_dining_table.SchemaUpdatePosition(x=5, y=10)
    mock_update_position_func = AsyncMock(return_value=1)
    await app_ops_dining_table.update_position(
        uuid.uuid4(), request, update_position_func=mock_update_position_func
    )
    mock_update_position_func.assert_called_once()


@pytest.mark.asyncio
async def test_update_position_persistence_error():
    request = schema_dining_table.SchemaUpdatePosition(x=5, y=10)
    mock_update_position_func = AsyncMock(return_value=1)
    mock_update_position_func.side_effect = PersistenceOpsBaseError()
    with pytest.raises(UpdatePositionError):
        await app_ops_dining_table.update_position(
            uuid.uuid4(), request, update_position_func=mock_update_position_func
        )
    mock_update_position_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_position_no_rows_affected():
    request = schema_dining_table.SchemaUpdatePosition(x=5, y=10)
    mock_update_position_func = AsyncMock(return_value=0)
    with pytest.raises(UpdatePositionError, match="No rows were affected."):
        await app_ops_dining_table.update_position(
            uuid.uuid4(), request, update_position_func=mock_update_position_func
        )
    mock_update_position_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_position_multiple_rows_affected():
    request = schema_dining_table.SchemaUpdatePosition(x=5, y=10)
    mock_update_position_func = AsyncMock(return_value=2)
    with pytest.raises(UpdatePositionError, match="More than 1 row was affected."):
        await app_ops_dining_table.update_position(
            uuid.uuid4(), request, update_position_func=mock_update_position_func
        )
    mock_update_position_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_size():
    request = schema_dining_table.SchemaUpdateSize(width=50, height=100)
    mock_update_size_func = AsyncMock(return_value=1)
    await app_ops_dining_table.update_size(
        uuid.uuid4(), request, update_size_func=mock_update_size_func
    )
    mock_update_size_func.assert_called_once()


@pytest.mark.asyncio
async def test_update_size_persistence_error():
    request = schema_dining_table.SchemaUpdateSize(width=50, height=100)
    mock_update_size_func = AsyncMock(return_value=1)
    mock_update_size_func.side_effect = PersistenceOpsBaseError()
    with pytest.raises(UpdateSizeError):
        await app_ops_dining_table.update_size(
            uuid.uuid4(), request, update_size_func=mock_update_size_func
        )
    mock_update_size_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_size_no_rows_affected():
    request = schema_dining_table.SchemaUpdateSize(width=50, height=100)
    mock_update_size_func = AsyncMock(return_value=0)
    with pytest.raises(UpdateSizeError, match="No rows were affected."):
        await app_ops_dining_table.update_size(
            uuid.uuid4(), request, update_size_func=mock_update_size_func
        )
    mock_update_size_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_size_multiple_rows_affected():
    request = schema_dining_table.SchemaUpdateSize(width=50, height=100)
    mock_update_size_func = AsyncMock(return_value=2)
    with pytest.raises(UpdateSizeError, match="More than 1 row was affected."):
        await app_ops_dining_table.update_size(
            uuid.uuid4(), request, update_size_func=mock_update_size_func
        )
    mock_update_size_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_name():
    request = schema_dining_table.SchemaUpdateName(name="NewTableName")
    mock_update_name_func = AsyncMock(return_value=1)
    await app_ops_dining_table.update_name(
        uuid.uuid4(), request, update_name_func=mock_update_name_func
    )
    mock_update_name_func.assert_called_once()


@pytest.mark.asyncio
async def test_update_name_invalid_name_format():
    request = schema_dining_table.SchemaUpdateName(name="     ")
    mock_update_name_func = AsyncMock(return_value=1)
    with pytest.raises(UpdateNameError, match="Invalid dining table name format."):
        await app_ops_dining_table.update_name(
            uuid.uuid4(), request, update_name_func=mock_update_name_func
        )
    mock_update_name_func.assert_not_called()


@pytest.mark.asyncio
async def test_update_name_persistence_error():
    request = schema_dining_table.SchemaUpdateName(name="NewTableName")
    mock_update_name_func = AsyncMock(return_value=1)
    mock_update_name_func.side_effect = PersistenceOpsBaseError()
    with pytest.raises(UpdateNameError):
        await app_ops_dining_table.update_name(
            uuid.uuid4(), request, update_name_func=mock_update_name_func
        )
    mock_update_name_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_name_no_rows_affected():
    request = schema_dining_table.SchemaUpdateName(name="NewTableName")
    mock_update_name_func = AsyncMock(return_value=0)
    with pytest.raises(UpdateNameError, match="No rows were affected."):
        await app_ops_dining_table.update_name(
            uuid.uuid4(), request, update_name_func=mock_update_name_func
        )
    mock_update_name_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_name_multiple_rows_affected():
    request = schema_dining_table.SchemaUpdateName(name="NewTableName")
    mock_update_name_func = AsyncMock(return_value=2)
    with pytest.raises(UpdateNameError, match="More than 1 row was affected."):
        await app_ops_dining_table.update_name(
            uuid.uuid4(), request, update_name_func=mock_update_name_func
        )
    mock_update_name_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_dining_table_list():

    returned_dining_table1 = schema_dining_table.SchemaDiningTableDisplay(
        id=uuid.uuid4(),
        name="diningtable1",
        x=2,
        y=3,
        width=50,
        height=50,
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )

    returned_dining_table2 = schema_dining_table.SchemaDiningTableDisplay(
        id=uuid.uuid4(),
        name="diningtable2",
        x=2,
        y=3,
        width=50,
        height=50,
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )

    mock_select_dining_table_list_func = AsyncMock()
    mock_select_dining_table_list_func.return_value = [
        returned_dining_table1,
        returned_dining_table2,
    ]

    results = await app_ops_dining_table.get_dining_table_list(
        0,
        10,
        "created_on DESC, name",
        select_dining_table_list_func=mock_select_dining_table_list_func,
    )
    mock_select_dining_table_list_func.assert_awaited_once()
    assert len(results) == 2
    assert all(
        isinstance(item, schema_dining_table.SchemaDiningTableDisplay)
        for item in results
    )


@pytest.mark.asyncio
async def test_get_dining_table_list_invalid_page_index():

    mock_select_dining_table_list_func = AsyncMock()
    with pytest.raises(GetDiningTableListError):
        await app_ops_dining_table.get_dining_table_list(
            -1,
            10,
            "created_on DESC, name",
            select_dining_table_list_func=mock_select_dining_table_list_func,
        )
    mock_select_dining_table_list_func.assert_not_called()


@pytest.mark.asyncio
async def test_get_dining_table_list_invalid_page_size():

    mock_select_dining_table_list_func = AsyncMock()
    with pytest.raises(GetDiningTableListError):
        await app_ops_dining_table.get_dining_table_list(
            0,
            0,
            "created_on DESC, name",
            select_dining_table_list_func=mock_select_dining_table_list_func,
        )
    mock_select_dining_table_list_func.assert_not_called()


@pytest.mark.asyncio
async def test_get_dining_table_list_persistence_error():

    mock_select_dining_table_list_func = AsyncMock()
    mock_select_dining_table_list_func.side_effect = PersistenceOpsBaseError()
    with pytest.raises(GetDiningTableListError):
        await app_ops_dining_table.get_dining_table_list(
            0,
            10,
            "created_on DESC, name",
            select_dining_table_list_func=mock_select_dining_table_list_func,
        )
    mock_select_dining_table_list_func.assert_awaited_once()
