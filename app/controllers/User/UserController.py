from fastapi import Depends, Response, status, Body, APIRouter, HTTPException
import json
from sqlalchemy.orm.exc import NoResultFound

from app.auth.token import create_access_token
from app.auth.user import get_current_user
from app.controllers.User.api_examples import change_password_example, register_example, register_error_responses
from app.controllers.User.api_examples import login_example
from app.deps import get_user_service
from app.exceptions.EmailDuplicationException import EmailDuplicationException
from app.exceptions.UserNotFoundException import UserNotFoundException
from app.requests.LoginRequest import LoginRequest
from app.requests.ChangePasswordRequest import ChangePasswordRequest
from app.requests.DeleteTodoRequest import UserCreateRequest
from app.responses.GetByUsernameResponse import GetByUsernameResponse
from app.services.UserService import UserService

user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@user_router.post("/", response_class=Response, status_code=status.HTTP_201_CREATED, responses=register_error_responses)
async def create_user(*, user_service: UserService = Depends(get_user_service),
                      request: UserCreateRequest = Body(..., examples=register_example)):
    try:
        await user_service.create_user(request)
        return Response(status_code=status.HTTP_201_CREATED)
    except EmailDuplicationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
            "message": str(e),
            "code": "EMAIL_DUPLICATION",
            "status_code": status.HTTP_409_CONFLICT,
        })
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
            "message": "Something went wrong",
            "code": "INTERNAL_SERVER_ERROR",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        })


@user_router.post("/login")
async def login(*, user_service: UserService = Depends(get_user_service),
                request: LoginRequest = Body(..., examples=login_example)):
    try:
        user = await user_service.login(request)

        access_token = create_access_token(
            data={"sub": user.username}
        )

        return Response(status_code=status.HTTP_200_OK,
                        content=json.dumps({"access_token": access_token, "token_type": "bearer"}))
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password or username")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
            "message": "Something went wrong",
            "code": "INTERNAL_SERVER_ERROR",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        })


@user_router.patch("/password")
async def change_password(*, user_service: UserService = Depends(get_user_service),
                          request: ChangePasswordRequest = Body(..., examples=change_password_example),
                          current_user: GetByUsernameResponse = Depends(get_current_user)
                          ):
    try:
        await user_service.change_password(current_user, request)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "code": "INVALID_PASSWORD", "status": status.HTTP_400_BAD_REQUEST, },
        )
    except Exception as e:
        print(e)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Something went wrong")
