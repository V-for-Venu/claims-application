from typing import Annotated

from claims_sql_data_model import Claims  # noqa: F401
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.config import settings

engine = create_async_engine(
    # Database URL/ Filename
    url=settings.POSTGRES_SERVER,
    # Print SQL Queries to the Console
    echo=True,
)


async def create_db_tables():
    async with engine.begin() as connection:
        await connection.run_async(SQLModel.metadata.create_all)


async def get_db_session():
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        print("DB Session Yielded Sucessfully...")
        yield session
        print("DB Session Closed Successfully...")


AsyncSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
