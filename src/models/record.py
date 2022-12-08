from __future__ import annotations

import asyncpg

from pydantic import BaseModel
from datetime import date


__all__ = [
    "Record",
    "GrowthProfitability",
    "ProfitabilityMargin",
    "Profitability",
    "Growth",
    "CashFlow",
    "FinancialHealth",
    "Liquidity",
    "Efficiency",
]


class GrowthProfitability(BaseModel):
    symbol_date: date

    gp_revenue_usd_mil: int | None
    gp_gross_margin: float | None
    gp_operating_income_usd_mil: float | None
    gp_operating_margin: float | None
    gp_net_income_usd_mil: int | None
    gp_earnings_per_share_usd: float | None
    gp_dividends_usd: float | None
    gp_payout_ratio: float | None
    gp_shares_mil: int | None
    gp_book_value_per_share_usd: float | None
    gp_operation_cash_flow_usd_mil: int | None
    gp_cap_spending_usd_mil: int | None
    gp_free_cash_flow_usd_mil: int | None
    gp_free_cash_flow_per_share_usd: float | None
    gp_working_capital_usd_mil: int | None


class ProfitabilityMargin(BaseModel):
    symbol_date: date

    pm_revenue: float | None
    pm_cogs: float | None
    pm_gross_margin: float | None
    pm_sg_and_a: float | None
    pm_r_and_d: float | None
    pm_other: float | None
    pm_operating_margin: float | None
    pm_net_interest_income_and_other: float | None
    pm_ebt_margin: float | None


class Profitability(BaseModel):
    symbol_date: date

    p_tax_rate_perc: float | None
    p_net_margin_perc: float | None
    p_asset_turnover: float | None
    p_return_on_assets: float | None
    p_financial_leverage: float | None
    p_return_on_equity: float | None
    p_return_on_invested_capital: float | None
    p_interest_coverage: float | None


class Growth(BaseModel):
    symbol_date: date

    p_revenue_perc_over_1_year_average: float | None
    p_revenue_perc_over_3_years_average: float | None
    p_revenue_perc_over_5_years_average: float | None
    p_revenue_perc_over_10_years_average: float | None

    p_operating_income_perc_over_1_year_average: float | None
    p_operating_income_perc_over_3_years_average: float | None
    p_operating_income_perc_over_5_years_average: float | None
    p_operating_income_perc_over_10_years_average: float | None

    p_net_income_perc_over_1_year_average: float | None
    p_net_income_perc_over_3_years_average: float | None
    p_net_income_perc_over_5_years_average: float | None
    p_net_income_perc_over_10_years_average: float | None

    p_eps_perc_over_1_year_average: float | None
    p_eps_perc_over_3_years_average: float | None
    p_eps_perc_over_5_years_average: float | None
    p_eps_perc_over_10_years_average: float | None


class CashFlow(BaseModel):
    symbol_date: date

    cf_operating_cash_flow_growth_perc_yoy: float | None
    cf_free_cash_flow_growth_perc_yoy: float | None
    cf_cap_ex_as_growth_perc_of_sales: float | None
    cf_free_cash_flow_over_sales_perc: float | None
    cf_free_cash_flow_over_net_income: float | None


class FinancialHealth(BaseModel):
    symbol_date: date

    fh_cash_and_short_term_investments: float | None
    fh_accounts_receivable: float | None
    fh_inventory: float | None
    fh_other_current_assets: float | None
    fh_total_current_assets: float | None
    fh_net_pp_and_e: float | None
    fh_intangibles: float | None
    fh_other_long_term_assets: float | None
    fh_total_assets: float | None
    fh_accounts_payable: float | None
    fh_short_term_debt: float | None
    fh_taxes_payable: float | None
    fh_accrued_liabilities: float | None
    fh_other_short_term_liabilities: float | None
    fh_total_current_liabilities: float | None
    fh_long_term_debt: float | None
    fh_other_long_term_liabilities: float | None
    fh_total_liabilities: float | None
    fh_total_stockholders_equity: float | None
    fh_total_liabilities_and_equity: float | None


class Liquidity(BaseModel):
    symbol_date: date

    lqd_current_ratio: float | None
    lqd_quick_ratio: float | None
    lqd_financial_leverage: float | None
    lqd_debt_over_equity: float | None


class Efficiency(BaseModel):
    symbol_date: date

    efc_days_sales_outstanding: float | None
    efc_days_inventory: float | None
    efc_payable_period: float | None
    efc_cash_conversion_cycle: float | None
    efc_receivable_turnover: float | None
    efc_inventory_turnover: float | None
    efc_fixed_asset_turnover: float | None
    efc_asset_turnover: float | None


class Record(BaseModel):
    id: int

    # NOTE: website name
    company_name: str  # use this like an ID
    # NOTE: stock ticker symbol
    symbol: str  # APL and so on
    symbol_date: date

    growth_profitability: GrowthProfitability
    profitability_margin: ProfitabilityMargin
    profitability: Profitability
    growth: Growth
    cash_flow: CashFlow
    financial_health: FinancialHealth
    liquidity: Liquidity
    efficiency: Efficiency

    @classmethod
    def from_db(cls, row: asyncpg.Record) -> Record:
        return cls(
            id=row['id'],
            company_name=row['company_name'],
            symbol=row['symbol'],
            symbol_date=row['symbol_date'],

            growth_profitability=GrowthProfitability(**row),
            profitability_margin=ProfitabilityMargin(**row),
            profitability=Profitability(**row),
            growth=Growth(**row),
            cash_flow=CashFlow(**row),
            financial_health=FinancialHealth(**row),
            liquidity=Liquidity(**row),
            efficiency=Efficiency(**row),
        )

    def flat_dict(self) -> dict[str, str | int | float | None]:
        return {
            'id': self.id,
            'company_name': self.company_name,
            'symbol': self.symbol,
            'symbol_date': self.symbol_date,
            **self.growth_profitability.dict(),
            **self.profitability_margin.dict(),
            **self.profitability.dict(),
            **self.growth.dict(),
            **self.cash_flow.dict(),
            **self.financial_health.dict(),
            **self.liquidity.dict(),
            **self.efficiency.dict(),
        }
