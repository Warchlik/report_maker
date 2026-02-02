from fastapi import Depends, HTTPException, Request
from datetime import datetime
from typing import Optional
from datetime import timedelta
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
import bcrypt

from app.db.models import User
from app.db.session import db

# TODO: change location for variables in to .env and .env.example
SECRET_KEY = "HpoPSC9U2JlHlX5kxTcWgKpeysVYAEjGmhk2IxcDa4q"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 30

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_value(value: str) -> str:
    hashed_value = bcrypt.hashpw(value.encode(), salt=bcrypt.gensalt(rounds=13))
    return hashed_value.decode()


def validate_hashed_value(value: str, value_hash: str) -> bool:
    return bcrypt.checkpw(password=value.encode(), hashed_password=value_hash.encode())


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def current_user(token: str = Depends(oauth2), db: AsyncSession = Depends(db)):
    exception = HTTPException(
        status_code=400,
        detail="Invalid auth data",
        headers={"Authentication": "Bearer"},
    )

    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        user_id: int | None = payload.get("user_id")
        if not user_id:
            raise exception
    except JWTError:
        raise exception

    usr: Optional[User] = (
        await db.scalars(select(User).where(User.id == user_id))
    ).one_or_none()

    if usr is None:
        raise exception

    return usr


async def current_user_cookie(request: Request, db: AsyncSession = Depends(db)):
    exception = HTTPException(
        status_code=400,
        detail="Invalid auth data",
        headers={"Authentication": "Bearer"},
    )

    cookie_token: Optional[str] = request.cookies.get("access_token")

    if not cookie_token:
        raise exception

    try:
        payload = jwt.decode(cookie_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[int] = payload.get("user_id")
        if user_id is None:
            raise exception

        user = await db.scalar(select(User).where(User.id == user_id))
    except JWTError:
        raise exception

    return user
