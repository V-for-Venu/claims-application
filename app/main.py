from contextlib import asynccontextmanager
from time import perf_counter

from api.routers import master_router as router
from core.exceptions import add_exception_handler
from database.session import create_db_tables
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from rich import panel, print
from scalar_fastapi import get_scalar_api_reference
from utils import add_log


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("...Server Started...", border_style="green"))
    await create_db_tables()
    yield
    print(panel.Panel("...Server Stopped...", border_style="red"))


app = FastAPI(lifespan=lifespan_handler)
app.include_router(router=router)

add_exception_handler(app)


@app.middleware("http")
async def custom_middleware(request: Request, call_next):

    start = perf_counter()
    response: Response = await call_next(request)
    end = perf_counter()

    time_taken = round(end - start, 2)

    print(response.headers)

    add_log(
        f"{request.method} {request.url} ({response.status_code}) {time_taken}ms \n"
    )

    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/scalar")
async def scalar_html():
    return get_scalar_api_reference(openapi_url=app.openapi_url)
