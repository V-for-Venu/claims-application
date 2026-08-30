from contextlib import asynccontextmanager

from api.router import router
from database.session import create_db_tables
from fastapi import FastAPI
from rich import panel, print
from scalar_fastapi import get_scalar_api_reference


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("...Server Started...", border_style="green"))
    await create_db_tables()
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
