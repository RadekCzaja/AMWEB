from datetime import datetime
from typing import List
from typing import Optional
from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel


class UserBase(SQLModel):
    name: str
    lastname: str
    email: str
    password: str
    adres: str
    pesel: str


class UserCreate(UserBase):


    pass


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class BooksBase(SQLModel):
    author: str
    title: str
    genere: str
    desc: str
    publisher: str
    year: int


class BooksCreate(BooksBase):
    pass


class Books(BooksBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class LendBooks(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: Optional[int] = Field(default=None, foreign_key="books.id")
    dateL: datetime
    dateR: datetime
    dateAR: datetime
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Admin(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
