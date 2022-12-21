from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.templating import _TemplateResponse

from src.data import ApplicationDbContext
from src.utilities import render_template


class IndexRouter:
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

    async def index(self, req: Request) -> "_TemplateResponse" | RedirectResponse:
        return render_template(
            "index.html",
            {
                "request": req,
                "title": "home",
            }
        )

    async def login(self, req: Request) -> "_TemplateResponse" | RedirectResponse:
        if req.user:
            return RedirectResponse(url="/")

        return render_template("login.html", {"request": req})

    async def logout(self, req: Request) -> RedirectResponse:
        req.cookies.pop("user_id")
        return RedirectResponse(url="/")

    async def premium(self, req: Request) -> "_TemplateResponse" | RedirectResponse:
        return render_template(
            "premium.html",
            {
                "request": req,
                "title": "premium",
            }
        )

    async def dashboard(self, req: Request, ticker: int = "AAPL") -> "_TemplateResponse" | RedirectResponse:
        return render_template(
            "dashboard.html",
            {
                "request": req,
                "title": "dashboard",
                "ticker": ticker,
            }
        )


    async def manage_subscription(self, req: Request) -> "_TemplateResponse" | RedirectResponse:
        if req.user:
            return render_template("manage_subscription.html", {"request": req})
        return RedirectResponse("/login")

