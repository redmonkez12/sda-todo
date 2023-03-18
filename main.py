import json

from fastapi import FastAPI, Response, status, Body, HTTPException, Depends

from database import init_db
from deps import get_todo_service, get_user_service
from error_responses import NotFoundResponse
from models.Todo import Todo
from request_examples import create_todo_example, update_todo_example
from requests import UpdateTodoRequest, CreateTodoRequest, UserCreateRequest
from services.TodoService import TodoService
from services.UserService import UserService

app = FastAPI(
    title="Todo list app",
    description="You can create your own todos",
    version="0.0.1",
)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
async def index():
    return {"message": "Api is running"}


@app.get("/todos/{todo_id}")
async def get_todo(*, todo_id: int, todo_service: TodoService = Depends(get_todo_service)):
    todo = await todo_service.get_todo(todo_id)

    return todo


@app.get("/todos", response_model=list[Todo])
async def get_todos(*, todo_service: TodoService = Depends(get_todo_service)):
    todo_list = await todo_service.get_todos()

    return todo_list


@app.post("/users")
async def create_user(*, user_service: UserService = Depends(get_user_service), request: UserCreateRequest = Body(...)):
    new_user = await user_service.create_user(request)

    return Response(status_code=status.HTTP_201_CREATED,
                    content=json.dumps({"id": new_user.user_id,
                                        "last_name": new_user.last_name,
                                        "first_name": new_user.first_name,
                                        "email": new_user.email,
                                        }))


@app.post("/users/{user_id}/todos", status_code=status.HTTP_201_CREATED, response_model=Todo)
async def create_todo(*, todo: CreateTodoRequest = Body(..., examples=create_todo_example),
                      todo_service: TodoService = Depends(get_todo_service),
                      user_id: int
                      ):
    new_todo = await todo_service.create_todo(todo, user_id)

    return Response(status_code=status.HTTP_201_CREATED,
                    content=json.dumps({"id": new_todo.todo_id, "label": new_todo.label}))


@app.patch("/todos", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"model": NotFoundResponse}})
async def update_todo(*, todo: UpdateTodoRequest = Body(..., examples=update_todo_example),
                      todo_service: TodoService = Depends(get_todo_service), ):
    await todo_service.update_todo(todo)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                     detail={
    #                         "message": f"Todo [{todo.id}] not found",
    #                         "status_code": status.HTTP_404_NOT_FOUND,
    #                         "code": "TODO_NOT_FOUND"
    #                     })


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"model": NotFoundResponse}})
async def delete_todo(*, todo_id: int, todo_service: TodoService = Depends(get_todo_service), ):
    await todo_service.delete_todo(todo_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                     detail={
    #                         "message": f"Todo [{todo_id}] not found",
    #                         "status_code": status.HTTP_404_NOT_FOUND,
    #                         "code": "TODO_NOT_FOUND"
    #                     })
