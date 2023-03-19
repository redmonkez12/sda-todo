from sqlmodel import Session, select, delete, update

from app.models.Todo import Todo
from app.requests import CreateTodoRequest, UpdateTodoRequest


class TodoService:
    def __init__(self, session: Session):
        self.session = session

    async def create_todo(self, data: CreateTodoRequest):
        new_todo = Todo(label=data.label, user_id=data.user_id)

        self.session.add(new_todo)
        await self.session.commit()

        return new_todo

    async def get_todo(self, todo_id):
        query = (
            select(Todo)
            .where(Todo.todo_id == todo_id)
        )

        result = await self.session.execute(query)
        return result.one()

    async def get_todos(self, page: int, limit: int):
        query = (
            select(Todo)
            .offset(page * limit)
            .limit(limit)
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
