from pydantic import BaseModel


class ErrorResponse(BaseModel):
    message: str
    code: str
    status_code: int
