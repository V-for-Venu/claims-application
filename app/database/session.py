from config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

engine = create_async_engine(
    # Database URL/ Filename
    url=settings.DATABASE_URL,
    # Print SQL Queries to the Console
    echo=True,
)


async def create_db_tables():
    async with engine.begin() as connection:
        from database.claim_sql_model import Claims  # noqa: F401

        await connection.run_sync(SQLModel.metadata.create_all)


async def get_db_session():
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        print("DB Session Yielded Sucessfully...")
        yield session
        print("DB Session Closed Successfully...")
