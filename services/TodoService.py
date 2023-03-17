from sqlmodel import Session, select, delete, update

from models.Todo import Todo
from requests import UpdateTodoRequest, CreateTodoRequest


class TodoService:
    def __init__(self, session: Session):
        self.session = session

    async def create_todo(self, data: CreateTodoRequest):
        new_todo = Todo(label=data.label)

        self.session.add(new_todo)
        await self.session.commit()

        return new_todo

    async def get_todos(self):
        query = (
            select(Todo)
        )

        data = await self.session.execute(query)
        return data.scalars().all()

    async def update_todo(self, new_todo: UpdateTodoRequest):
        query = (
            update(Todo)
            .values(label=new_todo.label)
            .where(Todo.todo_id == new_todo.todo_id)
        )

        await self.session.execute(query)
        await self.session.commit()

    async def delete_todo(self, todo_id: int):
        query = (
            delete(Todo)
            .where(Todo.todo_id == todo_id)
        )

        await self.session.execute(query)
        await self.session.commit()
