import random
import string
import uuid
from datetime import datetime

import pytest
from pydantic import ValidationError

from src.schemas.schema_menu import (
    SchemaMenuCreate,
    SchemaMenuDisplay,
    SchemaUpdateName,
)


def test_schema_menu_create_new_instance():
    SchemaMenuCreate(name="".join(random.choices(string.ascii_lowercase, k=50)))
    SchemaMenuCreate(name="A")


def test_schema_menu_create_new_instance_no_name():
    with pytest.raises(ValidationError):
        SchemaMenuCreate()

    with pytest.raises(ValidationError):
        SchemaMenuCreate(name="")

    with pytest.raises(ValidationError):
        SchemaMenuCreate(name=None)


def test_schema_menu_create_new_instance_name_max_length():
    with pytest.raises(ValidationError):
        SchemaMenuCreate(name="".join(random.choices(string.ascii_lowercase, k=51)))


def test_schema_menu_display_new_instance():
    SchemaMenuDisplay(
        id=uuid.uuid4(),
        name="".join(random.choices(string.ascii_lowercase, k=51)),
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )


def test_schema_menu_display_new_instance_unset_data():
    with pytest.raises(ValidationError):
        SchemaMenuDisplay(
            # id=uuid.uuid4(),
            name="".join(random.choices(string.ascii_lowercase, k=51)),
        )

        SchemaMenuDisplay(
            id=uuid.uuid4()
            # name="".join(random.choices(string.ascii_lowercase, k=51)),
        )


def test_schema_update_name_new_instance():
    SchemaUpdateName(name="".join(random.choices(string.ascii_lowercase, k=50)))
    SchemaUpdateName(name="A")


def test_schema_update_name_new_instance_no_data():
    with pytest.raises(ValidationError):
        SchemaUpdateName()

    with pytest.raises(ValidationError):
        SchemaUpdateName(name="")

    with pytest.raises(ValidationError):
        SchemaUpdateName(name=None)


def test_schema_update_name_new_instance_name_max_length():
    with pytest.raises(ValidationError):
        SchemaUpdateName(name="".join(random.choices(string.ascii_lowercase, k=51)))
