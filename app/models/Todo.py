import datetime

from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from typing import Optional

import sqlalchemy as sa

from app.models.User import User


class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    todo_id: Optional[int] = Field(default=None, primary_key=True)
    label: str = Field(sa_column=sa.Column(sa.TEXT, nullable=False))
    user_id: int = Field(sa_column=sa.Column(sa.Integer, sa.ForeignKey(User.user_id, ondelete="CASCADE"), nullable=False))
    created_at: datetime.datetime = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True), default=datetime.datetime.now()))

    user: User = Relationship(back_populates="todos", sa_relationship_kwargs={'lazy': 'joined'})

    __table_args__ = (
        UniqueConstraint("label", "user_id", name="unique_todos_user_id_label"),
    )
