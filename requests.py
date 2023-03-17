from pydantic import BaseModel


class CreateTodoRequest(BaseModel):
    label: str


class UpdateTodoRequest(BaseModel):
    todo_id: int
    label: str
