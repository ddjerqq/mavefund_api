from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from starlette.templating import _TemplateResponse

from utilities import render_template


class IndexRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/home")

        self.router.add_api_route(
            "/",
            self.index,
            methods=["GET"],
            description="get the index page",
            response_class=HTMLResponse
        )

    async def index(self, req: Request) -> "_TemplateResponse":
        return render_template("index.html", {"request": req})
