import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from src.persistence.database.models.db_tag import DbTag
from src.persistence.database.ops import db_batch_ops_tag
from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)
from src.schemas import schema_tag
from tests.persistence.database.ops.mock_utils import mock_async_session_scope_factory


@pytest.mark.asyncio
async def test_insert_tag():
    request = schema_tag.SchemaTagCreate(name="testtag")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_insert_tag_func = AsyncMock(
        return_value=DbTag(
            id=uuid.uuid4(),
            name=request.name,
            created_on=datetime.now(),
            last_updated_on=datetime.now(),
        )
    )

    new_tag = await db_batch_ops_tag.insert_tag(
        request,
        async_session_scope_func=mock_async_session_scope,
        insert_tag_func=mock_insert_tag_func,
    )
    assert isinstance(new_tag, schema_tag.SchemaTagDisplay)
    mock_insert_tag_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_awaited_once()
    mock_async_session.rollback.assert_not_called()


@pytest.mark.asyncio
async def test_insert_tag_db_error():
    request = schema_tag.SchemaTagCreate(name="testtag")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()
    mock_insert_tag_func = AsyncMock()
    mock_insert_tag_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_tag.insert_tag(
            request,
            async_session_scope_func=mock_async_session_scope,
            insert_tag_func=mock_insert_tag_func,
        )

    mock_insert_tag_func.assert_awaited_once()
    mock_async_session.commit.assert_not_called()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_tag():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_delete_tag_func = AsyncMock(return_value=1)

    rowcount = await db_batch_ops_tag.delete_tag(
        uuid.uuid4(),
        async_session_scope_func=mock_async_session_scope,
        delete_tag_func=mock_delete_tag_func,
    )
    mock_delete_tag_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 1


@pytest.mark.asyncio
async def test_delete_tag_db_error():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_delete_tag_func = AsyncMock(return_value=1)
    mock_delete_tag_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_tag.delete_tag(
            uuid.uuid4(),
            async_session_scope_func=mock_async_session_scope,
            delete_tag_func=mock_delete_tag_func,
        )
    mock_delete_tag_func.assert_awaited_once()
    mock_async_session.commit.assert_not_called()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_tag_no_rows_affected():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_delete_tag_func = AsyncMock(return_value=0)

    rowcount = await db_batch_ops_tag.delete_tag(
        uuid.uuid4(),
        async_session_scope_func=mock_async_session_scope,
        delete_tag_func=mock_delete_tag_func,
    )
    mock_delete_tag_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 0


@pytest.mark.asyncio
async def test_delete_tag_multiple_rows_affected():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_delete_tag_func = AsyncMock(return_value=5)

    rowcount = await db_batch_ops_tag.delete_tag(
        uuid.uuid4(),
        async_session_scope_func=mock_async_session_scope,
        delete_tag_func=mock_delete_tag_func,
    )
    mock_delete_tag_func.assert_awaited_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_not_called()
    mock_async_session.rollback.assert_not_called()
    assert rowcount == 5


@pytest.mark.asyncio
async def test_update_name():
    request = schema_tag.SchemaUpdateName(name="NewTag")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_name_func = AsyncMock(return_value=1)

    rowcount = await db_batch_ops_tag.update_name(
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
    request = schema_tag.SchemaUpdateName(name="NewTag")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_name_func = AsyncMock(return_value=1)
    mock_update_name_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_tag.update_name(
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
    request = schema_tag.SchemaUpdateName(name="NewTag")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_name_func = AsyncMock(return_value=0)

    rowcount = await db_batch_ops_tag.update_name(
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
    request = schema_tag.SchemaUpdateName(name="NewTag")
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_update_name_func = AsyncMock(return_value=5)

    rowcount = await db_batch_ops_tag.update_name(
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
async def test_select_tag_list():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    returned_tag1 = DbTag(
        id=uuid.uuid4(),
        name="tag1",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )
    returned_tag2 = DbTag(
        id=uuid.uuid4(),
        name="tag2",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )
    mock_select_tag_list_func = AsyncMock()
    mock_select_tag_list_func = AsyncMock(return_value=[returned_tag1, returned_tag2])

    tags = await db_batch_ops_tag.select_tag_list(
        0,
        3,
        "created_on DESC, name",
        async_session_scope_func=mock_async_session_scope,
        select_tag_list_func=mock_select_tag_list_func,
    )
    mock_select_tag_list_func.assert_awaited_once()
    assert len(tags) == 2
    assert all(isinstance(tag, schema_tag.SchemaTagDisplay) for tag in tags)


@pytest.mark.asyncio
async def test_select_tag_list_db_error():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_select_tag_list_func = AsyncMock()
    mock_select_tag_list_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_tag.select_tag_list(
            0,
            3,
            "created_on DESC, name",
            async_session_scope_func=mock_async_session_scope,
            select_tag_list_func=mock_select_tag_list_func,
        )
    mock_select_tag_list_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_select_tag_by_id():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    returned_tag1 = DbTag(
        id=uuid.uuid4(),
        name="testtag1",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )
    mock_select_tag_by_id_func = AsyncMock()
    mock_select_tag_by_id_func.return_value = returned_tag1

    tag = await db_batch_ops_tag.select_tag_by_id(
        uuid.uuid4(),
        async_session_scope_func=mock_async_session_scope,
        select_tag_by_id_func=mock_select_tag_by_id_func,
    )
    mock_select_tag_by_id_func.assert_awaited_once()
    assert isinstance(tag, schema_tag.SchemaTagDisplay)
    assert tag.id == returned_tag1.id


@pytest.mark.asyncio
async def test_select_tag_by_id_not_found():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_select_tag_by_id_func = AsyncMock()
    mock_select_tag_by_id_func.return_value = None

    tag = await db_batch_ops_tag.select_tag_by_id(
        uuid.uuid4(),
        async_session_scope_func=mock_async_session_scope,
        select_tag_by_id_func=mock_select_tag_by_id_func,
    )
    mock_select_tag_by_id_func.assert_awaited_once()
    assert tag is None


@pytest.mark.asyncio
async def test_select_tag_by_id_db_error():
    mock_async_session_scope, mock_async_session = mock_async_session_scope_factory()

    mock_select_tag_by_id_func = AsyncMock()
    mock_select_tag_by_id_func.return_value = None
    mock_select_tag_by_id_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(PersistenceOpsBaseError):
        await db_batch_ops_tag.select_tag_by_id(
            uuid.uuid4(),
            async_session_scope_func=mock_async_session_scope,
            select_tag_by_id_func=mock_select_tag_by_id_func,
        )
    mock_select_tag_by_id_func.assert_awaited_once()
