from typing import Optional

from .schemas.error import ErrorLocationEnum
from .status import Status


class _Error(Exception):
    __version__ = "1.0.0"
    ERROR_LOCATION = ErrorLocationEnum

    def __init__(
        self,
        code: str,
        message: str,
        details: str,
        location: ErrorLocationEnum,
        parameter: Optional[str] = None,
        displayable_message: Optional[str] = None,
        **kwargs,
    ):
        self.code = code
        self.message = message
        self.details = details
        self.location = location
        self.parameter = parameter
        self.displayable_message = displayable_message
        self.kwargs = kwargs

    @property
    def error_schema(self):
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
            "location": self.location,
            "parameter": self.parameter,
            "displayable_message": self.displayable_message,
            **self.kwargs,
        }


class BaseError(_Error):
    code: str
    message: str
    http_status: Status

    def __init__(
        self,
        details: str,
        location: ErrorLocationEnum,
        parameter: Optional[str] = None,
        displayable_message: Optional[str] = None,
        **kwargs,
    ):
        if (
            getattr(self, "code", None) is None
            or getattr(self, "message", None) is None
            or getattr(self, "http_status", None) is None
        ):
            raise TypeError(
                f"'code', 'message', 'http_status' attributes "
                f"must be setted at {self.__class__.__name__}"
            )
        super().__init__(
            self.code,
            self.message,
            details,
            location.value,
            parameter,
            displayable_message,
            **kwargs,
        )


class AlreadyExistsError(BaseError):
    code: str = "ALREADY_EXISTS"
    message: str = "The resource you tried to create already exists."
    http_status = Status.ALREADY_REPORTED


class AuthenticationError(BaseError):
    code: str = "UNAUTHORIZED"
    message: str = "The request lacks valid authentication credentials."
    http_status = Status.UNAUTHORIZED


class DefaultError(BaseError):
    code: str = "UNEXPECTED_ERROR"
    message: str = "An unexpected error occurred. Please try again."
    details: str = "If the problem consist, please report it."
    location: ErrorLocationEnum = ErrorLocationEnum.SERVER
    http_status = Status.INTERNAL_SERVER_ERROR

    def __init__(self):
        super().__init__(
            self.details,
            self.location,
        )


class IllegalCharactersError(BaseError):
    code: str = "ILLEGAL_CHARACTERS"
    message: str = "There is an invalid or unexpected character."
    http_status = Status.BAD_REQUEST


class InvalidParameterError(BaseError):
    code: str = "INVALID_PARAMETER"
    message: str = "A value provided as parameter is not valid for the request."
    http_status = Status.BAD_REQUEST


class MissingParameterError(BaseError):
    code: str = "MISSING_PARAMETER"
    message: str = "The request is missing a required parameter."
    http_status = Status.BAD_REQUEST


class NotFoundError(BaseError):
    code: str = "NOT_FOUND"
    message: str = "The specified resource was not found."
    http_status = Status.NOT_FOUND


class ForbiddenError(BaseError):
    code: str = "FORBIDDEN"
    message: str = "The request has been understood but server refuses to authorize it."
    http_status = Status.FORBIDDEN
