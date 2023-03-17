from sqlmodel import SQLModel, Field
from typing import Optional

import sqlalchemy as sa


class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    todo_id: Optional[int] = Field(default=None, primary_key=True)
    label: str = Field(sa_column=sa.Column(sa.TEXT, nullable=False, unique=True))
