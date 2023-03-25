from sqlmodel import Session, select, and_

from app.models.Todo import Todo
from app.requests.CreateTodoRequest import CreateTodoRequest


class UserTodoService:
    def __init__(self, session: Session):
        self.session = session

    async def create_todo(self, data: CreateTodoRequest, user_id: str):
        new_todo = Todo(label=data.label, user_id=user_id)

        self.session.add(new_todo)
        await self.session.commit()

        return new_todo

    async def get_todos(self, user_id: int):
        query = (
            select(Todo)
            .where(Todo.user_id == user_id)
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_todo(self, user_id: int, todo_id: int):
        query = (
            select(Todo)
            .where(and_(Todo.user_id == user_id, Todo.todo_id == todo_id))
        )

        result = await self.session.execute(query)
        return result.one()

    async def delete_todo(self, user_id: int, todo_id: int):
        pass

    async def update_todo(self):
        pass
