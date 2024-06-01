import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from src.app.ops import app_ops_tag
from src.app.ops.exceptions.app_ops_exceptions import (CreateTagError,
                                                       DeleteTagError,
                                                       GetTagByIdError,
                                                       GetTagListError,
                                                       UpdateNameError)
from src.persistence.interface.ops.exceptions.ops_exceptions import \
    PersistenceOpsBaseError
from src.schemas import schema_tag


def test_validate_tag_name():
    try:
        app_ops_tag.validate_tag_name("valid")
    except ValueError:
        pytest.fail("Error was raised unexpectedly.")


def test_validate_tag_name_not_provided():
    with pytest.raises(ValueError, match="Tag name not provided."):
        app_ops_tag.validate_tag_name("")


def test_validate_tag_name_whitespace_only():
    with pytest.raises(ValueError, match="Invalid tag name format."):
        app_ops_tag.validate_tag_name("     ")


@pytest.mark.asyncio
async def test_create_tag():
    request = schema_tag.SchemaTagCreate(name="tag1")
    mock_insert_tag_func = AsyncMock(
        return_value=schema_tag.SchemaTagDisplay(
            id=uuid.uuid4(),
            name="tag1",
            created_on=datetime.now(),
            last_updated_on=datetime.now(),
        )
    )
    new_tag = await app_ops_tag.create_tag(
        request, insert_tag_func=mock_insert_tag_func
    )
    mock_insert_tag_func.assert_called_once()
    assert isinstance(new_tag, schema_tag.SchemaTagDisplay)


@pytest.mark.asyncio
async def test_create_tag_invalid_name_format():
    request = schema_tag.SchemaTagCreate(name="    ")
    mock_insert_tag_func = AsyncMock()
    with pytest.raises(CreateTagError, match="Invalid tag name format."):
        await app_ops_tag.create_tag(request, insert_tag_func=mock_insert_tag_func)
    mock_insert_tag_func.assert_not_called()


@pytest.mark.asyncio
async def test_create_tag_persistence_error():
    request = schema_tag.SchemaTagCreate(name="tag1")
    mock_insert_tag_func = AsyncMock()
    mock_insert_tag_func.side_effect = PersistenceOpsBaseError()
    with pytest.raises(CreateTagError):
        await app_ops_tag.create_tag(request, insert_tag_func=mock_insert_tag_func)
    mock_insert_tag_func.assert_called_once()


@pytest.mark.asyncio
async def test_delete_tag():
    mock_delete_tag_func = AsyncMock(return_value=1)
    await app_ops_tag.delete_tag(uuid.uuid4(), delete_tag_func=mock_delete_tag_func)
    mock_delete_tag_func.assert_called_once()


@pytest.mark.asyncio
async def test_delete_tag_persistence_error():
    mock_delete_tag_func = AsyncMock(return_value=1)
    mock_delete_tag_func.side_effect = PersistenceOpsBaseError()

    with pytest.raises(DeleteTagError):
        await app_ops_tag.delete_tag(uuid.uuid4(), delete_tag_func=mock_delete_tag_func)
    mock_delete_tag_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_tag_no_rows_affected():
    mock_delete_tag_func = AsyncMock(return_value=0)
    with pytest.raises(DeleteTagError, match="No rows were affected."):
        await app_ops_tag.delete_tag(uuid.uuid4(), delete_tag_func=mock_delete_tag_func)
    mock_delete_tag_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_tag_more_than_one_row_affected():
    mock_delete_tag_func = AsyncMock(return_value=2)
    with pytest.raises(DeleteTagError, match="More than 1 row was affected."):
        await app_ops_tag.delete_tag(uuid.uuid4(), delete_tag_func=mock_delete_tag_func)
    mock_delete_tag_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_name():
    request = schema_tag.SchemaUpdateName(name="NewTagName")
    mock_update_name_func = AsyncMock(return_value=1)
    await app_ops_tag.update_name(
        uuid.uuid4(), request, update_name_func=mock_update_name_func
    )
    mock_update_name_func.assert_called_once()


@pytest.mark.asyncio
async def test_update_name_invalid_name_format():
    request = schema_tag.SchemaUpdateName(name="     ")
    mock_update_name_func = AsyncMock(return_value=1)
    with pytest.raises(UpdateNameError, match="Invalid tag name format."):
        await app_ops_tag.update_name(
            uuid.uuid4(), request, update_name_func=mock_update_name_func
        )
    mock_update_name_func.assert_not_called()


@pytest.mark.asyncio
async def test_update_name_persistence_error():
    request = schema_tag.SchemaUpdateName(name="NewTagName")
    mock_update_name_func = AsyncMock(return_value=1)
    mock_update_name_func.side_effect = PersistenceOpsBaseError()
    with pytest.raises(UpdateNameError):
        await app_ops_tag.update_name(
            uuid.uuid4(), request, update_name_func=mock_update_name_func
        )
    mock_update_name_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_name_no_rows_affected():
    request = schema_tag.SchemaUpdateName(name="NewTagName")
    mock_update_name_func = AsyncMock(return_value=0)
    with pytest.raises(UpdateNameError, match="No rows were affected."):
        await app_ops_tag.update_name(
            uuid.uuid4(), request, update_name_func=mock_update_name_func
        )
    mock_update_name_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_name_multiple_rows_affected():
    request = schema_tag.SchemaUpdateName(name="NewTagName")
    mock_update_name_func = AsyncMock(return_value=2)
    with pytest.raises(UpdateNameError, match="More than 1 row was affected."):
        await app_ops_tag.update_name(
            uuid.uuid4(), request, update_name_func=mock_update_name_func
        )
    mock_update_name_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_tag_list():

    returned_tag1 = schema_tag.SchemaTagDisplay(
        id=uuid.uuid4(),
        name="tag1",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )

    returned_tag2 = schema_tag.SchemaTagDisplay(
        id=uuid.uuid4(),
        name="tag2",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )

    mock_select_tag_list_func = AsyncMock()
    mock_select_tag_list_func.return_value = [
        returned_tag1,
        returned_tag2,
    ]

    results = await app_ops_tag.get_tag_list(
        0,
        10,
        "created_on DESC, name",
        select_tag_list_func=mock_select_tag_list_func,
    )
    mock_select_tag_list_func.assert_awaited_once()
    assert len(results) == 2
    assert all(isinstance(item, schema_tag.SchemaTagDisplay) for item in results)


@pytest.mark.asyncio
async def test_get_tag_list_invalid_page_index():

    mock_select_tag_list_func = AsyncMock()
    with pytest.raises(GetTagListError):
        await app_ops_tag.get_tag_list(
            -1,
            10,
            "created_on DESC, name",
            select_tag_list_func=mock_select_tag_list_func,
        )
    mock_select_tag_list_func.assert_not_called()


@pytest.mark.asyncio
async def test_get_tag_list_invalid_page_size():

    mock_select_tag_list_func = AsyncMock()
    with pytest.raises(GetTagListError):
        await app_ops_tag.get_tag_list(
            0,
            0,
            "created_on DESC, name",
            select_tag_list_func=mock_select_tag_list_func,
        )
    mock_select_tag_list_func.assert_not_called()


@pytest.mark.asyncio
async def test_get_tag_list_persistence_error():

    mock_select_tag_list_func = AsyncMock()
    mock_select_tag_list_func.side_effect = PersistenceOpsBaseError()
    with pytest.raises(GetTagListError):
        await app_ops_tag.get_tag_list(
            0,
            10,
            "created_on DESC, name",
            select_tag_list_func=mock_select_tag_list_func,
        )
    mock_select_tag_list_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_tag_by_id():

    returned_tag1 = schema_tag.SchemaTagDisplay(
        id=uuid.uuid4(),
        name="testtag1",
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )

    mock_select_tag_by_id_func = AsyncMock()
    mock_select_tag_by_id_func.return_value = returned_tag1
    tag = await app_ops_tag.get_tag_by_id(
        uuid.uuid4(), select_tag_by_id_func=mock_select_tag_by_id_func
    )
    mock_select_tag_by_id_func.assert_awaited_once()
    assert isinstance(tag, schema_tag.SchemaTagDisplay)
    assert tag.id == returned_tag1.id


@pytest.mark.asyncio
async def test_get_tag_by_id_not_found():

    mock_select_tag_by_id_func = AsyncMock()
    mock_select_tag_by_id_func.return_value = None
    tag = await app_ops_tag.get_tag_by_id(
        uuid.uuid4(), select_tag_by_id_func=mock_select_tag_by_id_func
    )
    mock_select_tag_by_id_func.assert_awaited_once()
    assert tag is None


@pytest.mark.asyncio
async def test_get_tag_by_id_persistence_error():

    mock_select_tag_by_id_func = AsyncMock()
    mock_select_tag_by_id_func.side_effect = PersistenceOpsBaseError()
    with pytest.raises(GetTagByIdError):
        await app_ops_tag.get_tag_by_id(
            uuid.uuid4(), select_tag_by_id_func=mock_select_tag_by_id_func
        )
    mock_select_tag_by_id_func.assert_awaited_once()
