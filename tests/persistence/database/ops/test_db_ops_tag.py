import uuid

import pytest

from src.persistence.database.models.db_tag import DbTag
from src.persistence.database.ops.db_ops_tag import (
    delete_tag,
    insert_tag,
    select_tag_by_id,
    select_tag_list,
    update_name,
)
from src.schemas.schema_tag import SchemaTagCreate, SchemaUpdateName
from tests.persistence.database.ops.mock_utils import (
    async_testing_session_scope,
    reset_test_database,
    setup_test_database,
)


@pytest.mark.asyncio
async def test_insert_tag():

    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_tag(
                async_session,
                SchemaTagCreate(name="NewTag"),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            assert isinstance(new_record, DbTag)
            assert new_record.id is not None
            results = await select_tag_list(async_session, 0, 10, "created_on")
            assert len(results) == 1
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_insert_tag_multiple_records():

    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record_1 = await insert_tag(
                async_session,
                SchemaTagCreate(name="NewTag1"),
            )
            new_record_2 = await insert_tag(
                async_session,
                SchemaTagCreate(name="NewTag2"),
            )
            await async_session.commit()
            await async_session.refresh(new_record_1)
            await async_session.refresh(new_record_2)
            assert isinstance(new_record_1, DbTag)
            assert new_record_1.id is not None
            assert new_record_1.name == "NewTag1"
            assert isinstance(new_record_2, DbTag)
            assert new_record_2.id is not None
            assert new_record_2.name == "NewTag2"
            results = await select_tag_list(async_session, 0, 10, "created_on")
            assert len(results) == 2
            assert all(isinstance(result, DbTag) for result in results)
            assert any(result.name == "NewTag1" for result in results)
            assert any(result.name == "NewTag2" for result in results)
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_delete_tag():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_tag(
                async_session,
                SchemaTagCreate(name="NewTag"),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_tag_list(async_session, 0, 10, "created_on")
            assert len(results) == 1
            rowcount = await delete_tag(async_session, results[0].id)
            await async_session.commit()
            assert rowcount == 1
            results = await select_tag_list(async_session, 0, 10, "created_on")
            assert len(results) == 0
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_delete_tag_not_found():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_tag(
                async_session,
                SchemaTagCreate(name="NewTag"),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_tag_list(async_session, 0, 10, "created_on")
            assert len(results) == 1
            rowcount = await delete_tag(async_session, uuid.uuid4())
            await async_session.commit()
            assert rowcount == 0
            results = await select_tag_list(async_session, 0, 10, "created_on")
            assert len(results) == 1
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_update_name():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_tag(
                async_session,
                SchemaTagCreate(name="NewTag"),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_tag_list(async_session, 0, 10, "created_on")
            assert results[0].name == "NewTag"
            rowcount = await update_name(
                async_session,
                results[0].id,
                SchemaUpdateName(name="NewTagNewName"),
            )
            await async_session.commit()
            assert rowcount == 1
            results = await select_tag_list(async_session, 0, 10, "created_on")
            assert results[0].name == "NewTagNewName"
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_update_name_not_found():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_tag(
                async_session,
                SchemaTagCreate(name="NewTag"),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_tag_list(async_session, 0, 10, "created_on")
            assert results[0].name == "NewTag"
            rowcount = await update_name(
                async_session, uuid.uuid4(), SchemaUpdateName(name="NewTagNewName")
            )
            await async_session.commit()
            assert rowcount == 0
            results = await select_tag_list(async_session, 0, 10, "created_on")
            assert results[0].name == "NewTag"
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_select_tag_list():

    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record_1 = await insert_tag(
                async_session, SchemaTagCreate(name="NewTag1")
            )
            new_record_2 = await insert_tag(
                async_session, SchemaTagCreate(name="NewTag2")
            )
            new_record_3 = await insert_tag(
                async_session, SchemaTagCreate(name="NewTag3")
            )
            new_record_4 = await insert_tag(
                async_session, SchemaTagCreate(name="NewTag4")
            )
            await async_session.commit()
            await async_session.refresh(new_record_1)
            await async_session.refresh(new_record_2)
            await async_session.refresh(new_record_3)
            await async_session.refresh(new_record_4)
            results = await select_tag_list(async_session, 0, 10, "name")
            assert results[0] == new_record_1
            assert results[1] == new_record_2
            assert results[2] == new_record_3
            assert results[3] == new_record_4
            results = await select_tag_list(async_session, 0, 10, "name desc")
            assert results[0] == new_record_4
            assert results[1] == new_record_3
            assert results[2] == new_record_2
            assert results[3] == new_record_1

        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_select_tag_by_id():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record_1 = await insert_tag(
                async_session,
                SchemaTagCreate(name="NewTag1"),
            )
            new_record_2 = await insert_tag(
                async_session,
                SchemaTagCreate(name="NewTag2"),
            )
            new_record_3 = await insert_tag(
                async_session,
                SchemaTagCreate(name="NewTag3"),
            )
            new_record_4 = await insert_tag(
                async_session,
                SchemaTagCreate(name="NewTag4"),
            )
            await async_session.commit()
            await async_session.refresh(new_record_1)
            await async_session.refresh(new_record_2)
            await async_session.refresh(new_record_3)
            await async_session.refresh(new_record_4)
            tag = await select_tag_by_id(async_session, new_record_1.id)
            assert tag == new_record_1
            tag = await select_tag_by_id(async_session, new_record_2.id)
            assert tag == new_record_2
            tag = await select_tag_by_id(async_session, new_record_3.id)
            assert tag == new_record_3
            tag = await select_tag_by_id(async_session, new_record_4.id)
            assert tag == new_record_4

        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_select_tag_by_id_not_found():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record_1 = await insert_tag(
                async_session, SchemaTagCreate(name="NewTag1")
            )
            await async_session.commit()
            await async_session.refresh(new_record_1)
            tag = await select_tag_by_id(async_session, uuid.uuid4())
            assert tag is None
        finally:
            await reset_test_database()
