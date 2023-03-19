from fastapi import FastAPI

from app.controllers.Todo.TodoController import todo_router
from app.controllers.User.UserController import user_router
from app.controllers.UserTodo.UserTodoController import user_todo_router
from database import init_db

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

app.include_router(user_router, prefix="/api/v1")
app.include_router(user_todo_router, prefix="/api/v1")
app.include_router(todo_router, prefix="/api/v1")
