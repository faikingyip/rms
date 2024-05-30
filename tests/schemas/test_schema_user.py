import random
import string
import uuid
from datetime import datetime

import pytest
from pydantic import ValidationError

from src.schemas.schema_user import (
    SchemaChangePassword,
    SchemaUserCreate,
    SchemaUserDisplay,
)


def test_schema_user_create_new_instance():
    SchemaUserCreate(
        username="".join(random.choices(string.ascii_lowercase, k=300)),
        password="".join(random.choices(string.ascii_lowercase, k=30)),
    )


def test_schema_user_create_new_instance_no_username():
    with pytest.raises(ValidationError):
        SchemaUserCreate(
            username="", password="".join(random.choices(string.ascii_lowercase, k=30))
        )

    with pytest.raises(ValidationError):
        SchemaUserCreate(password="".join(random.choices(string.ascii_lowercase, k=30)))


def test_schema_user_create_new_instance_no_password():
    with pytest.raises(ValidationError):
        SchemaUserCreate(
            username="".join(random.choices(string.ascii_lowercase, k=300)), password=""
        )

    with pytest.raises(ValidationError):
        SchemaUserCreate(
            username="".join(random.choices(string.ascii_lowercase, k=300))
        )


def test_schema_user_create_new_instance_username_max_length():
    with pytest.raises(ValidationError):
        SchemaUserCreate(
            username="".join(random.choices(string.ascii_lowercase, k=301)),
            password="".join(random.choices(string.ascii_lowercase, k=30)),
        )


def test_schema_user_create_new_instance_password_max_length():
    with pytest.raises(ValidationError):
        SchemaUserCreate(
            username="".join(random.choices(string.ascii_lowercase, k=300)),
            password="".join(random.choices(string.ascii_lowercase, k=31)),
        )


def test_schema_user_display_new_instance():
    SchemaUserDisplay(
        id=uuid.uuid4(),
        username="".join(random.choices(string.ascii_lowercase, k=301)),
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )


def test_schema_user_display_new_instance_unset_data():

    with pytest.raises(ValidationError):
        SchemaUserDisplay(
            # id=None,
            username="".join(random.choices(string.ascii_lowercase, k=301)),
            created_on=datetime.now(),
            last_updated_on=datetime.now(),
        )

    with pytest.raises(ValidationError):
        SchemaUserDisplay(
            id=uuid.uuid4(),
            # username=None,
            created_on=datetime.now(),
            last_updated_on=datetime.now(),
        )

    with pytest.raises(ValidationError):
        SchemaUserDisplay(
            id=uuid.uuid4(),
            username="".join(random.choices(string.ascii_lowercase, k=301)),
            # created_on=None,
            last_updated_on=datetime.now(),
        )

    with pytest.raises(ValidationError):
        SchemaUserDisplay(
            id=uuid.uuid4(),
            username="".join(random.choices(string.ascii_lowercase, k=301)),
            created_on=datetime.now(),
            # last_updated_on=None,
        )


def test_schema_change_password_new_instance():
    SchemaChangePassword(
        new_password="".join(random.choices(string.ascii_lowercase, k=30))
    )


def test_schema_change_password_new_instance_no_password():
    with pytest.raises(ValidationError):
        SchemaChangePassword(new_password="")

    with pytest.raises(ValidationError):
        SchemaChangePassword()


def test_schema_change_password_new_instance_password_max_length():
    with pytest.raises(ValidationError):
        SchemaChangePassword(
            new_password="".join(random.choices(string.ascii_lowercase, k=31))
        )
