from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi import HTTPException

from src.dependencies.auth import get_current_user
from src.models.user import User
from src.services.user_service import UserService

router = APIRouter()


@router.get("/users/me", tags=["users"], response_model=User)
async def read_users_me(
        current_user: User = Depends(get_current_user)
) -> User:
    if current_user:
        return current_user
    else:
        raise HTTPException(status_code=401, detail="unauthorized")


@router.get("/users/all", tags=["users"], response_model=list[User])
async def get_all_users(
        users: UserService = Depends()
) -> list[User]:
    return await users.get_all()


@router.get("/users/{id}", tags=["users"], response_model=User)
async def get_by_id(
        id: int,
        users: UserService = Depends()
) -> User | None:
    if (user := await users.get_by_id(id)) is None:
        raise HTTPException(
            status_code=404,
            detail=f"user with id: {id} could not be found"
        )

    return user


@router.put("/users/update", tags=["user"])
async def update(
        user: User,
        users: UserService = Depends()
) -> None:
    await users.update(user)


@router.delete("/users/delete", tags=["user"])
async def delete(
        user: User,
        users: UserService = Depends()
) -> None:
    await users.delete(user)
