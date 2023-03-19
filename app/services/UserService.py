import asyncpg
from sqlmodel import Session, select
from sqlalchemy import exc, func

from app.auth.password import verify_password, get_password_hash
from app.exceptions import EmailDuplicationException
from app.exceptions.UserNotFoundException import UserNotFoundException
from app.models.User import User
from app.models.UserPassword import UserPassword
from app.requests.ChangePasswordRequest import ChangePasswordRequest
from app.requests.DeleteTodoRequest import UserCreateRequest
from app.requests.LoginRequest import LoginRequest


class UserService:
    def __init__(self, session: Session):
        self.session = session

    async def create_user(self, data: UserCreateRequest):
        try:
            new_user = User(
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                birthdate=data.birthdate,
                username=data.username,
                passwords=[UserPassword(value=get_password_hash(data.password))],
            )

            self.session.add(new_user)
            await self.session.commit()

            return new_user
        except (exc.IntegrityError, asyncpg.exceptions.UniqueViolationError):
            raise EmailDuplicationException(f"Email [{data.email}] already exists")
        except Exception as e:
            raise Exception(e)

    async def get_by_username(self, username: str):
        query = (
            select(User.user_id, User.username, User.email, UserPassword.value.label("password"))
            .join(UserPassword)
            .where(User.username == username)
            .limit(1)
        )

        result = await self.session.execute(query)
        return result.first()

    async def login(self, data: LoginRequest):
        user = await self.get_by_username(data.username)

        if not user:
            raise UserNotFoundException("Username or password is invalid")

        if not verify_password(data.password, user.password):
            raise UserNotFoundException("Username or password is invalid")

        return user

    async def change_password(self, user: User, request_data: ChangePasswordRequest):
        if not verify_password(request_data.old_password, user.password):
            raise UserNotFoundException("Password is invalid")

        query = (
            select(UserPassword)
            .where(UserPassword.user_id == user.user_id)
            .limit(1)
        )

        data = await self.session.execute(query)
        user_password = data.scalars().first()

        user_password.value = get_password_hash(request_data.new_password)
        user_password.updated_at = func.now()

        await self.session.commit()
