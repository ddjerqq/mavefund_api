import logging

from fastapi import Request
from fastapi.logger import logger
from asgiref.typing import ASGI3Application
from asgiref.typing import Scope, ASGIReceiveCallable, ASGISendCallable

from src.data import ApplicationDbContext
from src.utilities import extract_claims_from_jwt

logger.handlers = logging.getLogger("uvicorn.error").handlers
logger.setLevel(logging.DEBUG)


class AuthMiddleware:
    def __init__(self, app: ASGI3Application, database: ApplicationDbContext) -> None:
        self.app = app
        self.db = database

    async def __call__(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> None:
        request = Request(scope, receive)

        scope["user"] = None

        if "api" in str(request.url):
            token = request.headers.get("authorization")
            if token is None:
                token = request.cookies.get("token")

            claims = extract_claims_from_jwt(token)
            if claims is not None:
                user_id = int(claims["sub"])
                user = await self.db.users.get_by_id(user_id)
                scope["user"] = user

        return await self.app(scope, receive, send)
