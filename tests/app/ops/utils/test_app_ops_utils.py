from unittest.mock import AsyncMock

import pytest

from src.app.ops.exceptions.app_ops_exceptions import OpsBaseError
from src.app.ops.utils import app_ops_utils


@pytest.mark.asyncio
async def test_affect_existing_row():
    mock_affect_existing_row_func = AsyncMock(return_value=1)
    await app_ops_utils.affect_existing_row(
        mock_affect_existing_row_func,
        OpsBaseError,
        my_arg1="Hello",
        my_arg2="There",
    )
    mock_affect_existing_row_func.assert_called_with(my_arg1="Hello", my_arg2="There")


@pytest.mark.asyncio
async def test_affect_existing_row_no_rows_affected():
    mock_affect_existing_row_func = AsyncMock(return_value=0)
    with pytest.raises(OpsBaseError):
        await app_ops_utils.affect_existing_row(
            mock_affect_existing_row_func,
            OpsBaseError,
            my_arg1="Hello",
            my_arg2="There",
        )
    mock_affect_existing_row_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_affect_existing_row_multiple_rows_affected():
    mock_affect_existing_row_func = AsyncMock(return_value=2)
    with pytest.raises(OpsBaseError):
        await app_ops_utils.affect_existing_row(
            mock_affect_existing_row_func,
            OpsBaseError,
            my_arg1="Hello",
            my_arg2="There",
        )
    mock_affect_existing_row_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_affect_existing_row_persistence_error():
    mock_affect_existing_row_func = AsyncMock(return_value=1)
    mock_affect_existing_row_func.side_effect = OpsBaseError()
    with pytest.raises(OpsBaseError):
        await app_ops_utils.affect_existing_row(
            mock_affect_existing_row_func,
            OpsBaseError,
            my_arg1="Hello",
            my_arg2="There",
        )
    mock_affect_existing_row_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_data_list():
    mock_select_data_list_func = AsyncMock(return_value=[1, 2, 3, 4, 5])

    results = await app_ops_utils.get_data_list(
        0,
        10,
        "created_on",
        mock_select_data_list_func,
        OpsBaseError,
        my_arg1="Hello",
        my_arg2="There",
    )

    mock_select_data_list_func.assert_called_with(
        page_index=0,
        page_size=10,
        sort_by="created_on",
        my_arg1="Hello",
        my_arg2="There",
    )
    assert results == [1, 2, 3, 4, 5]

    mock_select_data_list_func = AsyncMock(return_value=[])

    results = await app_ops_utils.get_data_list(
        0, 10, "", mock_select_data_list_func, OpsBaseError
    )

    mock_select_data_list_func.assert_called_with(
        page_index=0, page_size=10, sort_by=""
    )
    assert results == []


@pytest.mark.asyncio
async def test_get_data_list_invalid_page_index():
    mock_select_data_list_func = AsyncMock()
    with pytest.raises(OpsBaseError, match="Invalid page index."):
        await app_ops_utils.get_data_list(
            -1, 1, "created_on", mock_select_data_list_func, OpsBaseError
        )
    mock_select_data_list_func.assert_not_called()


@pytest.mark.asyncio
async def test_get_data_list_invalid_page_size():
    mock_select_data_list_func = AsyncMock()
    with pytest.raises(OpsBaseError, match="Invalid page size."):
        await app_ops_utils.get_data_list(
            1, 0, "created_on", mock_select_data_list_func, OpsBaseError
        )
    mock_select_data_list_func.assert_not_called()


@pytest.mark.asyncio
async def test_get_data_list_persistence_error():
    mock_select_data_list_func = AsyncMock()
    mock_select_data_list_func.side_effect = OpsBaseError
    with pytest.raises(OpsBaseError):
        await app_ops_utils.get_data_list(
            0,
            10,
            "created_on",
            mock_select_data_list_func,
            OpsBaseError,
            my_arg1="Hello",
            my_arg2="There",
        )

    mock_select_data_list_func.assert_called_with(
        page_index=0,
        page_size=10,
        sort_by="created_on",
        my_arg1="Hello",
        my_arg2="There",
    )
