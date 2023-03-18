from sqlmodel import Session

from models.User import User
from requests import UserCreateRequest


class UserService:
    def __init__(self, session: Session):
        self.session = session

    async def create_user(self, data: UserCreateRequest):
        new_user = User(first_name=data.first_name, last_name=data.last_name, email=data.email)

        self.session.add(new_user)
        await self.session.commit()

        return new_user
