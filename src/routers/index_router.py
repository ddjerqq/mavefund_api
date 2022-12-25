from __future__ import annotations

import os

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.templating import _TemplateResponse
from src.data import ApplicationDbContext
from src.utilities import render_template, tokenizer
from src.models.user import User


class IndexRouter:
    _recaptcha_public_key = os.getenv('RECAPTCHA_PUBLIC')

    def __init__(self, db: ApplicationDbContext):
        self.db = db

        self.router = APIRouter(prefix="")

        self.router.add_api_route(
            "/",
            self.index,
            methods=["GET", "POST"],
            description="get the index page",
            response_class=HTMLResponse
        )

        self.router.add_api_route(
            "/login",
            self.login,
            methods=["GET"],
            description="get the login page",
            response_class=HTMLResponse
        )

        self.router.add_api_route(
            "/verify-email/{token}",
            self.verify_email,
            methods=["GET"],
            description="Email verification",
            response_class=HTMLResponse
        )

        self.router.add_api_route(
            "/reset-password",
            self.reset_password,
            methods=["GET"],
            description="Reset Password",
            response_class=HTMLResponse
        )

        self.router.add_api_route(
            "/reset-password-verify/{token}",
            self.reset_password_verify,
            methods=["GET"],
            description="Reset Password verify",
            response_class=HTMLResponse
        )

        self.router.add_api_route(
            "/logout",
            self.logout,
            methods=["GET"],
            description="log the user out",
            response_class=HTMLResponse
        )

        self.router.add_api_route(
            "/premium",
            self.premium,
            methods=["GET"],
            description="get the plans page",
            response_class=HTMLResponse
        )

        self.router.add_api_route(
            "/dashboard",
            self.dashboard,
            methods=["GET"],
            description="get the about page",
            response_class=HTMLResponse
        )

    async def index(self,
                    req: Request) -> "_TemplateResponse" | RedirectResponse:
        return render_template(
            "index.html",
            {
                "request": req,
                "title": "home",
            }
        )

    async def login(self,
                    req: Request) -> "_TemplateResponse" | RedirectResponse:
        if req.user:
            return RedirectResponse(url="/")

        return render_template("login.html",
                               {"request": req,
                                'pub_key': self._recaptcha_public_key})

    async def logout(self, req: Request) -> RedirectResponse:
        req.cookies.pop("user_id")
        return RedirectResponse(url="/")

    async def premium(self,
                      req: Request) -> "_TemplateResponse" | RedirectResponse:
        return render_template(
            "premium.html",
            {
                "request": req,
                "title": "premium",
            }
        )

    async def dashboard(self, req: Request,
                        ticker: int = "AAPL") -> "_TemplateResponse" | RedirectResponse:
        return render_template(
            "dashboard.html",
            {
                "request": req,
                "title": "dashboard",
                "ticker": ticker,
            }
        )

    async def manage_subscription(self,
                                  req: Request) -> "_TemplateResponse" | RedirectResponse:
        if req.user:
            return render_template("manage_subscription.html",
                                   {"request": req})
        return RedirectResponse("/login")

    async def verify_email(self, token: str):
        user = await self._verify_token(token, mark_as_verified=True)
        if user is None:
            return HTMLResponse("the link is invalid or already used!")
        return RedirectResponse('/login?m=email-verified')

    async def reset_password(self, req: Request):
        if req.user:
            return RedirectResponse("/")
        return render_template("reset-password-email.html",
                               {"request": req})

    async def reset_password_verify(self, token: str, req: Request):
        if req.user:
            return RedirectResponse("/")
        user = await self._verify_token(token)
        if user is None:
            return HTMLResponse("The link is invalid!")
        return render_template("reset-password.html",
                               {"request": req, 'token': token})

    async def _verify_token(self, token: str,
                            mark_as_verified=False) -> User | None:

        email = tokenizer.decode_token(token)
        if not email:
            return
        user: User = await self.db.users.get_by_email(email)
        if not user:
            return
        if mark_as_verified:
            user.verified = True
            await self.db.users.update(user)
        return user
