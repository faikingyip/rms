import uuid

import pytest

from src.persistence.database.models.db_user import DbUser
from src.persistence.database.ops.db_ops_user import (
    delete_user,
    insert_user,
    select_user_by_id,
    select_user_by_username,
    select_user_list,
    update_password,
)
from src.schemas.schema_user import SchemaChangePassword, SchemaUserCreate
from src.utils import bcrypt_hash
from tests.persistence.database.ops.mock_utils import (
    async_testing_session_scope,
    reset_test_database,
    setup_test_database,
)


@pytest.mark.asyncio
async def test_insert_user():

    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser", password="thepassword"),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            assert isinstance(new_record, DbUser)
            assert new_record.id is not None
            results = await select_user_list(async_session, 0, 10, "created_on")
            assert len(results) == 1
            results[0] = new_record
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_insert_user_multiple_records():

    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record_1 = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser1", password="thepassword"),
            )
            new_record_2 = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser2", password="thepassword"),
            )
            await async_session.commit()
            await async_session.refresh(new_record_1)
            await async_session.refresh(new_record_2)
            assert isinstance(new_record_1, DbUser)
            assert new_record_1.id is not None
            assert new_record_1.username == "NewUser1"
            assert isinstance(new_record_2, DbUser)
            assert new_record_2.id is not None
            assert new_record_2.username == "NewUser2"
            results = await select_user_list(async_session, 0, 10, "created_on")
            assert len(results) == 2
            assert all(isinstance(result, DbUser) for result in results)
            assert any(result.username == "NewUser1" for result in results)
            assert any(result.username == "NewUser2" for result in results)
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_delete_user():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser1", password="thepassword"),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_user_list(async_session, 0, 10, "created_on")
            assert len(results) == 1
            rowcount = await delete_user(async_session, results[0].id)
            await async_session.commit()
            assert rowcount == 1
            results = await select_user_list(async_session, 0, 10, "created_on")
            assert len(results) == 0
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_delete_user_not_found():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser1", password="thepassword"),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_user_list(async_session, 0, 10, "created_on")
            assert len(results) == 1
            rowcount = await delete_user(async_session, uuid.uuid4())
            await async_session.commit()
            assert rowcount == 0
            results = await select_user_list(async_session, 0, 10, "created_on")
            assert len(results) == 1
        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_update_password():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser1", password="thepassword"),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_user_list(async_session, 0, 10, "created_on")
            password_hash_b4_update = results[0].password_hash
            assert password_hash_b4_update is not None
            rowcount = await update_password(
                async_session,
                results[0].id,
                SchemaChangePassword(new_password="newpassword"),
            )
            await async_session.commit()
            assert rowcount == 1
            results = await select_user_list(async_session, 0, 10, "created_on")
            assert results[0].password_hash is not None
            assert results[0].password_hash != password_hash_b4_update
            assert bcrypt_hash.verify_bcrypt("thepassword", password_hash_b4_update)
            assert bcrypt_hash.verify_bcrypt("newpassword", results[0].password_hash)

        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_update_password_not_found():
    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser1", password="thepassword"),
            )
            await async_session.commit()
            await async_session.refresh(new_record)
            results = await select_user_list(async_session, 0, 10, "created_on")
            password_hash_b4_update = results[0].password_hash
            assert password_hash_b4_update is not None
            rowcount = await update_password(
                async_session,
                uuid.uuid4(),
                SchemaChangePassword(new_password="newpassword"),
            )
            await async_session.commit()
            assert rowcount == 0
            results = await select_user_list(async_session, 0, 10, "created_on")
            assert results[0].password_hash == password_hash_b4_update
            assert bcrypt_hash.verify_bcrypt("thepassword", results[0].password_hash)

        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_select_user_list():

    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record_1 = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser1", password="mypassword"),
            )
            new_record_2 = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser2", password="mypassword"),
            )
            new_record_3 = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser3", password="mypassword"),
            )
            new_record_4 = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser4", password="mypassword"),
            )
            await async_session.commit()
            await async_session.refresh(new_record_1)
            await async_session.refresh(new_record_2)
            await async_session.refresh(new_record_3)
            await async_session.refresh(new_record_4)
            results = await select_user_list(async_session, 0, 10, "username")
            assert results[0] == new_record_1
            assert results[1] == new_record_2
            assert results[2] == new_record_3
            assert results[3] == new_record_4
            results = await select_user_list(async_session, 0, 10, "username DESC")
            assert results[0] == new_record_4
            assert results[1] == new_record_3
            assert results[2] == new_record_2
            assert results[3] == new_record_1
            results = await select_user_list(async_session, 0, 2, "username DESC")
            assert len(results) == 2
            assert results[0] == new_record_4
            assert results[1] == new_record_3
            results = await select_user_list(async_session, 1, 2, "username DESC")
            assert len(results) == 2
            assert results[0] == new_record_2
            assert results[1] == new_record_1

        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_select_user_by_id():

    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record_1 = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser1", password="mypassword"),
            )
            new_record_2 = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser2", password="mypassword"),
            )
            new_record_3 = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser3", password="mypassword"),
            )
            new_record_4 = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser4", password="mypassword"),
            )
            await async_session.commit()
            await async_session.refresh(new_record_1)
            await async_session.refresh(new_record_2)
            await async_session.refresh(new_record_3)
            await async_session.refresh(new_record_4)
            user = await select_user_by_id(async_session, new_record_1.id)
            assert user == new_record_1
            user = await select_user_by_id(async_session, new_record_2.id)
            assert user == new_record_2
            user = await select_user_by_id(async_session, new_record_3.id)
            assert user == new_record_3
            user = await select_user_by_id(async_session, new_record_4.id)
            assert user == new_record_4

        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_select_user_by_id_not_found():

    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record_1 = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser1", password="mypassword"),
            )
            await async_session.commit()
            await async_session.refresh(new_record_1)
            user = await select_user_by_id(async_session, uuid.uuid4())
            assert user is None

        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_select_user_by_username():

    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record_1 = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser1", password="mypassword"),
            )
            new_record_2 = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser2", password="mypassword"),
            )
            new_record_3 = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser3", password="mypassword"),
            )
            new_record_4 = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser4", password="mypassword"),
            )
            await async_session.commit()
            await async_session.refresh(new_record_1)
            await async_session.refresh(new_record_2)
            await async_session.refresh(new_record_3)
            await async_session.refresh(new_record_4)
            user = await select_user_by_username(async_session, new_record_1.username)
            assert user == new_record_1
            user = await select_user_by_username(async_session, new_record_2.username)
            assert user == new_record_2
            user = await select_user_by_username(async_session, new_record_3.username)
            assert user == new_record_3
            user = await select_user_by_username(async_session, new_record_4.username)
            assert user == new_record_4

        finally:
            await reset_test_database()


@pytest.mark.asyncio
async def test_select_user_by_username_not_found():

    await setup_test_database()
    async with async_testing_session_scope() as async_session:
        try:
            new_record_1 = await insert_user(
                async_session,
                SchemaUserCreate(username="NewUser1", password="mypassword"),
            )
            await async_session.commit()
            await async_session.refresh(new_record_1)
            user = await select_user_by_username(async_session, "nonexistentusername")
            assert user is None

        finally:
            await reset_test_database()
