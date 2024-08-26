from typing import Optional

from presentation.error import InvalidParameterError, MissingParameterError
from presentation.response import Response
from presentation.schemas.error import ErrorLocationEnum


def destructuring(errors: list) -> list:
    """
    Formats pydantic error validation messages.

    :param errors: Errors' list from RequestValidationError.
    :return: Errors' list with a message ready to be displayed.
    """
    presentation_errors = []
    for e in errors:
        fields = e.get("loc")
        fields = (str(field) for field in fields)
        fields_as_string = "->".join(fields)
        msg = e.get("msg")
        _type = e.get("type")

        error = {
            "type": _type,
            "details": f"{msg}.".capitalize(),
            "parameter": fields_as_string,
        }
        if _type == "value_error.missing":
            error["displayable_message"] = (
                f"El siguiente campo es requerido: {fields_as_string}."
            )
        elif "type_error" in _type:
            if _type == "type_error.enum":
                allowed_values = [
                    enum.value for enum in e.get("ctx").get("enum_values")
                ]
                error["displayable_message"] = (
                    f"Formato invalido. El campo: {fields_as_string} "
                    f"solo admite los siguientes "
                    f"valores: {allowed_values}"
                )
            else:
                if len(_type.split(".")) > 1:
                    error["displayable_message"] = (
                        f"Formato invalido. El campo: {fields_as_string} "
                        f"debe tener formato: {_type.split('.')[1]}."
                    )
                elif _type == "type_error.none.not_allowed":
                    error["displayable_message"] = (
                        f"El campo: {fields_as_string} es requerido"
                    )
                else:
                    error["displayable_message"] = (
                        f"Formato invalido para el campo: {fields_as_string} "
                    )
        elif "assertion_error" in _type:
            error["displayable_message"] = (
                f"Valor invalido para el campo: {fields_as_string}."
            )
        else:
            error["displayable_message"] = (
                f"Error inesperado en el campo: {fields_as_string}."
            )
        if error:
            presentation_errors.append(error)
    return presentation_errors


def add_errors_to_response(
    response: Response,
    errors: list,
    location: Optional[ErrorLocationEnum] = None,
) -> None:
    if location is None:
        location = ErrorLocationEnum.BODY
    for _error in errors:
        error_data = (
            _error.get("details"),
            location,
            _error.get("parameter"),
            _error.get("displayable_message"),
        )
        if _error.get("type") == "value_error.missing":
            response.add_error(MissingParameterError(*error_data))
        else:
            response.add_error(InvalidParameterError(*error_data))
