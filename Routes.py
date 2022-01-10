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
from datetime import date, timedelta, datetime

router = APIRouter()


@router.post("/books/")
def add_book(
        *, session: Session = Depends(db.get_session), book: models.BooksCreate
):
    db_book = models.Books.from_orm(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


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
    book = session.exec(select(models.Books).where(models.Books.title == title)).first()
    if not book:
        return "nie ma ksiazki"
    lendbooks = models.LendBooks(book_id=book.id, user_id=user.id, dateL=datetime.today(),
                                 dateR=datetime.today() + timedelta(14), dateAR=datetime.today())
    session.add(lendbooks)
    session.commit()
    session.refresh()
    return lendbooks


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
