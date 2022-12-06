from fastapi import Request
from asgiref.typing import ASGI3Application
from asgiref.typing import Scope, ASGIReceiveCallable, ASGISendCallable

from ..data import ApplicationDbContext
from ..dependencies import extract_claims_from_jwt


class AuthMiddleware:
    def __init__(self, app: ASGI3Application, database: ApplicationDbContext) -> None:
        self.app = app
        self.db = database

    async def __call__(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> None:
        request = Request(scope, receive)

        scope["user"] = None

        if (token := request.cookies.get("token")) is not None:
            if (claims := extract_claims_from_jwt(token)) is not None:
                user_id = claims["sub"]
                user = await self.db.users.get_by_id(user_id)
                scope["user"] = user

        return await self.app(scope, receive, send)
