from pydantic import BaseModel


class UpdateTodoRequest(BaseModel):
    todo_id: int
    label: str
