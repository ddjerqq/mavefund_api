from __future__ import annotations

import csv
import os
from typing import Callable

import aiofiles

from src.models import *

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
    async def read_csv(cls, path: str) -> str:
        async with aiofiles.open(path, "r", encoding="utf-8", errors="ignore") as f:
            return await f.read()

    @classmethod
    async def parse(
            cls,
            path: str | None = None,
            db_data: tuple[str, str, str] | None = None,
    ) -> CompanyInfo:
        name = None

        if db_data is not None:
            ticker, name, content = db_data
            content = content.strip("﻿")
            line_separator = ""
        else:
            content = await cls.read_csv(path)
            ticker = os.path.basename(path).removesuffix(".csv").split(" ")[0]
            line_separator = "\n"

        chunks = []
        lines = []
        for _line in content.splitlines():
            if name is None and "Ratios for " in _line:
                name = _line.split("Ratios for ")[1][:-1].lower()

            if _line == line_separator:
                chunks.append(lines)
                lines = []

            else:
                lines.append(_line.strip())

        chunks.append(lines)
        del lines

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

        info = CompanyInfo(company_name=name, ticker=ticker)

        # iterate this and append shit here everytime instead of creating vars.

        for gp, pm, p, g, cf, fh, lqd, efc in zip(*chunk_records):
            date = gp["symbol_date"]
            gp = GrowthProfitability(**gp)
            pm = ProfitabilityMargin(**pm)
            p = Profitability(**p)
            g = Growth(**g)
            cf = CashFlow(**cf)
            fh = FinancialHealth(**fh)
            lqd = Liquidity(**lqd)
            efc = Efficiency(**efc)

            info.dates.append(date)

            info.gp_revenue_usd_mil.append(gp.gp_revenue_usd_mil)
            info.gp_gross_margin.append(gp.gp_gross_margin)
            info.gp_operating_income_usd_mil.append(gp.gp_operating_income_usd_mil)
            info.gp_operating_margin.append(gp.gp_operating_margin)
            info.gp_net_income_usd_mil.append(gp.gp_net_income_usd_mil)
            info.gp_earnings_per_share_usd.append(gp.gp_earnings_per_share_usd)
            info.gp_dividends_usd.append(gp.gp_dividends_usd)
            info.gp_payout_ratio.append(gp.gp_payout_ratio)
            info.gp_shares_mil.append(gp.gp_shares_mil)
            info.gp_book_value_per_share_usd.append(gp.gp_book_value_per_share_usd)
            info.gp_operation_cash_flow_usd_mil.append(gp.gp_operation_cash_flow_usd_mil)
            info.gp_cap_spending_usd_mil.append(gp.gp_cap_spending_usd_mil)
            info.gp_free_cash_flow_usd_mil.append(gp.gp_free_cash_flow_usd_mil)
            info.gp_free_cash_flow_per_share_usd.append(gp.gp_free_cash_flow_per_share_usd)
            info.gp_working_capital_usd_mil.append(gp.gp_working_capital_usd_mil)

            info.pm_revenue.append(pm.pm_revenue)
            info.pm_cogs.append(pm.pm_cogs)
            info.pm_gross_margin.append(pm.pm_gross_margin)
            info.pm_sg_and_a.append(pm.pm_sg_and_a)
            info.pm_r_and_d.append(pm.pm_r_and_d)
            info.pm_other.append(pm.pm_other)
            info.pm_operating_margin.append(pm.pm_operating_margin)
            info.pm_net_interest_income_and_other.append(pm.pm_net_interest_income_and_other)
            info.pm_ebt_margin.append(pm.pm_ebt_margin)

            info.p_tax_rate_perc.append(p.p_tax_rate_perc)
            info.p_net_margin_perc.append(p.p_net_margin_perc)
            info.p_asset_turnover.append(p.p_asset_turnover)
            info.p_return_on_assets.append(p.p_return_on_assets)
            info.p_financial_leverage.append(p.p_financial_leverage)
            info.p_return_on_equity.append(p.p_return_on_equity)
            info.p_return_on_invested_capital.append(p.p_return_on_invested_capital)
            info.p_interest_coverage.append(p.p_interest_coverage)

            info.g_revenue_perc_over_1_year_average.append(g.g_revenue_perc_over_1_year_average)
            info.g_revenue_perc_over_3_years_average.append(g.g_revenue_perc_over_3_years_average)
            info.g_revenue_perc_over_5_years_average.append(g.g_revenue_perc_over_5_years_average)
            info.g_revenue_perc_over_10_years_average.append(g.g_revenue_perc_over_10_years_average)

            info.g_operating_income_perc_over_1_year_average.append(g.g_operating_income_perc_over_1_year_average)
            info.g_operating_income_perc_over_3_years_average.append(g.g_operating_income_perc_over_3_years_average)
            info.g_operating_income_perc_over_5_years_average.append(g.g_operating_income_perc_over_5_years_average)
            info.g_operating_income_perc_over_10_years_average.append(g.g_operating_income_perc_over_10_years_average)

            info.g_net_income_perc_over_1_year_average.append(g.g_net_income_perc_over_1_year_average)
            info.g_net_income_perc_over_3_years_average.append(g.g_net_income_perc_over_3_years_average)
            info.g_net_income_perc_over_5_years_average.append(g.g_net_income_perc_over_5_years_average)
            info.g_net_income_perc_over_10_years_average.append(g.g_net_income_perc_over_10_years_average)

            info.g_eps_perc_over_1_year_average.append(g.g_eps_perc_over_1_year_average)
            info.g_eps_perc_over_3_years_average.append(g.g_eps_perc_over_3_years_average)
            info.g_eps_perc_over_5_years_average.append(g.g_eps_perc_over_5_years_average)
            info.g_eps_perc_over_10_years_average.append(g.g_eps_perc_over_10_years_average)

            info.cf_operating_cash_flow_growth_perc_yoy.append(cf.cf_operating_cash_flow_growth_perc_yoy)
            info.cf_free_cash_flow_growth_perc_yoy.append(cf.cf_free_cash_flow_growth_perc_yoy)
            info.cf_cap_ex_as_growth_perc_of_sales.append(cf.cf_cap_ex_as_growth_perc_of_sales)
            info.cf_free_cash_flow_over_sales_perc.append(cf.cf_free_cash_flow_over_sales_perc)
            info.cf_free_cash_flow_over_net_income.append(cf.cf_free_cash_flow_over_net_income)

            info.fh_cash_and_short_term_investments.append(fh.fh_cash_and_short_term_investments)
            info.fh_accounts_receivable.append(fh.fh_accounts_receivable)
            info.fh_inventory.append(fh.fh_inventory)
            info.fh_other_current_assets.append(fh.fh_other_current_assets)
            info.fh_total_current_assets.append(fh.fh_total_current_assets)
            info.fh_net_pp_and_e.append(fh.fh_net_pp_and_e)
            info.fh_intangibles.append(fh.fh_intangibles)
            info.fh_other_long_term_assets.append(fh.fh_other_long_term_assets)
            info.fh_total_assets.append(fh.fh_total_assets)
            info.fh_accounts_payable.append(fh.fh_accounts_payable)
            info.fh_short_term_debt.append(fh.fh_short_term_debt)
            info.fh_taxes_payable.append(fh.fh_taxes_payable)
            info.fh_accrued_liabilities.append(fh.fh_accrued_liabilities)
            info.fh_other_short_term_liabilities.append(fh.fh_other_short_term_liabilities)
            info.fh_total_current_liabilities.append(fh.fh_total_current_liabilities)
            info.fh_long_term_debt.append(fh.fh_long_term_debt)
            info.fh_other_long_term_liabilities.append(fh.fh_other_long_term_liabilities)
            info.fh_total_liabilities.append(fh.fh_total_liabilities)
            info.fh_total_stockholders_equity.append(fh.fh_total_stockholders_equity)
            info.fh_total_liabilities_and_equity.append(fh.fh_total_liabilities_and_equity)

            info.lqd_current_ratio.append(lqd.lqd_current_ratio)
            info.lqd_quick_ratio.append(lqd.lqd_quick_ratio)
            info.lqd_financial_leverage.append(lqd.lqd_financial_leverage)
            info.lqd_debt_over_equity.append(lqd.lqd_debt_over_equity)

            info.efc_days_sales_outstanding.append(efc.efc_days_sales_outstanding)
            info.efc_days_inventory.append(efc.efc_days_inventory)
            info.efc_payable_period.append(efc.efc_payable_period)
            info.efc_cash_conversion_cycle.append(efc.efc_cash_conversion_cycle)
            info.efc_receivable_turnover.append(efc.efc_receivable_turnover)
            info.efc_inventory_turnover.append(efc.efc_inventory_turnover)
            info.efc_fixed_asset_turnover.append(efc.efc_fixed_asset_turnover)
            info.efc_asset_turnover.append(efc.efc_asset_turnover)

        return info
