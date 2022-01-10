from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from pydantic import parse_obj_as
from sqlmodel import select
from sqlmodel import Session
import db
import models
from datetime import date, timedelta

router = APIRouter()


@router.post("/books/")
def add_book(
        *, session: Session = Depends(db.get_session), book: models.BooksCreate
):
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.get("/books/")
def get_book(
        *, session: Session = Depends(db.get_session)
):
    books = session.exec(select(models.Books)).all()
    return books


@router.post('/users/{user_id}/books')
def boorow_book(
        *, session: Session = Depends(db.get_session), user_id: int, title: str
):
    user = session.get(models.User, user_id)
    if not user:
        return "nie ma uzytkownika"
    book = session.exec(select(models.Books).where(models.Books.title == title))
    if not book:
        return "nie ma ksiazki"
    lendbooks = models.LendBooks(book_id=book.id, user_id=user.id, dateL=date.today(),
                                 dateR=date.today() + timedelta(14), DateAR=0)


@router.post('/users/')
def add_user(
        *, session: Session = Depends(db.get_session), user: models.UserCreate
):
    db_user = models.User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/users/")
def get_users(
        *, session: Session = Depends(db.get_session)
):
    books = session.exec(select(models.User)).all()
    return books
