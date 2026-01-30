from datetime import timedelta
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm, http
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select, true
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST

from app.db.session import db
from app.utils.validator import (
    create_access_token,
    current_user_cookie,
    hash_value,
    validate_hashed_value,
)
from app.db.models import User


auth = APIRouter()


class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


@auth.post("/register")
async def register(
    user_data: RegisterRequest,
    db: AsyncSession = Depends(db),
):
    existing_user = await db.scalar(select(User).where(User.email == user_data.email))
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this credentials already exist"
        )

    password_hash = hash_value(user_data.password)
    user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password=password_hash,
    )

    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return {"status": 200}


@auth.post("/login")
async def login(
    response: Response,
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(db),
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

    response.set_cookie(
        key="access_token",
        value=f"{token}",
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=30 * 60,
    )

    return {"access_token": token, "token_type": "Bearer"}


@auth.get("/logout")
async def logout(
    response: Response, user: Optional[User] = Depends(current_user_cookie)
):
    if not user:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="not loged user")
    try:
        response.delete_cookie("access_token")
        return {"logout": True}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Somting wrong, try again"
        )


class UserResposne(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_atributes = True


@auth.get("/me", response_model=UserResposne)
async def me(user: User | None = Depends(current_user_cookie)):
    return user
