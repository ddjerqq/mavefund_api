from fastapi import APIRouter

from src.data import ApplicationDbContext
from src.routers.api.v1.auth_router import AuthRouter
from src.routers.api.v1.user_router import UserRouter
from src.routers.api.v1.record_router import RecordRouter
from src.routers.api.v1.stripe_router import StripeRouter, StripeWebhookRouter


class ApiV1Router:
    def __init__(self, db: ApplicationDbContext):
        self.db = db

        self.router = APIRouter(prefix="/v1")

        self.auth = AuthRouter(db)
        self.users = UserRouter(db)
        self.stripe = StripeRouter(db)
        self.stripe_webhook = StripeWebhookRouter(db)
        self.records = RecordRouter(db)

        self.router.include_router(self.auth.router)
        self.router.include_router(self.users.router)
        self.router.include_router(self.stripe.router)
        self.router.include_router(self.stripe_webhook.router)
        self.router.include_router(self.records.router)
