from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Starting Server Booklib app....")
    yield
    print("Stopping Server Booklib app....")


version = "v1"

app = FastAPI(
    title="Book API",
    description="A simple API to manage books",
    version=version,
    lifespan=life_span
)

app.include_router(book_router, prefix=f"/api/{version}/books")
