from pydantic import BaseModel


class NotFoundResponse(BaseModel):
    code: str
    message: str
    status_code: int
