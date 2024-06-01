import random
import string
import uuid
from datetime import datetime

import pytest
from pydantic import ValidationError

from src.schemas.schema_tag import SchemaTagCreate, SchemaTagDisplay, SchemaUpdateName


def test_schema_tag_create_new_instance():
    SchemaTagCreate(name="".join(random.choices(string.ascii_lowercase, k=50)))
    SchemaTagCreate(name="A")


def test_schema_tag_create_new_instance_no_name():
    with pytest.raises(ValidationError):
        SchemaTagCreate()

    with pytest.raises(ValidationError):
        SchemaTagCreate(name="")

    with pytest.raises(ValidationError):
        SchemaTagCreate(name=None)


def test_schema_tag_create_new_instance_name_max_length():
    with pytest.raises(ValidationError):
        SchemaTagCreate(name="".join(random.choices(string.ascii_lowercase, k=51)))


def test_schema_tag_display_new_instance():
    SchemaTagDisplay(
        id=uuid.uuid4(),
        name="".join(random.choices(string.ascii_lowercase, k=51)),
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )


def test_schema_tag_display_new_instance_unset_data():
    with pytest.raises(ValidationError):
        SchemaTagDisplay(
            # id=uuid.uuid4(),
            name="".join(random.choices(string.ascii_lowercase, k=51)),
        )

        SchemaTagDisplay(
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
