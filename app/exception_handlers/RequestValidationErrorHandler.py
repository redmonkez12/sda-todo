from fastapi import status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def request_validation_error_handler(app):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError):
        errors = exc.errors()

        error_messages = []

        for error in errors:
            if error["msg"] == "field required":
                field = errors[0]['loc'][1]
                error_messages.append({
                    "error": f"The field {field} is required",
                    "code": f"{field.upper()}_REQUIRED"

                })
            else:
                field = "unknown"
                error_messages.append({
                    "error": f"Unknown error",
                    "code": f"{field.upper()}_REQUIRED"
                })

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({
                "messages": error_messages,
                "code": "INVALID_REQUEST",
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            }),
        )