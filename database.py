from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

config = dotenv_values("./.env")
username = config.get("DB_USERNAME")
password = config.get("DB_PASSWORD")
dbname = config.get("DB_NAME")

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{username}:{password}@localhost:5432/{dbname}"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)


async def init_db():
    async with engine.begin() as conn:
        # tables = SQLModel.metadata.tables.values()
        # print(tables)
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
