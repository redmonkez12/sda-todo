from pydantic import BaseModel


class UserCreateResponse(BaseModel):
    user_id: int
    username: str
    first_name: str
    last_name: str
    email: str
    birthdate: str
