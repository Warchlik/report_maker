from datetime import timedelta
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import db
from app.utils.validator import (
    create_access_token,
    current_user,
    hash_value,
    validate_hashed_value,
)
from app.db.models import User


auth = APIRouter()


@auth.post("/register")
async def register(
    firstname: str = Body(default=None, alias="firstname"),
    lastname: str = Body(default=None, alias="lastname"),
    email: str = Body(default=None, alias="email"),
    password: str = Body(default=None, alias="password"),
    db: AsyncSession = Depends(db),
):
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Invalid password validation")

    password_hash = hash_value(password)
    user = User(
        firstname=firstname, lastname=lastname, email=email, password=password_hash
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {"status": 200}


@auth.post("/login")
async def login(
    form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(db)
):
    login_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login credentials"
    )
    if not form.password or not form.username:
        raise login_exception

    user: Optional[User] = await db.scalar(
        select(User).where(User.email == form.username)
    )

    if user is None:
        raise login_exception

    is_validated_password = validate_hashed_value(form.password, user.password)

    if not is_validated_password:
        raise login_exception

    token = create_access_token(
        {"user_id": user.id, "email": user.email}, timedelta(minutes=30)
    )

    return {"access_token": token, "token_type": "Bearer"}


class UserResposne:
    id: str
    email: str
    created_at: datetime


@auth.get("/me", response_model=UserResposne)
async def me(user: User | None = Depends(current_user)):
    return user
