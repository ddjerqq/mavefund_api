from __future__ import annotations

import csv
import os
from typing import Callable

from src.models.record import *
from src.utilities import Snowflake


# record = {
#     "company_name": str,
#     "symbol": str,
#     "date": str,
#
#     "growth_profitability_and_financial_ratios": {
#         "revenue_usd_mil": int,
#         "gross_margin": float,
#         "operating_income_usd_mil": int,
#         "operating_margin": float,
#         "net_income_usd_mil": int,
#         "earnings_per_share_usd": float,
#         "dividends_usd": float,
#         "payout_ratio": float,
#         "shares_mil": int,
#         "book_value_per_share_usd": float,
#         "operation_cash_flow_usd_mil": int,
#         "cap_spending_usd_mil": int,
#         "free_cash_flow_usd_mil": int,
#         "free_cash_flow_per_share_usd": float,
#         "working_capital_usd_mil": float,
#     },
#     "profitability_margin_perc_of_sales": {
#         "revenue": float,
#         "cogs": float,
#         "gross_margin": float,
#         "sg_and_a": float,
#         "r_and_d": float,
#         "other": float,
#         "operating_margin": float,
#         "net_interest_income_and_other": float,
#         "ebt_margin": float,
#     },
#     "profitability": {
#         "tax_rate_perc": float,
#         "net_margin_perc": float,
#         "asset_turnover": float,
#         "return_on_assets": float,
#         "financial_leverage": float,
#         "return_on_equity": float,
#         "return_on_invested_capital": float,
#         "interest_coverage": float,
#     },
#     "growth": {
#         "revenue_perc_over_1_year_average": float,
#         "revenue_perc_over_3_years_average": float,
#         "revenue_perc_over_5_years_average": float,
#         "revenue_perc_over_10_years_average": float,
#
#         "operating_income_perc_over_1_year_average": float,
#         "operating_income_perc_over_3_years_average": float,
#         "operating_income_perc_over_5_years_average": float,
#         "operating_income_perc_over_10_years_average": float,
#
#         "net_income_perc_over_1_year_average": float,
#         "net_income_perc_over_3_years_average": float,
#         "net_income_perc_over_5_years_average": float,
#         "net_income_perc_over_10_years_average": float,
#
#         "eps_perc_over_1_year_average": float,
#         "eps_perc_over_3_years_average": float,
#         "eps_perc_over_5_years_average": float,
#         "eps_perc_over_10_years_average": float,
#     },
#     "cash_flow_ratios": {
#         "operating_cash_flow_growth_and_yoy": float,
#         "free_cash_flow_growth_and_yoy": float,
#         "cap_ex_as_a_perc_of_sales": float,
#         "free_cash_flow_as_a_perc_of_sales": float,
#         "free_cash_flow_as_a_perc_of_net_income": float,
#     },
#     "financial_health_balance_sheet_items": {
#         "cash_and_short_term_investments": float,
#         "accounts_receivable": float,
#         "inventory": float,
#         "other_current_assets": float,
#         "total_current_assets": float,
#         "net_pp_and_e": float,
#         "intangibles": float,
#         "other_long_term_assets": float,
#         "total_assets": float,
#         "accounts_payable": float,
#         "short_term_debt": float,
#         "taxes_payable": float,
#         "accrued_liabilities": float,
#         "other_short_term_liabilities": float,
#         "total_current_liabilities": float,
#         "long_term_debt": float,
#         "other_long_term_liabilities": float,
#         "total_liabilities": float,
#         "total_stockholders_equity": float,
#         "total_liabilities_and_equity": float,
#     },
#     "financial_health": {
#         "current_ratio": float,
#         "quick_ratio": float,
#         "financial_leverage": float,
#         "debt_to_equity": float,
#     }
# }

__all__ = {
    "CsvDataParser"
}

class CsvDataParser:
    @classmethod
    def _parse_chunk(
            cls,
            chunk: list[str],
            date_line_idx: int,
            data_start_idx: int,
            keys: list[str],
            additional_cleanup: Callable[[list[list[str]]], None] | None = None,
    ) -> list[dict]:
        lines: list[list[str]] = list(csv.reader(chunk))

        dates = lines[date_line_idx].copy()
        dates[0] = "dates"
        lines = lines[data_start_idx:]

        if additional_cleanup:
            lines.insert(0, dates)
            additional_cleanup(lines)

        lines.insert(0, dates)

        for li, line in enumerate(lines):
            for pi, part in enumerate(line):
                if "," in part:
                    line[pi] = int(part.replace(",", ""))  # type: ignore

                if part == "":
                    line[pi] = None  # type: ignore

                try:
                    line[pi] = float(part)  # type: ignore
                except ValueError:
                    continue

        columns = list(map(list, zip(*lines)))

        return [
            {
                key: row[idx]
                for idx, key in enumerate(keys)
            }
            for row in columns
        ][1:]

    @classmethod
    def parse(cls, path: str) -> list[Record]:
        name = None

        with open(path, "r") as f:
            chunks = []
            lines = []
            for _line in f.readlines():
                if not name and "Ratios for " in _line:
                    name = _line.split("Ratios for ")[1][:-5].lower().replace(" ", "_")

                if _line == "\n":
                    chunks.append(lines)
                    lines = []

                else:
                    lines.append(_line.strip())

            chunks.append(lines)
            del lines

        symbol = os.path.basename(path).split(".")[0].split()[0]

        # parsing a chunk returns a list of record-dicts
        # for that chunk
        chunk_records = []

        methods = [
            # growth profitability
            lambda chunk: cls._parse_chunk(chunk, 2, 3, [
                "date",
                "revenue_usd_mil",
                "gross_margin",
                "operating_income_usd_mil",
                "operating_margin",
                "net_income_usd_mil",
                "earnings_per_share_usd",
                "dividends_usd",
                "payout_ratio",
                "shares_mil",
                "book_value_per_share_usd",
                "operation_cash_flow_usd_mil",
                "cap_spending_usd_mil",
                "free_cash_flow_usd_mil",
                "free_cash_flow_per_share_usd",
                "working_capital_usd_mil",
            ]),

            # profitability margin
            lambda chunk: cls._parse_chunk(chunk, 1, 2, [
                "date",
                "revenue",
                "cogs",
                "gross_margin",
                "sg_and_a",
                "r_and_d",
                "other",
                "operating_margin",
                "net_interest_income_and_other",
                "ebt_margin",
            ]),

            # profitability
            lambda chunk: cls._parse_chunk(chunk, 0, 1, [
                "date",
                "tax_rate_perc",
                "net_margin_perc",
                "asset_turnover",
                "return_on_assets",
                "financial_leverage",
                "return_on_equity",
                "return_on_invested_capital",
                "interest_coverage",
            ]),

            # growth
            lambda chunk: cls._parse_chunk(chunk, 1, 3, [
                "date",
                "revenue_perc_over_1_year_average",
                "revenue_perc_over_3_years_average",
                "revenue_perc_over_5_years_average",
                "revenue_perc_over_10_years_average",
                "operating_income_perc_over_1_year_average",
                "operating_income_perc_over_3_years_average",
                "operating_income_perc_over_5_years_average",
                "operating_income_perc_over_10_years_average",
                "net_income_perc_over_1_year_average",
                "net_income_perc_over_3_years_average",
                "net_income_perc_over_5_years_average",
                "net_income_perc_over_10_years_average",
                "eps_perc_over_1_year_average",
                "eps_perc_over_3_years_average",
                "eps_perc_over_5_years_average",
                "eps_perc_over_10_years_average",
            ],
                                          additional_cleanup=lambda lns: lns.__delitem__(slice(0, len(lns), 5))),

            # cash flow
            lambda chunk: cls._parse_chunk(chunk, 1, 2, [
                "date",
                "operating_cash_flow_growth_perc_yoy",
                "free_cash_flow_growth_perc_yoy",
                "cap_ex_as_growth_perc_of_sales",
                "free_cash_flow_over_sales_perc",
                "free_cash_flow_over_net_income",
            ]),

            # financial health
            lambda chunk: cls._parse_chunk(chunk, 1, 2, [
                "date",
                "cash_and_short_term_investments",
                "accounts_receivable",
                "inventory",
                "other_current_assets",
                "total_current_assets",
                "net_pp_and_e",
                "intangibles",
                "other_long_term_assets",
                "total_assets",
                "accounts_payable",
                "short_term_debt",
                "taxes_payable",
                "accrued_liabilities",
                "other_short_term_liabilities",
                "total_current_liabilities",
                "long_term_debt",
                "other_long_term_liabilities",
                "total_liabilities",
                "total_stockholders_equity",
                "total_liabilities_and_equity",
            ]),

            # liquidity
            lambda chunk: cls._parse_chunk(chunk, 0, 1, [
                "date",
                "current_ratio",
                "quick_ratio",
                "financial_leverage",
                "debt_over_equity",
            ]),

            # efficiency
            lambda chunk: cls._parse_chunk(chunk, 1, 2, [
                "date",
                "days_sales_outstanding",
                "days_inventory",
                "payable_period",
                "cash_conversion_cycle",
                "receivable_turnover",
                "inventory_turnover",
                "fixed_asset_turnover",
                "asset_turnover",
            ])
        ]

        for idx, method in enumerate(methods):
            chunk_records.append(method(chunks[idx]))

        records = []
        for gp, pm, p, g, cf, fh, lqd, efc in zip(*chunk_records):
            record = Record(
                id=Snowflake(),
                company_name=name,
                symbol=symbol,
                date=gp["date"],

                growth_profitability=GrowthProfitability(**gp),
                profitability_margin=ProfitabilityMargin(**pm),
                profitability=Profitability(**p),
                growth=Growth(**g),
                cash_flow=CashFlow(**cf),
                financial_health=FinancialHealth(**fh),
                liquidity=Liquidity(**lqd),
                efficiency=Efficiency(**efc),
            )
            records.append(record)
        return records
