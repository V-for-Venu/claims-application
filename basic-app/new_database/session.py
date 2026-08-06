from sqlalchemy import create_engine
from sqlmodel import SQLModel
from claims_sql_data_model import Claims

engine = create_engine(
    "sqlite:///claims.db", 
    echo=True, 
    connect_args={"check_same_thread": False}
)

SQLModel.metadata.create_all(bind=engine)
