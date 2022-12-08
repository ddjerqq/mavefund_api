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
            methods=["GET"],
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
            "/register",
            self.register,
            methods=["GET"],
            description="get the register page",
            response_class=HTMLResponse
        )

        # self.router.add_api_route(
        #     "/dashboard",
        #     self.dashboard,
        #     methods=["GET"],
        #     description="get the dashboard page",
        #     response_class=HTMLResponse
        # )

    async def index(self, req: Request) -> "_TemplateResponse" | RedirectResponse:
        if req.user:
            return render_template("index.html", {"request": req})
        else:
            return RedirectResponse(url="/login")

    async def login(self, req: Request) -> "_TemplateResponse":
        return render_template("login.html", {"request": req})

    async def register(self, req: Request) -> "_TemplateResponse":
        return render_template("register.html", {"request": req})

    # async def dashboard(self, req: Request) -> "_TemplateResponse" | RedirectResponse:
    #     if req.cookies.get("token"):
    #         user = await self.auth.get_user_from_token(req.cookies.get("token"))
    #         return render_template("dashboard.html", {"request": req, "user": user})
    #     else:
    #         return RedirectResponse(url="/login")
