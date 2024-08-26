from enum import Enum
from typing import Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

ErrorSchemaT = TypeVar("ErrorSchemaT", bound="ErrorSchema")


class ErrorLocationEnum(str, Enum):
    PATH = "request.url.path"
    QUERY = "request.url.query_params"
    BODY = "request.body"
    HEADERS = "request.headers"
    AUTHORIZATION = "request.authorization"
    SERVER = "server"
    DATABASE = "database"


class ErrorSchema(BaseModel):
    code: str
    message: str
    details: str
    location: ErrorLocationEnum
    parameter: Optional[str] = None
    displayable_message: Optional[str] = Field(
        default=None, json_schema_extra={"hidden_for_external_response": True}
    )

    model_config = ConfigDict(
        populate_by_name=True, use_enum_values=True, extra="allow"
    )
