from pydantic import BaseModel


class UserCreateTodoResponse(BaseModel):
    todo_id: int
    label: str
    created_at: str
