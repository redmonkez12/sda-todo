from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def starlette_http_error_handler(app):
    @app.exception_handler(StarletteHTTPException)
    async def unicorn_exception_handler(_: Request, e: StarletteHTTPException):
        if e.status_code == 401:
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "message": e.detail,
                    "status_code": e.status_code,
                    "code": "UNAUTHORIZED_ACCESS"
                },
            )

        return JSONResponse(
            status_code=e.status_code,
            content=e.detail,
        )
