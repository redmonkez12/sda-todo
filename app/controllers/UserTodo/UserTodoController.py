from fastapi import APIRouter, status, Response, Body, Depends, HTTPException
import json

from app.auth.user import get_current_user
from app.controllers.Todo.api_examples import create_todo_example, update_todo_example
from app.deps import get_user_todo_service
from app.responses.GetByUsernameResponse import GetByUsernameResponse
from error_response import ErrorResponse
from app.requests.CreateTodoRequest import CreateTodoRequest
from app.requests.UpdateTodoRequest import UpdateTodoRequest
from app.services.TodoService import TodoService

user_todo_router = APIRouter(
    prefix="/users/todos",
    tags=["User todos"]
)


@user_todo_router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_todo(*, todo: CreateTodoRequest = Body(..., examples=create_todo_example),
                      todo_service: TodoService = Depends(get_user_todo_service),
                      current_user: GetByUsernameResponse = Depends(get_current_user),
                      ):
    try:
        new_todo = await todo_service.create_todo(todo, current_user.user_id)

        return Response(status_code=status.HTTP_201_CREATED,
                        content=json.dumps(
                            {
                                "todo_id": new_todo.todo_id,
                                "label": new_todo.label,
                                "created_at": new_todo.created_at.isoformat(),
                            }
                        ))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something weng wrong")


@user_todo_router.get("/{todo_id}")
async def get_todo(*, todo_id: int, todo_service: TodoService = Depends(get_user_todo_service)):
    todo = await todo_service.get_todo(todo_id)

    return todo


@user_todo_router.patch("/", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"model": ErrorResponse}})
async def update_todo(*, todo: UpdateTodoRequest = Body(..., examples=update_todo_example),
                      todo_service: TodoService = Depends(get_user_todo_service), ):
    await todo_service.update_todo(todo)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                     detail={
    #                         "message": f"Todo [{todo.id}] not found",
    #                         "status_code": status.HTTP_404_NOT_FOUND,
    #                         "code": "TODO_NOT_FOUND"
    #                     })


@user_todo_router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT,
                         responses={404: {"model": ErrorResponse}})
async def delete_todo(*, todo_id: int, todo_service: TodoService = Depends(get_user_todo_service), ):
    await todo_service.delete_todo(todo_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                     detail={
    #                         "message": f"Todo [{todo_id}] not found",
    #                         "status_code": status.HTTP_404_NOT_FOUND,
    #                         "code": "TODO_NOT_FOUND"
    #                     })
