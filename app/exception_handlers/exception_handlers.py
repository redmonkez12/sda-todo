from fastapi import FastAPI

from app.exception_handlers.RequestValidationErrorHandler import request_validation_error_handler
from app.exception_handlers.StarletterHttpErrorHandler import starlette_http_error_handler


def register_error_handlers(app: FastAPI):
    request_validation_error_handler(app)
    starlette_http_error_handler(app)
