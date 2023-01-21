from __future__ import annotations

import io
from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import StreamingResponse

from src.data import ApplicationDbContext
from src.models import CompanyInfo
from src.dependencies.auth import subscriber_only


class CompanyInfoRouter:
    def __init__(self, db: ApplicationDbContext):
        self.db = db

        self.router = APIRouter(
            prefix="/info",
        )

        self.router.add_api_route(
            "/download",
            self.download_csv,
            methods=["GET"],
            dependencies=[Depends(subscriber_only)],
        )

        self.router.add_api_route(
            "/search",
            self.get_all_companies_by_name_or_ticker,
            methods=["GET"],
        )

        self.router.add_api_route(
            "/get",
            self.get_by_ticker,
            methods=["GET"],
            response_model=CompanyInfo,
            dependencies=[Depends(subscriber_only)],
        )

    async def download_csv(self, q: str):
        csv = await self.db.companies.get_csv_by_ticker(q)

        if csv is None:
            raise HTTPException(status_code=404, detail=f"no records found for {q}.")

        csv_data = io.BytesIO()
        csv_data.write(csv.encode("utf-8"))
        csv_data.seek(0)

        return StreamingResponse(
            csv_data,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={q}_mavefund.csv"
            },
            status_code=200
        )

    async def get_all_companies_by_name_or_ticker(self, q: str) -> dict[str, str]:
        return await self.db.companies.get_all_companies_by_name_or_ticker(q)

    async def get_by_ticker(self, q: str) -> CompanyInfo | None:
        info = await self.db.companies.get_by_ticker(q)

        if not info:
            raise HTTPException(status_code=404, detail=f"no records found for {q}.")

        return info
