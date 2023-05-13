from fastapi import Depends, APIRouter, Query, status, HTTPException
from typing_extensions import Annotated

from sqlalchemy.exc import NoResultFound
from typing import List

from app.deps import get_todo_service
from app.models.Todo import Todo
from app.services.TodoService import TodoService

todo_router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)


@todo_router.get("/", response_model=List[Todo])
async def get_todos(*,
                    todo_service: TodoService = Depends(get_todo_service),
                    page: Annotated[int, Query()],
                    limit: Annotated[int, Query()],
                ):
    todo_list = await todo_service.get_todos(page, limit)

    return todo_list


@todo_router.get("/{todo_id}", response_model=Todo)
async def get_todo(*, todo_service: TodoService = Depends(get_todo_service), todo_id: int):
    try:
        return await todo_service.get_todo(todo_id)
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={
                                "message": f"Todo [{todo_id}] not found",
                                "status_code": status.HTTP_404_NOT_FOUND,
                                "code": "TODO_NOT_FOUND",
                            })
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={
                                "message": "Something went wrong",
                                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                                "code": "INTERNAL_SERVER_ERROR",
                            })