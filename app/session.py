from typing import Annotated

from claims_sql_data_model import Claims  # noqa: F401
from fastapi import Depends
from sqlalchemy import AsyncSession, async_create_engine, sessionmaker
from sqlmodel import SQLModel

from app.config import settings

engine = async_create_engine(url=settings.POSTGRES_SERVER, echo=True)


async def create_db_tables():
    async with engine.begin() as connection:
        connection.run_async(SQLModel.metadata.create_all)


async def get_db_session():
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        print("DB Session Yielded Sucessfully...")
        yield session
        print("DB Session Closed Successfully...")


SessionDep = Annotated[AsyncSession, Depends(get_db_session)]
