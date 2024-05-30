import uuid

import pytest

from src.persistence.database.models.db_menu import DbMenu
from src.persistence.database.ops.db_ops_menu import (
    delete_menu,
    insert_menu,
    select_menu_by_id,
    select_menu_list,
    update_name,
)
from src.schemas.schema_menu import SchemaMenuCreate, SchemaUpdateName
from tests.persistence.database.ops.mock_utils import (
    async_testing_session_scope,
    reset_test_database,
    setup_test_database,
)


@pytest.mark.asyncio
async def test_insert_menu():

    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_menu(
                async_session,
                SchemaMenuCreate(name="NewMenu"),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            assert isinstance(new_record, DbMenu)
            assert new_record.id is not None
            results = await select_menu_list(async_session, 0, 10, "created_on")
            assert len(results) == 1
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_insert_menu_multiple_records():

    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record_1 = await insert_menu(
                async_session,
                SchemaMenuCreate(name="NewMenu1"),
            )
            new_record_2 = await insert_menu(
                async_session,
                SchemaMenuCreate(name="NewMenu2"),
            )
            await async_session.commit()
            await async_session.refresh(new_record_1)
            await async_session.refresh(new_record_2)
            assert isinstance(new_record_1, DbMenu)
            assert new_record_1.id is not None
            assert new_record_1.name == "NewMenu1"
            assert isinstance(new_record_2, DbMenu)
            assert new_record_2.id is not None
            assert new_record_2.name == "NewMenu2"
            results = await select_menu_list(async_session, 0, 10, "created_on")
            assert len(results) == 2
            assert all(isinstance(result, DbMenu) for result in results)
            assert any(result.name == "NewMenu1" for result in results)
            assert any(result.name == "NewMenu2" for result in results)
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_delete_menu():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_menu(
                async_session,
                SchemaMenuCreate(name="NewMenu"),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_menu_list(async_session, 0, 10, "created_on")
            assert len(results) == 1
            rowcount = await delete_menu(async_session, results[0].id)
            await async_session.commit()
            assert rowcount == 1
            results = await select_menu_list(async_session, 0, 10, "created_on")
            assert len(results) == 0
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_delete_menu_not_found():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_menu(
                async_session,
                SchemaMenuCreate(name="NewMenu"),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_menu_list(async_session, 0, 10, "created_on")
            assert len(results) == 1
            rowcount = await delete_menu(async_session, uuid.uuid4())
            await async_session.commit()
            assert rowcount == 0
            results = await select_menu_list(async_session, 0, 10, "created_on")
            assert len(results) == 1
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_update_name():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_menu(
                async_session,
                SchemaMenuCreate(name="NewMenu"),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_menu_list(async_session, 0, 10, "created_on")
            assert results[0].name == "NewMenu"
            rowcount = await update_name(
                async_session,
                results[0].id,
                SchemaUpdateName(name="NewMenuNewName"),
            )
            await async_session.commit()
            assert rowcount == 1
            results = await select_menu_list(async_session, 0, 10, "created_on")
            assert results[0].name == "NewMenuNewName"
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_update_name_not_found():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_menu(
                async_session,
                SchemaMenuCreate(name="NewMenu"),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_menu_list(async_session, 0, 10, "created_on")
            assert results[0].name == "NewMenu"
            rowcount = await update_name(
                async_session, uuid.uuid4(), SchemaUpdateName(name="NewMenuNewName")
            )
            await async_session.commit()
            assert rowcount == 0
            results = await select_menu_list(async_session, 0, 10, "created_on")
            assert results[0].name == "NewMenu"
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_select_menu_list():

    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record_1 = await insert_menu(
                async_session, SchemaMenuCreate(name="NewMenu1")
            )
            new_record_2 = await insert_menu(
                async_session, SchemaMenuCreate(name="NewMenu2")
            )
            new_record_3 = await insert_menu(
                async_session, SchemaMenuCreate(name="NewMenu3")
            )
            new_record_4 = await insert_menu(
                async_session, SchemaMenuCreate(name="NewMenu4")
            )
            await async_session.commit()
            await async_session.refresh(new_record_1)
            await async_session.refresh(new_record_2)
            await async_session.refresh(new_record_3)
            await async_session.refresh(new_record_4)
            results = await select_menu_list(async_session, 0, 10, "name")
            assert results[0] == new_record_1
            assert results[1] == new_record_2
            assert results[2] == new_record_3
            assert results[3] == new_record_4
            results = await select_menu_list(async_session, 0, 10, "name desc")
            assert results[0] == new_record_4
            assert results[1] == new_record_3
            assert results[2] == new_record_2
            assert results[3] == new_record_1

        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_select_menu_by_id():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record_1 = await insert_menu(
                async_session,
                SchemaMenuCreate(name="NewMenu1"),
            )
            new_record_2 = await insert_menu(
                async_session,
                SchemaMenuCreate(name="NewMenu2"),
            )
            new_record_3 = await insert_menu(
                async_session,
                SchemaMenuCreate(name="NewMenu3"),
            )
            new_record_4 = await insert_menu(
                async_session,
                SchemaMenuCreate(name="NewMenu4"),
            )
            await async_session.commit()
            await async_session.refresh(new_record_1)
            await async_session.refresh(new_record_2)
            await async_session.refresh(new_record_3)
            await async_session.refresh(new_record_4)
            menu = await select_menu_by_id(async_session, new_record_1.id)
            assert menu == new_record_1
            menu = await select_menu_by_id(async_session, new_record_2.id)
            assert menu == new_record_2
            menu = await select_menu_by_id(async_session, new_record_3.id)
            assert menu == new_record_3
            menu = await select_menu_by_id(async_session, new_record_4.id)
            assert menu == new_record_4

        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_select_menu_by_id_not_found():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record_1 = await insert_menu(
                async_session, SchemaMenuCreate(name="NewMenu1")
            )
            await async_session.commit()
            await async_session.refresh(new_record_1)
            menu = await select_menu_by_id(async_session, uuid.uuid4())
            assert menu is None
        finally:
            await reset_test_database()
