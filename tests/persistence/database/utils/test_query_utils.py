import pytest
from sqlalchemy import Column, Integer, String, select

from src.persistence.database.session import Base
from src.persistence.database.utils import query_utils


# Mock entity type
class MockEntity(Base):
    __tablename__ = "mock_entities"
    id = Column(Integer, primary_key=True)
    created_on = Column(String)
    username = Column(String)


def evaluate_order_by_clause(sort_by: str, expected_order_by_clause: str):
    page_index = 1
    page_size = 10
    # sort_by = "username"

    query = select(MockEntity)
    final_query = query_utils.apply_sorting_and_paging_to_list_query(
        query, MockEntity, page_index, page_size, sort_by
    )
    if sort_by:
        assert len(query._order_by_clauses) == 0
        # assert len(final_query._order_by_clauses) == 1
        assert expected_order_by_clause in str(final_query)
        # Make sure no ASC is attached unexpectedly to the final query
        assert f"{expected_order_by_clause} ASC" not in str(final_query)
        if not expected_order_by_clause.endswith("DESC"):
            assert f"{expected_order_by_clause} DESC" not in str(final_query)
    else:
        assert "ORDER BY" not in str(final_query)


@pytest.mark.asyncio
async def test_apply_sorting_and_paging_to_list_query_1_col():
    evaluate_order_by_clause("username", "ORDER BY mock_entities.username")
    evaluate_order_by_clause("username ASC", "ORDER BY mock_entities.username")
    evaluate_order_by_clause("username DESC", "ORDER BY mock_entities.username DESC")


@pytest.mark.asyncio
async def test_apply_sorting_and_paging_to_list_query_2_col():
    evaluate_order_by_clause(
        "username, created_on",
        "ORDER BY mock_entities.username, mock_entities.created_on",
    )

    evaluate_order_by_clause(
        "username, created_on ASC",
        "ORDER BY mock_entities.username, mock_entities.created_on",
    )

    evaluate_order_by_clause(
        "username, created_on DESC",
        "ORDER BY mock_entities.username, mock_entities.created_on DESC",
    )

    evaluate_order_by_clause(
        "username ASC, created_on",
        "ORDER BY mock_entities.username, mock_entities.created_on",
    )

    evaluate_order_by_clause(
        "username ASC, created_on ASC",
        "ORDER BY mock_entities.username, mock_entities.created_on",
    )

    evaluate_order_by_clause(
        "username ASC, created_on DESC",
        "ORDER BY mock_entities.username, mock_entities.created_on DESC",
    )

    evaluate_order_by_clause(
        "username DESC, created_on",
        "ORDER BY mock_entities.username DESC, mock_entities.created_on",
    )

    evaluate_order_by_clause(
        "username DESC, created_on ASC",
        "ORDER BY mock_entities.username DESC, mock_entities.created_on",
    )

    evaluate_order_by_clause(
        "username DESC, created_on DESC",
        "ORDER BY mock_entities.username DESC, mock_entities.created_on DESC",
    )


@pytest.mark.asyncio
async def test_apply_sorting_and_paging_to_list_query_3_col():
    evaluate_order_by_clause(
        "username, created_on, id",
        "ORDER BY mock_entities.username, mock_entities.created_on, mock_entities.id",
    )

    evaluate_order_by_clause(
        "username, created_on, id ASC",
        "ORDER BY mock_entities.username, mock_entities.created_on, mock_entities.id",
    )

    evaluate_order_by_clause(
        "username, created_on, id DESC",
        "ORDER BY mock_entities.username, mock_entities.created_on, mock_entities.id DESC",
    )

    evaluate_order_by_clause(
        "username, created_on ASC, id",
        "ORDER BY mock_entities.username, mock_entities.created_on, mock_entities.id",
    )

    evaluate_order_by_clause(
        "username, created_on ASC, id ASC",
        "ORDER BY mock_entities.username, mock_entities.created_on, mock_entities.id",
    )

    evaluate_order_by_clause(
        "username, created_on ASC, id DESC",
        "ORDER BY mock_entities.username, mock_entities.created_on, mock_entities.id DESC",
    )

    evaluate_order_by_clause(
        "username, created_on DESC, id",
        "ORDER BY mock_entities.username, mock_entities.created_on DESC, mock_entities.id",
    )

    evaluate_order_by_clause(
        "username, created_on DESC, id ASC",
        "ORDER BY mock_entities.username, mock_entities.created_on DESC, mock_entities.id",
    )

    evaluate_order_by_clause(
        "username, created_on DESC, id DESC",
        "ORDER BY mock_entities.username, mock_entities.created_on DESC, mock_entities.id DESC",
    )

    evaluate_order_by_clause(
        "username ASC, created_on DESC, id",
        "ORDER BY mock_entities.username, mock_entities.created_on DESC, mock_entities.id",
    )

    evaluate_order_by_clause(
        "username ASC, created_on DESC, id ASC",
        "ORDER BY mock_entities.username, mock_entities.created_on DESC, mock_entities.id",
    )

    evaluate_order_by_clause(
        "username ASC, created_on DESC, id DESC",
        "ORDER BY mock_entities.username, mock_entities.created_on DESC, mock_entities.id DESC",
    )

    evaluate_order_by_clause(
        "username DESC, created_on DESC, id",
        "ORDER BY mock_entities.username DESC, mock_entities.created_on DESC, mock_entities.id",
    )

    evaluate_order_by_clause(
        "username DESC, created_on DESC, id ASC",
        "ORDER BY mock_entities.username DESC, mock_entities.created_on DESC, mock_entities.id",
    )

    evaluate_order_by_clause(
        "username DESC, created_on DESC, id DESC",
        "ORDER BY mock_entities.username DESC, mock_entities.created_on DESC, mock_entities.id DESC",
    )


@pytest.mark.asyncio
async def test_apply_sorting_and_paging_to_list_query_none():
    evaluate_order_by_clause(None, None)
    evaluate_order_by_clause("", None)
