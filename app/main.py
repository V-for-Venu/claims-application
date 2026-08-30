from contextlib import asynccontextmanager

from database.session import create_db_tables
from fastapi import FastAPI
from rich import panel, print
from scalar_fastapi import get_scalar_api_reference

# from claims_data import claims_data - Old Claims Data - Not Required
from app.api.router import router

# from utils import claim_exists - Old Check for Claim Existence - Not Required


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("...Server Started...", border_style="green"))
    create_db_tables()
    yield
    print(panel.Panel("...Server Stopped...", border_style="red"))


app = FastAPI(lifespan=lifespan_handler)
app.include_router(router=router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/scalar")
async def scalar_html():
    return get_scalar_api_reference(openapi_url=app.openapi_url)
