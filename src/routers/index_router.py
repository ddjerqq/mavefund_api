from __future__ import annotations

import json
import os

from fastapi import APIRouter, Request
# from fastapi import Depends
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.templating import _TemplateResponse

from src.data import ApplicationDbContext
from src.utilities import render_template, tokenizer
from src.models import User
from src.models.dto import Symbol, MinimalRecord
# from src.dependencies.auth import subscriber_only


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
            "/premium",
            self.premium,
            methods=["GET"],
            description="get the plans page",
            response_class=HTMLResponse
        )

        self.router.add_api_route(
            "/dashboard/{ticker:str}",
            self.dashboard,
            methods=["GET"],
            description="get the dashboard page",
            response_class=HTMLResponse,
            # dependencies=[Depends(subscriber_only)],
        )

        self.router.add_api_route(
            "/table/{ticker:str}",
            self.table,
            methods=["GET"],
            description="get the table view",
            response_class=HTMLResponse,
            # dependencies=[Depends(subscriber_only)],
        )

    async def index(self, req: Request, q: str | None = None) -> "_TemplateResponse" | RedirectResponse:
        tickers = None

        if q is not None:
            tickers = await self.db.records.get_all_by_company_name(q)

        return render_template(
            "index.html",
            {
                "request": req,
                "title": "home",
                "tickers": tickers
            }
        )

    async def login(self, req: Request) -> "_TemplateResponse" | RedirectResponse:
        if req.user:
            return RedirectResponse(url="/")

        return render_template("login.html",
                               {"request": req,
                                'pub_key': self._recaptcha_public_key})

    async def premium(self, req: Request) -> "_TemplateResponse" | RedirectResponse:
        return render_template(
            "premium.html",
            {
                "request": req,
                "title": "premium",
            }
        )

    async def dashboard(self, req: Request, ticker: str) -> "_TemplateResponse" | RedirectResponse:
        if req.user.rank < 0:
            return RedirectResponse("/premium")

        records = await self.db.records.get_all_by_symbol(ticker)
        # if records is None
        minimal_records = list(map(MinimalRecord.from_record, records))
        s = Symbol.from_minimal_records(minimal_records)

        return render_template(
            "dashboard.html",
            {
                "request": req,
                "title": f"chart {ticker.upper()}",
                "ticker": ticker,
                "company_name": s.cnm,
                "data_provider": json.dumps(s.data_provider, indent=4),
            }
        )

    async def table(self, req: Request, ticker: str) -> "_TemplateResponse" | RedirectResponse:
        if req.user.rank < 0:
            return RedirectResponse("/premium")

        records = await self.db.records.get_all_by_symbol(ticker)
        minimal_records = list(map(MinimalRecord.from_record, records))
        symbol = Symbol.from_minimal_records(minimal_records)

        dates = symbol.dt
        table = {
            "Revenue (USD mil)": symbol.gp_rum,
            "Gross Margin %": symbol.gp_gm,
            "Operating Income (USD MIL)": symbol.gp_oim,
            "Operating Margin %": symbol.gp_om,
            "Net Income (USD MIL)": symbol.gp_nim,
            "Earnings Per Share (USD)": symbol.gp_eps,
            "Dividends (USD)": symbol.gp_d,
            "Payout Ratio %": symbol.gp_pr,
            "Shares (Mil)": symbol.gp_sm,
            "Book Value Per Share (USD)": symbol.gp_bvps,
            "Operating Cash Flow (USD": symbol.gp_ocf,
            "Cap Spending (USD MIL)": symbol.gp_sm,
            "Free Cash Flow (USD MIL)": symbol.gp_fcf,
            "Free Cash Flow Per Share (USD)": symbol.gp_fcfps,
            "Working Capital (USD MIL)": symbol.gp_wc,
        }

        return render_template(
            "table.html",
            {
                "request": req,
                "title": f"table {ticker.upper()}",
                "ticker": ticker,
                "dates": dates,
                "table": table
            }
        )

    async def manage_subscription(self, req: Request) -> "_TemplateResponse" | RedirectResponse:
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

    async def _verify_token(self, token: str, mark_as_verified=False) -> User | None:

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
