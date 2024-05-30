import uuid

import pytest

from src.persistence.database.models.db_dining_table import DbDiningTable
from src.persistence.database.ops.db_ops_dining_table import (
    delete_dining_table,
    insert_dining_table,
    select_dining_table_list,
    update_name,
    update_position,
    update_size,
)
from src.schemas.schema_dining_table import (
    SchemaDiningTableCreate,
    SchemaUpdateName,
    SchemaUpdatePosition,
    SchemaUpdateSize,
)
from tests.persistence.database.ops.mock_utils import (
    async_testing_session_scope,
    reset_test_database,
    setup_test_database,
)


@pytest.mark.asyncio
async def test_insert_dining_table():

    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_dining_table(
                async_session,
                SchemaDiningTableCreate(
                    name="NewTable", x=5, y=10, width=50, height=100
                ),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            assert isinstance(new_record, DbDiningTable)
            assert new_record.id is not None
            results = await select_dining_table_list(async_session, 0, 10, "created_on")
            assert len(results) == 1
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_insert_dining_table_multiple_records():

    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record_1 = await insert_dining_table(
                async_session,
                SchemaDiningTableCreate(
                    name="NewTable1", x=5, y=10, width=50, height=100
                ),
            )
            new_record_2 = await insert_dining_table(
                async_session,
                SchemaDiningTableCreate(
                    name="NewTable2", x=6, y=11, width=51, height=101
                ),
            )
            await async_session.commit()
            await async_session.refresh(new_record_1)
            await async_session.refresh(new_record_2)
            assert isinstance(new_record_1, DbDiningTable)
            assert new_record_1.id is not None
            assert new_record_1.x == 5
            assert new_record_1.y == 10
            assert new_record_1.width == 50
            assert new_record_1.height == 100
            assert isinstance(new_record_2, DbDiningTable)
            assert new_record_2.id is not None
            assert new_record_2.x == 6
            assert new_record_2.y == 11
            assert new_record_2.width == 51
            assert new_record_2.height == 101
            results = await select_dining_table_list(async_session, 0, 10, "created_on")
            assert len(results) == 2
            assert all(isinstance(result, DbDiningTable) for result in results)
            assert any(result.name == "NewTable1" for result in results)
            assert any(result.name == "NewTable2" for result in results)
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_delete_dining_table():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_dining_table(
                async_session,
                SchemaDiningTableCreate(
                    name="NewTable", x=5, y=10, width=50, height=100
                ),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_dining_table_list(async_session, 0, 10, "created_on")
            assert len(results) == 1
            rowcount = await delete_dining_table(async_session, results[0].id)
            await async_session.commit()
            assert rowcount == 1
            results = await select_dining_table_list(async_session, 0, 10, "created_on")
            assert len(results) == 0
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_delete_dining_table_not_found():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_dining_table(
                async_session,
                SchemaDiningTableCreate(
                    name="NewTable", x=5, y=10, width=50, height=100
                ),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_dining_table_list(async_session, 0, 10, "created_on")
            assert len(results) == 1
            rowcount = await delete_dining_table(async_session, uuid.uuid4())
            await async_session.commit()
            assert rowcount == 0
            results = await select_dining_table_list(async_session, 0, 10, "created_on")
            assert len(results) == 1
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_update_position():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_dining_table(
                async_session,
                SchemaDiningTableCreate(
                    name="NewTable", x=5, y=10, width=50, height=100
                ),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_dining_table_list(async_session, 0, 10, "created_on")
            assert results[0].x == 5
            assert results[0].y == 10
            rowcount = await update_position(
                async_session, results[0].id, SchemaUpdatePosition(x=15, y=20)
            )
            await async_session.commit()
            assert rowcount == 1
            results = await select_dining_table_list(async_session, 0, 10, "created_on")
            assert results[0].x == 15
            assert results[0].y == 20
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_update_position_not_found():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_dining_table(
                async_session,
                SchemaDiningTableCreate(
                    name="NewTable", x=5, y=10, width=50, height=100
                ),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_dining_table_list(async_session, 0, 10, "created_on")
            assert results[0].x == 5
            assert results[0].y == 10
            rowcount = await update_position(
                async_session, uuid.uuid4(), SchemaUpdatePosition(x=15, y=20)
            )
            await async_session.commit()
            assert rowcount == 0
            results = await select_dining_table_list(async_session, 0, 10, "created_on")
            assert results[0].x == 5
            assert results[0].y == 10
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_update_size():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_dining_table(
                async_session,
                SchemaDiningTableCreate(
                    name="NewTable", x=5, y=10, width=50, height=100
                ),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_dining_table_list(async_session, 0, 10, "created_on")
            assert results[0].width == 50
            assert results[0].height == 100
            rowcount = await update_size(
                async_session,
                results[0].id,
                SchemaUpdateSize(width=150, height=200),
            )
            await async_session.commit()
            assert rowcount == 1
            results = await select_dining_table_list(async_session, 0, 10, "created_on")
            assert results[0].width == 150
            assert results[0].height == 200
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_update_size_not_found():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_dining_table(
                async_session,
                SchemaDiningTableCreate(
                    name="NewTable", x=5, y=10, width=50, height=100
                ),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_dining_table_list(async_session, 0, 10, "created_on")
            assert results[0].width == 50
            assert results[0].height == 100
            rowcount = await update_size(
                async_session, uuid.uuid4(), SchemaUpdateSize(width=150, height=200)
            )
            await async_session.commit()
            assert rowcount == 0
            results = await select_dining_table_list(async_session, 0, 10, "created_on")
            assert results[0].width == 50
            assert results[0].height == 100
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_update_name():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_dining_table(
                async_session,
                SchemaDiningTableCreate(
                    name="NewTable", x=5, y=10, width=50, height=100
                ),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_dining_table_list(async_session, 0, 10, "created_on")
            assert results[0].name == "NewTable"
            rowcount = await update_name(
                async_session,
                results[0].id,
                SchemaUpdateName(name="NewTableNewName"),
            )
            await async_session.commit()
            assert rowcount == 1
            results = await select_dining_table_list(async_session, 0, 10, "created_on")
            assert results[0].name == "NewTableNewName"
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_update_name_not_found():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_dining_table(
                async_session,
                SchemaDiningTableCreate(
                    name="NewTable", x=5, y=10, width=50, height=100
                ),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_dining_table_list(async_session, 0, 10, "created_on")
            assert results[0].name == "NewTable"
            rowcount = await update_name(
                async_session, uuid.uuid4(), SchemaUpdateName(name="NewTableNewName")
            )
            await async_session.commit()
            assert rowcount == 0
            results = await select_dining_table_list(async_session, 0, 10, "created_on")
            assert results[0].name == "NewTable"
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_select_dining_table_list():

    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record_1 = await insert_dining_table(
                async_session,
                SchemaDiningTableCreate(
                    name="NewTable1", x=5, y=10, width=50, height=100
                ),
            )
            new_record_2 = await insert_dining_table(
                async_session,
                SchemaDiningTableCreate(
                    name="NewTable2", x=6, y=11, width=55, height=101
                ),
            )
            new_record_3 = await insert_dining_table(
                async_session,
                SchemaDiningTableCreate(
                    name="NewTable3", x=7, y=12, width=50, height=102
                ),
            )
            new_record_4 = await insert_dining_table(
                async_session,
                SchemaDiningTableCreate(
                    name="NewTable4", x=8, y=13, width=60, height=103
                ),
            )
            await async_session.commit()
            await async_session.refresh(new_record_1)
            await async_session.refresh(new_record_2)
            await async_session.refresh(new_record_3)
            await async_session.refresh(new_record_4)
            results = await select_dining_table_list(async_session, 0, 10, "name desc")
            assert results[0] == new_record_4
            assert results[1] == new_record_3
            assert results[2] == new_record_2
            assert results[3] == new_record_1
            results = await select_dining_table_list(
                async_session, 0, 10, "width, name desc"
            )
            assert results[0] == new_record_3
            assert results[1] == new_record_1
            assert results[2] == new_record_2
            assert results[3] == new_record_4
            results = await select_dining_table_list(
                async_session, 0, 10, "width desc, name"
            )
            assert results[0] == new_record_4
            assert results[1] == new_record_2
            assert results[2] == new_record_1
            assert results[3] == new_record_3
            results = await select_dining_table_list(
                async_session, 0, 2, "width desc, name"
            )
            assert len(results) == 2
            assert results[0] == new_record_4
            assert results[1] == new_record_2
            results = await select_dining_table_list(
                async_session, 1, 2, "width desc, name"
            )
            assert len(results) == 2
            assert results[0] == new_record_1
            assert results[1] == new_record_3

        finally:
            await reset_test_database()
