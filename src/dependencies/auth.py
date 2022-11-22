from __future__ import annotations

import os
from datetime import datetime

from jose import JWTError, jwt
from datetime import timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.models.user import User
from src.services.user_service import UserService
from src.utilities.password_hasher import Password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_user(
        username: str,
        password: str,
        users: UserService = Depends(),
) -> User | None:
    all_users = await users.get_all()

    user = next((
        user
        for user in all_users
        if user.username == username
        and Password.compare(user.password_hash, password)
    ), None)

    return user


def generate_token(user: User, expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta

    claims = {
        "sub": user.id,
        "exp": expire,
    }

    token = jwt.encode(claims, key=os.getenv("JWT_SECRET"))
    return token


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        users: UserService = Depends(),
) -> User | None:

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"))
        user_id: int = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = await users.get_by_id(user_id)

    if user is None:
        raise credentials_exception

    return user
