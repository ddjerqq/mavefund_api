from fastapi import APIRouter

from src.data import ApplicationDbContext
from src.routers.api.v1.auth_router import AuthRouter
from src.routers.api.v1.company_info_router import CompanyInfoRouter
from src.routers.api.v1.stripe_router import StripeRouter


class ApiV1Router:
    def __init__(self, db: ApplicationDbContext):
        self.db = db

        self.router = APIRouter(prefix="/v1")

        self.auth = AuthRouter(db)
        self.stripe = StripeRouter(db)
        self.company_info = CompanyInfoRouter(db)

        self.router.include_router(self.auth.router)
        self.router.include_router(self.stripe.router)
        self.router.include_router(self.company_info.router)
