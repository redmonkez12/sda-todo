from pydantic import BaseModel


class CreateTodoRequest(BaseModel):
    label: str
