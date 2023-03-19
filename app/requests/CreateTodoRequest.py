from pydantic import BaseModel


class CreateTodoRequest(BaseModel):
    user_id: int
    label: str
