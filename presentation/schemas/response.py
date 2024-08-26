from time import time
from typing import List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from ..alias_generators import to_camel
from .error import ErrorSchema

ResponseSchemaT = TypeVar("ResponseSchemaT", bound="ResponseSchema")


class ResponseSchema(BaseModel):
    version: str = "1.0.0"
    status: str
    process_id: str
    timestamp: PositiveInt = Field(default_factory=lambda: int(time() * 1000))
    data: Optional[dict] = Field(
        default=None, json_schema_extra={"hidden_for_failed": True}
    )
    errors: Optional[List[ErrorSchema]] = Field(
        default=[], json_schema_extra={"hidden_for_success": True}
    )

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    def model_dump(
        self,
        external_response: bool = False,
        success: bool = False,
        failed: bool = False,
        **kwargs
    ):
        hidden_fields = {}
        if success:
            hidden_fields = {
                attribute_name: True
                for attribute_name, model_field in self.model_fields.items()
                if model_field.json_schema_extra is not None
                and model_field.json_schema_extra.get("hidden_for_success")
                is True
            }
        if failed:
            hidden_fields = {
                attribute_name: True
                for attribute_name, model_field in self.model_fields.items()
                if model_field.json_schema_extra is not None
                and model_field.json_schema_extra.get("hidden_for_failed")
                is True
            }

        if external_response:
            ResponseSchema.hidde_fields_from_errors(hidden_fields)

        kwargs.setdefault("exclude", hidden_fields)
        return super().model_dump(**kwargs)

    @staticmethod
    def hidde_fields_from_errors(hidden_fields):
        if "errors" not in hidden_fields:
            fields_to_hidde = set()
            for (
                attribute_name,
                model_field,
            ) in ErrorSchema.model_fields.items():
                if (
                    model_field.json_schema_extra is not None
                    and model_field.json_schema_extra.get(
                        "hidden_for_external_response"
                    )
                ):
                    fields_to_hidde.add(attribute_name)

            hidden_fields.update({"errors": {"__all__": fields_to_hidde}})
