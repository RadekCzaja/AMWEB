from fastapi import FastAPI
import models
from db import create_db_and_tables
import Routes
app = FastAPI()


app.include_router(Routes.router)

@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.delete("/book")
async def delete_book():
    return {"hello"}

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()
