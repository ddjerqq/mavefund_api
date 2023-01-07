from __future__ import annotations

import json
import os
import re
import io
import asyncio as aio

from fastapi import APIRouter, Request
# from fastapi import Depends
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse, StreamingResponse
from starlette.templating import _TemplateResponse

from src.data import ApplicationDbContext
from src.utilities import render_template, tokenizer, get_stock_price
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

        self.router.add_api_route(
            "/download/{ticker:str}",
            self.download,
            methods=["GET"],
            description="download csv for ticker",
            response_class=StreamingResponse,
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
        if req.user is None or req.user.rank < 0:
            return RedirectResponse("/premium")

        ticker_regex = re.compile(r"^[A-Z]{1,5}$")

        if not re.match(ticker_regex, ticker) or not ticker:
            return RedirectResponse("/")

        records = await self.db.records.get_all_by_symbol(ticker)
        # if records is None
        minimal_records = list(map(MinimalRecord.from_record, records))
        s = Symbol.from_minimal_records(minimal_records)
        stock_prices = await get_stock_price(ticker)

        # im sorry for this but this projects budget is too
        # low for me to put any more effort into it
        data_provider = s.data_provider
        for record, price in zip(data_provider, stock_prices.values()):
            # this could potentially be inaccurate, and sometime in the future it
            # will go out of sync, wrong data will be displayed and chaos everywhere
            record["column-0"] = price

        return render_template(
            "dashboard.html",
            {
                "request": req,
                "title": f"chart {ticker.upper()}",
                "ticker": ticker,
                "company_name": s.cnm,
                "data_provider": json.dumps(data_provider, indent=4),
            }
        )

    async def table(self, req: Request, ticker: str) -> "_TemplateResponse" | RedirectResponse:
        if req.user is None or req.user.rank < 0:
            return RedirectResponse("/premium")

        ticker_regex = re.compile(r"^[A-Z]{1,5}$")

        if not re.match(ticker_regex, ticker) or not ticker:
            return RedirectResponse("/")

        records = await self.db.records.get_all_by_symbol(ticker)
        minimal_records = list(map(MinimalRecord.from_record, records))
        symbol = Symbol.from_minimal_records(minimal_records)

        dates = symbol.dt
        table = {
            "Growth Profit": "",
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

            "Profit Margin": "",
            "Revenue": symbol.pm_r,
            "COGS": symbol.pm_cogs,
            "Gross Margin": symbol.pm_gm,
            "SG&A": symbol.pm_sga,
            "R&D": symbol.pm_rd,
            "Other": symbol.pm_o,
            "Operating Margin": symbol.pm_om,
            "Net Int Inc & Other": symbol.pm_nii,
            "EBT Margin": symbol.pm_ebm,

            "Profitability": "",
            "Tax Rate %": symbol.p_trp,
            "Net Margin %": symbol.p_nm,
            "Asset Turnover (Average)": symbol.p_at,
            "Return on Assets %": symbol.p_roa,
            "Financial Leverage (Average)": symbol.p_fl,
            "Return on Equity %": symbol.p_roe,
            "Return on Invested Capital %": symbol.p_roic,
            "Interest Coverage": symbol.p_ic,

            "Growth": "",
            "Revenue % Year over Year": symbol.g_rp_1,
            "Revenue % 3-Year Average": symbol.g_rp_3,
            "Revenue % 5-Year Average": symbol.g_rp_5,
            "Revenue % 10-Year Average": symbol.g_rp_10,

            "Operating Income % Year over Year": symbol.g_opi_1,
            "Operating Income % 3-Year Average": symbol.g_opi_3,
            "Operating Income % 5-Year Average": symbol.g_opi_5,
            "Operating Income % 10-Year Average": symbol.g_opi_10,

            "Net Income % Year over Year": symbol.g_ni_1,
            "Net Income % 3-Year Average": symbol.g_ni_3,
            "Net Income % 5-Year Average": symbol.g_ni_5,
            "Net Income % 10-Year Average": symbol.g_ni_10,

            "EPS % Year over Year": symbol.g_eps_1,
            "EPS % 3-Year Average": symbol.g_eps_3,
            "EPS % 5-Year Average": symbol.g_eps_5,
            "EPS % 10-Year Average": symbol.g_eps_10,

            "Cash Flow": "",
            "Operating Cash Flow Growth % YOY": symbol.cf_ocf,
            "Free Cash Flow Growth % YOY": symbol.cf_fcfgp,
            "Cap Ex as a % of Sales": symbol.cf_ceag,
            "Free Cash Flow/Sales %": symbol.cf_fcfos,
            "Free Cash Flow/Net Income": symbol.cf_fcfoni,

            "Financial Health": "",
            "Cash & Short-Term Investments": symbol.fh_casti,
            "Accounts Receivable": symbol.fh_ar,
            "Inventory": symbol.fh_inv,
            "Other Current Assets": symbol.fh_oca,
            "Total Current Assets": symbol.fh_tca,
            "Net PP&E": symbol.fh_nppe,
            "Intangibles": symbol.fh_int,
            "Other Long-Term Assets": symbol.fh_olta,
            "Total Assets": symbol.fh_ta,
            "Accounts Payable": symbol.fh_ap,
            "Short-Term Debt": symbol.fh_std,
            "Taxes Payable": symbol.fh_tp,
            "Accrued Liabilities": symbol.fh_al,
            "Other Short-Term Liabilities": symbol.fh_ostl,
            "Total Current Liabilities": symbol.fh_tcl,
            "Long-Term Debt": symbol.fh_ltd,
            "Other Long-Term Liabilities": symbol.fh_oltl,
            "Total Liabilities": symbol.fh_tl,
            "Total Stockholders' Equity": symbol.fh_tse,
            "Total Liabilities & Equity": symbol.fh_tle,

            "Liquidity/Financial Health": "",
            "Current Ratio": symbol.lqd_cr,
            "Quick Ratio": symbol.lqd_qr,
            "Financial Leverage": symbol.lqd_fl,
            "Debt/Equity": symbol.lqd_doe,

            "Efficiency Ratios": "",
            "Days Sales Outstanding": symbol.efc_dso,
            "Days Inventory": symbol.efc_di,
            "Payables Period":  symbol.efc_pp,
            "Cash Conversion Cycle": symbol.efc_ccc,
            "Receivables Turnover": symbol.efc_rt,
            "Inventory Turnover": symbol.efc_it,
            "Fixed Assets Turnover": symbol.efc_fat,
            "Asset Turnover": symbol.efc_at,
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

    async def download(self, req: Request, ticker: str) -> StreamingResponse | RedirectResponse:
        """Download the table as a CSV file."""
        if req.user is None or req.user.rank < 0:
            return RedirectResponse("/premium")

        ticker_regex = re.compile(r"^[A-Z]{1,5}$")

        if not re.match(ticker_regex, ticker) or not ticker:
            return RedirectResponse("/")

        csv_content = await self.db.records.get_csv_by_symbol(ticker)
        if csv_content is None:
            return RedirectResponse("/not_found")

        csv_data = io.BytesIO()
        csv_data.write(csv_content.encode("utf-8"))
        csv_data.seek(0)

        return StreamingResponse(
            csv_data,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={ticker}_mavefund.csv"
            },
            status_code=200,
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
