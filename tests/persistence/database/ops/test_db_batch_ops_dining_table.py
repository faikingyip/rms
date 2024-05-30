import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from src.persistence.database.models.db_dining_table import DbDiningTable
from src.persistence.database.ops import db_batch_ops_dining_table
from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)
from src.schemas import schema_dining_table
from tests.persistence.database.ops.mock_utils import mock_async_session_scope_factory


@pytest.mark.asyncio
async def test_insert_dining_table():
    request = schema_dining_table.SchemaDiningTableCreate(
        name="testtable", x=5, y=10, width=30, height=40
    )
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_insert_dining_table_func = AsyncMock(
        return_value=DbDiningTable(
            id=uuid.uuid4(),
            name=request.name,
            x=request.x,
            y=request.y,
            width=request.width,
            height=request.height,
            created_on=datetime.now(),
            last_updated_on=datetime.now(),
        )
    )

    new_dining_table = await db_batch_ops_dining_table.insert_dining_table(
        request,
        async_session_scope_func=mock_async_session_scope,
        insert_dining_table_func=mock_insert_dining_table_func,
    )
    assert isinstance(new_dining_table, schema_dining_table.SchemaDiningTableDisplay)
    mock_insert_dining_table_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_awaited_once()
    mock_async_session.rollback.assert_not_called()


@pytest.mark.asyncio
async def test_insert_dining_table_db_error():
    request = schema_dining_table.SchemaDiningTableCreate(
        name="testtable", x=5, y=10, width=30, height=40
    )
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()
    mock_insert_dining_table_func = AsyncMock()
    mock_insert_dining_table_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_dining_table.insert_dining_table(
            request,
            async_session_scope_func=mock_async_session_scope,
            insert_dining_table_func=mock_insert_dining_table_func,
        )

    mock_insert_dining_table_func.assert_awaited_once()
    mock_async_session.commit.assert_not_called()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_dining_table():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_delete_dining_table_func = AsyncMock(return_value=1)

    rowcount = await db_batch_ops_dining_table.delete_dining_table(
        uuid.uuid4(),
        async_session_scope_func=mock_async_session_scope,
        delete_dining_table_func=mock_delete_dining_table_func,
    )
    mock_delete_dining_table_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 1


@pytest.mark.asyncio
async def test_delete_dining_table_db_error():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_delete_dining_table_func = AsyncMock(return_value=1)
    mock_delete_dining_table_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_dining_table.delete_dining_table(
            uuid.uuid4(),
            async_session_scope_func=mock_async_session_scope,
            delete_dining_table_func=mock_delete_dining_table_func,
        )
    mock_delete_dining_table_func.assert_awaited_once()
    mock_async_session.commit.assert_not_called()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_dining_table_no_rows_affected():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_delete_dining_table_func = AsyncMock(return_value=0)

    rowcount = await db_batch_ops_dining_table.delete_dining_table(
        uuid.uuid4(),
        async_session_scope_func=mock_async_session_scope,
        delete_dining_table_func=mock_delete_dining_table_func,
    )
    mock_delete_dining_table_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 0


@pytest.mark.asyncio
async def test_delete_dining_table_multiple_rows_affected():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_delete_dining_table_func = AsyncMock(return_value=5)

    rowcount = await db_batch_ops_dining_table.delete_dining_table(
        uuid.uuid4(),
        async_session_scope_func=mock_async_session_scope,
        delete_dining_table_func=mock_delete_dining_table_func,
    )
    mock_delete_dining_table_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 5


@pytest.mark.asyncio
async def test_update_position():
    request = schema_dining_table.SchemaUpdatePosition(x=20, y=25)
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_position_func = AsyncMock(return_value=1)

    rowcount = await db_batch_ops_dining_table.update_position(
        uuid.uuid4(),
        request,
        async_session_scope_func=mock_async_session_scope,
        update_position_func=mock_update_position_func,
    )
    mock_update_position_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 1


@pytest.mark.asyncio
async def test_update_position_db_error():
    request = schema_dining_table.SchemaUpdatePosition(x=20, y=25)
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_position_func = AsyncMock(return_value=1)
    mock_update_position_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_dining_table.update_position(
            uuid.uuid4(),
            request,
            async_session_scope_func=mock_async_session_scope,
            update_position_func=mock_update_position_func,
        )
    mock_update_position_func.assert_awaited_once()
    mock_async_session.commit.assert_not_called()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_position_no_rows_affected():
    request = schema_dining_table.SchemaUpdatePosition(x=20, y=25)
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_position_func = AsyncMock(return_value=0)

    rowcount = await db_batch_ops_dining_table.update_position(
        uuid.uuid4(),
        request,
        async_session_scope_func=mock_async_session_scope,
        update_position_func=mock_update_position_func,
    )
    mock_update_position_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 0


@pytest.mark.asyncio
async def test_update_position_multiple_rows_affected():
    request = schema_dining_table.SchemaUpdatePosition(x=20, y=25)
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_position_func = AsyncMock(return_value=5)

    rowcount = await db_batch_ops_dining_table.update_position(
        uuid.uuid4(),
        request,
        async_session_scope_func=mock_async_session_scope,
        update_position_func=mock_update_position_func,
    )
    mock_update_position_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 5


@pytest.mark.asyncio
async def test_update_size():
    request = schema_dining_table.SchemaUpdateSize(width=50, height=100)
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_size_func = AsyncMock(return_value=1)

    rowcount = await db_batch_ops_dining_table.update_size(
        uuid.uuid4(),
        request,
        async_session_scope_func=mock_async_session_scope,
        update_size_func=mock_update_size_func,
    )
    mock_update_size_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 1


@pytest.mark.asyncio
async def test_update_size_db_error():
    request = schema_dining_table.SchemaUpdateSize(width=50, height=100)
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_size_func = AsyncMock(return_value=1)
    mock_update_size_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_dining_table.update_size(
            uuid.uuid4(),
            request,
            async_session_scope_func=mock_async_session_scope,
            update_size_func=mock_update_size_func,
        )
    mock_update_size_func.assert_awaited_once()
    mock_async_session.commit.assert_not_called()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_size_no_rows_affected():
    request = schema_dining_table.SchemaUpdateSize(width=50, height=100)
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_size_func = AsyncMock(return_value=0)

    rowcount = await db_batch_ops_dining_table.update_size(
        uuid.uuid4(),
        request,
        async_session_scope_func=mock_async_session_scope,
        update_size_func=mock_update_size_func,
    )
    mock_update_size_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 0


@pytest.mark.asyncio
async def test_update_size_multiple_rows_affected():
    request = schema_dining_table.SchemaUpdateSize(width=50, height=100)
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_size_func = AsyncMock(return_value=5)

    rowcount = await db_batch_ops_dining_table.update_size(
        uuid.uuid4(),
        request,
        async_session_scope_func=mock_async_session_scope,
        update_size_func=mock_update_size_func,
    )
    mock_update_size_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 5


@pytest.mark.asyncio
async def test_update_name():
    request = schema_dining_table.SchemaUpdateName(name="TableName")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_name_func = AsyncMock(return_value=1)

    rowcount = await db_batch_ops_dining_table.update_name(
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
    request = schema_dining_table.SchemaUpdateName(name="TableName")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_name_func = AsyncMock(return_value=1)
    mock_update_name_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_dining_table.update_name(
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
    request = schema_dining_table.SchemaUpdateName(name="TableName")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_name_func = AsyncMock(return_value=0)

    rowcount = await db_batch_ops_dining_table.update_name(
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
    request = schema_dining_table.SchemaUpdateName(name="TableName")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_name_func = AsyncMock(return_value=5)

    rowcount = await db_batch_ops_dining_table.update_name(
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
async def test_select_dining_table_list():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    returned_dining_table1 = DbDiningTable(
        id=uuid.uuid4(),
        name="diningtable1",
        x=5,
        y=10,
        width=100,
        height=100,
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )
    returned_dining_table2 = DbDiningTable(
        id=uuid.uuid4(),
        name="diningtable2",
        x=5,
        y=10,
        width=100,
        height=100,
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )
    mock_select_dining_table_list_func = AsyncMock()
    mock_select_dining_table_list_func = AsyncMock(
        return_value=[returned_dining_table1, returned_dining_table2]
    )

    dining_tables = await db_batch_ops_dining_table.select_dining_table_list(
        0,
        3,
        "created_on DESC, name",
        async_session_scope_func=mock_async_session_scope,
        select_dining_table_list_func=mock_select_dining_table_list_func,
    )
    mock_select_dining_table_list_func.assert_awaited_once()
    assert len(dining_tables) == 2
    assert all(
        isinstance(dining_table, schema_dining_table.SchemaDiningTableDisplay)
        for dining_table in dining_tables
    )


@pytest.mark.asyncio
async def test_select_dining_table_list_db_error():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_select_dining_table_list_func = AsyncMock()
    mock_select_dining_table_list_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_dining_table.select_dining_table_list(
            0,
            3,
            "created_on DESC, name",
            async_session_scope_func=mock_async_session_scope,
            select_dining_table_list_func=mock_select_dining_table_list_func,
        )
    mock_select_dining_table_list_func.assert_awaited_once()
