from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

from .claims_sql_data_model import Claims  # noqa: F401

engine = create_engine(
    "sqlite:///new_database/claims.db",
    echo=True,
    connect_args={"check_same_thread": False},
)


def create_db_tables():
    SQLModel.metadata.create_all(bind=engine)


def get_db_session():
    with Session(bind=engine) as session:
        print("DB Session Yielded Sucessfully...")
        yield session
        print("DB Session Closed Successfully...")


SessionDep = Annotated[Session, Depends(get_db_session)]
