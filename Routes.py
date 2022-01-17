from fastapi import APIRouter
from fastapi import Depends
from sqlmodel import select
from sqlmodel import Session
import db
import models
from datetime import timedelta, datetime
import auth

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


@router.post('/users/me/books')
def boorow_book(
        *, session: Session = Depends(db.get_session), user: models.User = Depends(auth.get_current_user), title: str
):
    books = session.exec(select(models.Books).where(models.Books.title == title)).all()
    if not books:
        return "nie ma ksiazki"
    for book in books:
        result = session.exec(select(models.LendBooks).where(models.LendBooks.book_id == book.id)).first()
        if result is None:
            lendbooks = models.LendBooks(book_id=book.id, user_id=user.id, dateL=datetime.today(),
                                         dateR=datetime.today() + timedelta(14), dateAR=0)
            session.add(lendbooks)
            session.commit()
            return "ksiazke o nazwie " + title + " zostala wypozyczona"

    return "brak takiej ksiązki do wypożyczenia"


@router.delete('/users/{user_id}/books')
def return_book(
        *, session: Session = Depends(db.get_session), user_id: int, book_id: int
):
    user = session.get(models.User, user_id)
    if not user:
        return "nie ma uzytkownika"
    looking_for = session.exec(select(models.LendBooks).where(models.LendBooks.book_id == book_id,
                                                              models.LendBooks.user_id == user_id)).first()
    if not looking_for:
        return "nie ma ksiazki"
    session.delete(looking_for)
    session.commit()
    return "ksiazka oddana"


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


@router.get("/lendbooks/")
def get_book(
        *, session: Session = Depends(db.get_session)
):
    books = session.exec(select(models.LendBooks)).all()
    return books
