from fastapi import FastAPI
from sqlmodel import Session
import auth
import models
from db import create_db_and_tables, engine
import Routes
from db import get_session

app = FastAPI()

app.include_router(Routes.router)
app.include_router(auth.router)


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
    with Session(engine) as session:
        user = models.User(name='radek', lastname='czaja', email='asd@asd.com', password=auth.get_password_hash('asd'),
                           adres='wroclaw reja 10',
                           pesel='101203021030123')
        book = models.Books(author='J.K.Rowling', title="harry potter", genere='fantasy', desc='cos tam',
                            publisher='asd',
                            year=1990)
        session.add(user)
        session.add(book)
        session.commit()
        session.refresh(user)

    return
