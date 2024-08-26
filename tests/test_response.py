from presentation.error import AlreadyExistsError
from presentation.response import Response
from presentation.schemas.error import ErrorLocationEnum
from presentation.status import Status
from tests.test_error import CustomErrorTester


def test_default_response_data():
    response = Response()
    assert response.version == "1.0.0"
    assert response.status == Status.BAD_REQUEST.value
    assert response.errors == []
    assert response.data == {}


def test_response_with_data():
    response = Response()
    response.status = Status.OK
    data = {"pytest": "pytest"}
    response.update_data(data)
    assert response.response.get("data") == data


def test_response_with_status():
    response = Response()
    response.status = Status.OK
    assert response.status == Status.OK.value


def test_response_dict():
    # We need to test response.response
    pass


def test_predefined_error():
    response = Response()
    already_exist_error = AlreadyExistsError(
        details="TESTING DETAILS",
        location=ErrorLocationEnum.SERVER,
    )
    response.add_error(already_exist_error)
    result = response.response
    error = result.get("errors")[0]

    assert error.get("code") == AlreadyExistsError.code
    assert error.get("message") == AlreadyExistsError.message
    assert error.get("details") == "TESTING DETAILS"


def test_custom_error():
    response = Response()
    custom_error = CustomErrorTester(
        details="TESTING DETAILS",
        location=ErrorLocationEnum.SERVER,
        displayable_message="DISPLAY MESSAGE TEST",
        param_extra_1="PARAM_1",
        param_extra_2="PARAM_2",
    )
    response.add_error(custom_error)
    result = response.response
    error = result.get("errors")[0]

    assert error.get("code") == CustomErrorTester.code
    assert error.get("message") == CustomErrorTester.message
    assert error.get("details") == "TESTING DETAILS"
    assert error.get("displayable_message") == "DISPLAY MESSAGE TEST"
    assert error.get("location") == ErrorLocationEnum.SERVER
    assert error.get("param_extra_1") == "PARAM_1"
    assert error.get("param_extra_2") == "PARAM_2"
