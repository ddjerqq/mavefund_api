import os

import uvicorn
from fastapi import Depends, FastAPI

from src.dependencies.database_connection import DbConnection
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService
from src.routers import users

ACCESS_TOKEN_EXPIRE_MINUTES = 60


app = FastAPI(
    dependencies=[
        Depends(DbConnection),
        Depends(UserRepository),
        Depends(UserService)
    ]
)
app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run(app)
