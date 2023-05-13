from pydantic import BaseModel
from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from typing import Union

from app.auth.token import SECRET_KEY, ALGORITHM
from app.deps import get_user_service
from app.services.UserService import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenData(BaseModel):
    username: Union[str, None] = None


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_service: UserService = Depends(get_user_service)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await user_service.get_by_username(token_data.username)
    if user is None:
        raise credentials_exception

    return user
