from typing import Any

from presentation.logger import Logger

from .alias_generators import dict_to_camel
from .error import BaseError
from .schemas.error import ErrorSchema
from .schemas.response import ResponseSchema
from .status import Status


class Response:
    __version__ = "1.0.0"

    def __init__(
        self,
        logger: Logger = None,
        external_response: bool = False,
        version: str = __version__,
    ):
        self._errors = []
        self._data = {}
        self._status: Status = Status.BAD_REQUEST
        self._metadata = None
        self._logger = logger or Logger()
        self._external_response = external_response
        self._version = version

    @property
    def logger(self) -> Logger:
        return self._logger

    @property
    def metadata(self) -> Any:
        return self._metadata

    @metadata.setter
    def metadata(self, value: Any) -> None:
        self._metadata = value

    @property
    def version(self) -> str:
        return self.__version__

    @property
    def status(self) -> Status:
        return self._status.value

    @property
    def data(self) -> dict:
        return self._data

    @property
    def errors(self) -> list:
        return self._errors

    @property
    def code(self) -> int:
        return self._status.code

    @status.setter
    def status(self, value: Status) -> None:
        if value not in Status:
            raise ValueError(f"{value} not member of Status Enum")
        self._status = value

    @property
    def response(self) -> dict:
        if self._external_response:
            self._data = dict_to_camel(self._data)

        response = ResponseSchema(
            errors=self._errors,
            data=self._data,
            status=self._status.value,
            version=self._version,
            process_id=self._logger.process_id,
        )
        if self.code >= 400:
            return response.model_dump(
                external_response=self._external_response,
                failed=True,
                by_alias=self._external_response,
            )
        elif self.code >= 200:
            return response.model_dump(
                external_response=self._external_response,
                success=True,
                by_alias=self._external_response,
            )
        return response.model_dump(by_alias=self._external_response)

    def update_data(self, result: dict) -> None:
        self._data.update(result)

    def add_error(self, code: BaseError) -> None:
        error = ErrorSchema(**code.error_schema)
        self._errors.append(error.model_dump())
