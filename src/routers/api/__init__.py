from fastapi import APIRouter

from src.data import ApplicationDbContext
from src.routers.api.v1 import ApiV1Router



class ApiRouter:
    def __init__(self, db: ApplicationDbContext):
        self.db = db

        self.router = APIRouter(prefix="/api")

        self.v1 = ApiV1Router(db)

        self.router.include_router(self.v1.router)
