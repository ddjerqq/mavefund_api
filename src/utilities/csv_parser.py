from __future__ import annotations

import csv
import os
from typing import Callable

from models.record import *
from utilities import Snowflake


# record = {
#     "company_name": str,
#     "symbol": str,
#     "symbol_date": str,
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
                "symbol_date",
                "gp_revenue_usd_mil",
                "gp_gross_margin",
                "gp_operating_income_usd_mil",
                "gp_operating_margin",
                "gp_net_income_usd_mil",
                "gp_earnings_per_share_usd",
                "gp_dividends_usd",
                "gp_payout_ratio",
                "gp_shares_mil",
                "gp_book_value_per_share_usd",
                "gp_operation_cash_flow_usd_mil",
                "gp_cap_spending_usd_mil",
                "gp_free_cash_flow_usd_mil",
                "gp_free_cash_flow_per_share_usd",
                "gp_working_capital_usd_mil",
            ]),

            # profitability margin
            lambda chunk: cls._parse_chunk(chunk, 1, 2, [
                "symbol_date",
                "pm_revenue",
                "pm_cogs",
                "pm_gross_margin",
                "pm_sg_and_a",
                "pm_r_and_d",
                "pm_other",
                "pm_operating_margin",
                "pm_net_interest_income_and_other",
                "pm_ebt_margin",
            ]),

            # profitability
            lambda chunk: cls._parse_chunk(chunk, 0, 1, [
                "symbol_date",
                "p_tax_rate_perc",
                "p_net_margin_perc",
                "p_asset_turnover",
                "p_return_on_assets",
                "p_financial_leverage",
                "p_return_on_equity",
                "p_return_on_invested_capital",
                "p_interest_coverage",
            ]),

            # growth
            lambda chunk: cls._parse_chunk(chunk, 1, 3, [
                "symbol_date",
                "g_revenue_perc_over_1_year_average",
                "g_revenue_perc_over_3_years_average",
                "g_revenue_perc_over_5_years_average",
                "g_revenue_perc_over_10_years_average",
                "g_operating_income_perc_over_1_year_average",
                "g_operating_income_perc_over_3_years_average",
                "g_operating_income_perc_over_5_years_average",
                "g_operating_income_perc_over_10_years_average",
                "g_net_income_perc_over_1_year_average",
                "g_net_income_perc_over_3_years_average",
                "g_net_income_perc_over_5_years_average",
                "g_net_income_perc_over_10_years_average",
                "g_eps_perc_over_1_year_average",
                "g_eps_perc_over_3_years_average",
                "g_eps_perc_over_5_years_average",
                "g_eps_perc_over_10_years_average",
            ],
                                          additional_cleanup=lambda lns: lns.__delitem__(slice(0, len(lns), 5))),

            # cash flow
            lambda chunk: cls._parse_chunk(chunk, 1, 2, [
                "symbol_date",
                "cf_operating_cash_flow_growth_perc_yoy",
                "cf_free_cash_flow_growth_perc_yoy",
                "cf_cap_ex_as_growth_perc_of_sales",
                "cf_free_cash_flow_over_sales_perc",
                "cf_free_cash_flow_over_net_income",
            ]),

            # financial health
            lambda chunk: cls._parse_chunk(chunk, 1, 2, [
                "symbol_date",
                "fh_cash_and_short_term_investments",
                "fh_accounts_receivable",
                "fh_inventory",
                "fh_other_current_assets",
                "fh_total_current_assets",
                "fh_net_pp_and_e",
                "fh_intangibles",
                "fh_other_long_term_assets",
                "fh_total_assets",
                "fh_accounts_payable",
                "fh_short_term_debt",
                "fh_taxes_payable",
                "fh_accrued_liabilities",
                "fh_other_short_term_liabilities",
                "fh_total_current_liabilities",
                "fh_long_term_debt",
                "fh_other_long_term_liabilities",
                "fh_total_liabilities",
                "fh_total_stockholders_equity",
                "fh_total_liabilities_and_equity",
            ]),

            # liquidity
            lambda chunk: cls._parse_chunk(chunk, 0, 1, [
                "symbol_date",
                "lqd_current_ratio",
                "lqd_quick_ratio",
                "lqd_financial_leverage",
                "lqd_debt_over_equity",
            ]),

            # efficiency
            lambda chunk: cls._parse_chunk(chunk, 1, 2, [
                "symbol_date",
                "efc_days_sales_outstanding",
                "efc_days_inventory",
                "efc_payable_period",
                "efc_cash_conversion_cycle",
                "efc_receivable_turnover",
                "efc_inventory_turnover",
                "efc_fixed_asset_turnover",
                "efc_asset_turnover",
            ])
        ]

        for idx, method in enumerate(methods):
            chunk_records.append(method(chunks[idx]))

        records = []
        for gp, pm, p, g, cf, fh, lqd, efc in zip(*chunk_records):
            record = Record(
                id=Snowflake(),
                company_name=name[:32],
                symbol=symbol,
                symbol_date=gp["symbol_date"],

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
