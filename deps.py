from database import async_session
from services.TodoService import TodoService


async def get_todo_service():
    async with async_session() as session:
        async with session.begin():
            yield TodoService(session)
