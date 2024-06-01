from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SchemaTagCreate(BaseModel):
    name: str = Field(description="name", min_length=1, max_length=50)

    model_config = ConfigDict(json_schema_extra={"examples": [{"name": "name"}]})


class SchemaTagDisplay(BaseModel):
    id: UUID
    name: str
    created_on: datetime
    last_updated_on: datetime

    model_config = ConfigDict(from_attributes=True)


class SchemaUpdateName(BaseModel):
    name: str = Field(description="name", min_length=1, max_length=50)

    model_config = ConfigDict(json_schema_extra={"examples": [{"name": "name"}]})
