from presentation.error import BaseError
from presentation.schemas.error import ErrorLocationEnum
from presentation.status import Status


class CustomErrorTester(BaseError):
    code = "TESTING_CODE_ERROR"
    message = "TESTING MESSAGE"
    http_status = Status.BAD_REQUEST


def test_error():
    custom_error = CustomErrorTester(
        details="DETAILS TEST",
        location=ErrorLocationEnum.SERVER,
        param_extra_1="PARAM_1",
        param_extra_2="PARAM_2",
    )

    error_schema = custom_error.error_schema

    assert error_schema.get("code") == CustomErrorTester.code
    assert error_schema.get("message") == CustomErrorTester.message
    assert error_schema.get("details") == "DETAILS TEST"
    assert error_schema.get("param_extra_1") == "PARAM_1"
    assert error_schema.get("param_extra_2") == "PARAM_2"
