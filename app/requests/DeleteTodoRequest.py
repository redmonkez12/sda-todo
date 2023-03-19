from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    birthdate: str
    username: str
    password: str
