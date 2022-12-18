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
            methods=["GET", "POST"],
            description="get the login page",
            response_class=HTMLResponse
        )

        self.router.add_api_route(
            "/register",
            self.register,
            methods=["GET", "POST"],
            description="get the register page",
            response_class=HTMLResponse
        )

        self.router.add_api_route(
            "/plans",
            self.plans,
            methods=["GET"],
            description="get the plans page",
            response_class=HTMLResponse
        )

        self.router.add_api_route(
            "/chart",
            self.chart_view,
            methods=["GET"],
            description="get the about page",
            response_class=HTMLResponse
        )

    async def index(self, req: Request) -> "_TemplateResponse" | RedirectResponse:
        return render_template("index.html", {"request": req})

    async def login(self, req: Request) -> "_TemplateResponse":
        return render_template("login.html", {"request": req})

    async def register(self, req: Request) -> "_TemplateResponse":
        return render_template("register.html", {"request": req})

    async def logout(self, req: Request) -> RedirectResponse:
        req.cookies.pop("user_id")
        return RedirectResponse(url="/login")

    async def manage_subscription(self, req: Request) -> "_TemplateResponse" | RedirectResponse:
        if req.user:
            return render_template("manage_subscription.html", {"request": req})
        return RedirectResponse("/login")

    async def plans(self, req: Request) -> "_TemplateResponse" | RedirectResponse:
        return render_template("plans.html", {"request": req})

    async def chart_view(self, req: Request) -> "_TemplateResponse" | RedirectResponse:
        if req.user:
            return render_template("chart.html", {"request": req})
        return RedirectResponse("/login")
