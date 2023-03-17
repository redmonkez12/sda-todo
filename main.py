import json

from fastapi import FastAPI, Response, status, Body, HTTPException, Depends

from database import init_db
from deps import get_todo_service
from error_responses import NotFoundResponse
from models.Todo import Todo
from request_examples import create_todo_example, update_todo_example
from requests import UpdateTodoRequest, CreateTodoRequest
from services.TodoService import TodoService

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


@app.get("/todos", response_model=list[Todo])
async def get_todos(*, todo_service: TodoService = Depends(get_todo_service)):
    todo_list = await todo_service.get_todos()

    return todo_list


@app.post("/todos", status_code=status.HTTP_201_CREATED, response_model=Todo)
async def create_todo(*, todo: CreateTodoRequest = Body(..., examples=create_todo_example),
                      todo_service: TodoService = Depends(get_todo_service),
                      ):

    new_todo = await todo_service.create_todo(todo)

    return Response(status_code=status.HTTP_201_CREATED, content=json.dumps({"id": new_todo.todo_id, "label": new_todo.label}))


@app.patch("/todos", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"model": NotFoundResponse}})
async def update_todo(*, todo: UpdateTodoRequest = Body(..., examples=update_todo_example),
                      todo_service: TodoService = Depends(get_todo_service),):
    await todo_service.update_todo(todo)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                     detail={
    #                         "message": f"Todo [{todo.id}] not found",
    #                         "status_code": status.HTTP_404_NOT_FOUND,
    #                         "code": "TODO_NOT_FOUND"
    #                     })


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"model": NotFoundResponse}})
async def delete_todo(*, todo_id: int, todo_service: TodoService = Depends(get_todo_service),):
    await todo_service.delete_todo(todo_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                     detail={
    #                         "message": f"Todo [{todo_id}] not found",
    #                         "status_code": status.HTTP_404_NOT_FOUND,
    #                         "code": "TODO_NOT_FOUND"
    #                     })
