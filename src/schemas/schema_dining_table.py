from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SchemaDiningTableCreate(BaseModel):
    name: str = Field(description="name", min_length=1, max_length=30)
    x: int = Field(description="x", ge=0)
    y: int = Field(description="y", ge=0)
    width: int = Field(description="width", ge=10)
    height: int = Field(description="height", ge=10)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"name": "name", "x": 30, "y": 50, "width": 100, "height": 100}
            ]
        }
    )


class SchemaDiningTableDisplay(BaseModel):
    id: UUID
    name: str
    x: int
    y: int
    width: int
    height: int
    created_on: datetime
    last_updated_on: datetime

    model_config = ConfigDict(from_attributes=True)


class SchemaUpdatePosition(BaseModel):
    x: int = Field(description="x", ge=0)
    y: int = Field(description="y", ge=0)

    model_config = ConfigDict(json_schema_extra={"examples": [{"x": 30, "y": 50}]})


class SchemaUpdateSize(BaseModel):
    width: int = Field(description="width", ge=10)
    height: int = Field(description="height", ge=10)

    model_config = ConfigDict(
        json_schema_extra={"examples": [{"width": 100, "height": 100}]}
    )


class SchemaUpdateName(BaseModel):
    name: str = Field(description="name", min_length=1, max_length=30)

    model_config = ConfigDict(json_schema_extra={"examples": [{"name": "name"}]})
