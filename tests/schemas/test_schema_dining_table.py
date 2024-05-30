import random
import string
import uuid
from datetime import datetime

import pytest
from pydantic import ValidationError

from src.schemas.schema_dining_table import (
    SchemaDiningTableCreate,
    SchemaDiningTableDisplay,
    SchemaUpdateName,
    SchemaUpdatePosition,
    SchemaUpdateSize,
)


def test_schema_dining_table_create_new_instance():
    SchemaDiningTableCreate(
        name="".join(random.choices(string.ascii_lowercase, k=30)),
        x=5,
        y=10,
        width=100,
        height=200,
    )

    SchemaDiningTableCreate(
        name="".join(random.choices(string.ascii_lowercase, k=1)),
        x=5,
        y=10,
        width=100,
        height=200,
    )


def test_schema_dining_table_create_new_instance_no_name():
    with pytest.raises(ValidationError):
        SchemaDiningTableCreate(
            name="",
            x=5,
            y=10,
            width=100,
            height=200,
        )

    with pytest.raises(ValidationError):
        SchemaDiningTableCreate(
            # name=None,
            x=5,
            y=10,
            width=100,
            height=200,
        )


def test_schema_dining_table_create_new_instance_name_max_length():
    with pytest.raises(ValidationError):
        SchemaDiningTableCreate(
            name="".join(random.choices(string.ascii_lowercase, k=31)),
            x=5,
            y=10,
            width=100,
            height=200,
        )


def test_schema_dining_table_create_new_instance_xy_lt_zero():
    with pytest.raises(ValidationError):
        SchemaDiningTableCreate(
            name="".join(random.choices(string.ascii_lowercase, k=30)),
            x=-1,
            y=10,
            width=100,
            height=200,
        )

    with pytest.raises(ValidationError):
        SchemaDiningTableCreate(
            name="".join(random.choices(string.ascii_lowercase, k=30)),
            x=10,
            y=-1,
            width=100,
            height=200,
        )


def test_schema_dining_table_create_new_instance_wh_lt_min():
    with pytest.raises(ValidationError):
        SchemaDiningTableCreate(
            name="".join(random.choices(string.ascii_lowercase, k=30)),
            x=10,
            y=10,
            width=9,
            height=100,
        )

    with pytest.raises(ValidationError):
        SchemaDiningTableCreate(
            name="".join(random.choices(string.ascii_lowercase, k=30)),
            x=10,
            y=-1,
            width=100,
            height=9,
        )


def test_schema_dining_table_display_new_instance():
    SchemaDiningTableDisplay(
        id=uuid.uuid4(),
        name="".join(random.choices(string.ascii_lowercase, k=31)),
        x=10,
        y=10,
        width=100,
        height=100,
        created_on=datetime.now(),
        last_updated_on=datetime.now(),
    )


def test_schema_dining_table_display_new_instance_unset_data():
    with pytest.raises(ValidationError):
        SchemaDiningTableDisplay(
            # id=uuid.uuid4(),
            name="".join(random.choices(string.ascii_lowercase, k=31)),
            x=10,
            y=10,
            width=100,
            height=100,
            created_on=datetime.now(),
            last_updated_on=datetime.now(),
        )

    with pytest.raises(ValidationError):
        SchemaDiningTableDisplay(
            id=uuid.uuid4(),
            # name="".join(random.choices(string.ascii_lowercase, k=31)),
            x=10,
            y=10,
            width=100,
            height=100,
            created_on=datetime.now(),
            last_updated_on=datetime.now(),
        )

    with pytest.raises(ValidationError):
        SchemaDiningTableDisplay(
            id=uuid.uuid4(),
            name="".join(random.choices(string.ascii_lowercase, k=31)),
            # x=10,
            y=10,
            width=100,
            height=100,
            created_on=datetime.now(),
            last_updated_on=datetime.now(),
        )

    with pytest.raises(ValidationError):
        SchemaDiningTableDisplay(
            id=uuid.uuid4(),
            name="".join(random.choices(string.ascii_lowercase, k=31)),
            x=10,
            # y=10,
            width=100,
            height=100,
            created_on=datetime.now(),
            last_updated_on=datetime.now(),
        )

    with pytest.raises(ValidationError):
        SchemaDiningTableDisplay(
            id=uuid.uuid4(),
            name="".join(random.choices(string.ascii_lowercase, k=31)),
            x=10,
            y=10,
            # width=100,
            height=100,
            created_on=datetime.now(),
            last_updated_on=datetime.now(),
        )

    with pytest.raises(ValidationError):
        SchemaDiningTableDisplay(
            id=uuid.uuid4(),
            name="".join(random.choices(string.ascii_lowercase, k=31)),
            x=10,
            y=10,
            width=100,
            # height=100,
            created_on=datetime.now(),
            last_updated_on=datetime.now(),
        )

    with pytest.raises(ValidationError):
        SchemaDiningTableDisplay(
            id=uuid.uuid4(),
            name="".join(random.choices(string.ascii_lowercase, k=31)),
            x=10,
            y=10,
            width=100,
            height=100,
            # created_on=datetime.now(),
            last_updated_on=datetime.now(),
        )

    with pytest.raises(ValidationError):
        SchemaDiningTableDisplay(
            id=uuid.uuid4(),
            name="".join(random.choices(string.ascii_lowercase, k=31)),
            x=10,
            y=10,
            width=100,
            height=100,
            created_on=datetime.now(),
            # last_updated_on=datetime.now(),
        )


def test_schema_update_position_new_instance():
    SchemaUpdatePosition(x=5, y=10)

    SchemaUpdatePosition(x=0, y=0)


def test_schema_update_position_new_instance_xy_below_min():
    with pytest.raises(ValidationError):
        SchemaUpdatePosition(x=-1, y=0)

    with pytest.raises(ValidationError):
        SchemaUpdatePosition(x=0, y=-1)


def test_schema_update_position_new_instance_xy_no_data():
    with pytest.raises(ValidationError):
        SchemaUpdatePosition(y=10)

    with pytest.raises(ValidationError):
        SchemaUpdatePosition(x=10)


def test_schema_update_size_new_instance():
    SchemaUpdateSize(width=50, height=100)

    SchemaUpdateSize(width=10, height=10)


def test_schema_update_size_new_instance_wh_below_min():
    with pytest.raises(ValidationError):
        SchemaUpdateSize(width=-9, height=10)

    with pytest.raises(ValidationError):
        SchemaUpdateSize(width=10, height=9)


def test_schema_update_size_new_instance_wh_no_data():
    with pytest.raises(ValidationError):
        SchemaUpdateSize(height=10)

    with pytest.raises(ValidationError):
        SchemaUpdateSize(width=10)


def test_schema_update_name_new_instance():
    SchemaUpdateName(name="".join(random.choices(string.ascii_lowercase, k=30)))
    SchemaUpdateName(name="A")


def test_schema_update_name_new_instance_no_data():
    with pytest.raises(ValidationError):
        SchemaUpdateName()

    with pytest.raises(ValidationError):
        SchemaUpdateName(name="")

    with pytest.raises(ValidationError):
        SchemaUpdateName(name=None)
