import jwt
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
from passlib.context import CryptContext
from models import User
from db import get_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(tags=["Auth"])


class Token(BaseModel):
    access_token: str
    token_type: str


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, "123123", algorithms=["HS256"]
        )
        user: User = parse_obj_as(User, payload)
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    return user


def authenticate_user(session: Session, email: str, password: str):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


def create_access_token(user: User) -> Token:
    token = jwt.encode(
        user.dict(), "123123", algorithm="HS256"
    )
    token_type = "bearer"
    # return Token(access_token=token, token_type=token_type)
    return token


@router.post("/token")
async def generate_token(
        *,
        session: Session = Depends(get_session),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user)
    user_read = parse_obj_as(User, user)
    return {"user": user_read, "access_token": access_token}
