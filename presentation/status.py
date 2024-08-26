from enum import Enum


class Status(Enum):
    OK = "OK", 200
    CREATED = "CREATED", 201
    ACCEPTED = "ACCEPTED", 202
    NO_CONTENT = "NO_CONTENT", 204
    ALREADY_REPORTED = "ALREADY_REPORTED", 208
    SEE_OTHER = "SEE_OTHER", 303
    BAD_REQUEST = "BAD_REQUEST", 400
    UNAUTHORIZED = "UNAUTHORIZED", 401
    PAYMENT_REQUIRED = "PAYMENT_REQUIRED", 402
    FORBIDDEN = "FORBIDDEN", 403
    NOT_FOUND = "NOT_FOUND", 404
    METHOD_NOT_ALLOWED = "METHOD_NOT_ALLOWED", 405
    NOT_ACCEPTABLE = "NOT_ACCEPTABLE", 406
    PROXY_AUTHENTICATION_REQUIRED = "PROXY_AUTHENTICATION_REQUIRED", 407
    REQUEST_TIMEOUT = "REQUEST_TIMEOUT", 408
    CONFLICT = "CONFLICT", 409
    GONE = "GONE", 410
    IM_A_TEAPOT = "IM_A_TEAPOT", 418
    UNPROCESSABLE_CONTENT = "UNPROCESSABLE_CONTENT", 422
    LOCKED = "LOCKED", 423
    FAILED_DEPENDENCY = "FAILED_DEPENDENCY", 424
    TOO_EARLY = "TOO_EARLY", 425
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS", 429
    UNAVAILABLE_FOR_LEGAL_REASONS = "UNAVAILABLE_FOR_LEGAL_REASONS", 451
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR", 500
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED", 501
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE", 503

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, _: str, code: int):
        self._code = code

    def __str__(self):
        return self.value

    @property
    def code(self):
        return self._code
