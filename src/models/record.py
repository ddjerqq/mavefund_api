from __future__ import annotations

from pydantic import BaseModel


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
    date: str

    revenue_usd_mil: int | None
    gross_margin: float | None
    operating_income_usd_mil: float | None
    operating_margin: float | None
    net_income_usd_mil: int | None
    earnings_per_share_usd: float | None
    dividends_usd: float | None
    payout_ratio: float | None
    shares_mil: int | None
    book_value_per_share_usd: float | None
    operation_cash_flow_usd_mil: int | None
    cap_spending_usd_mil: int | None
    free_cash_flow_usd_mil: int | None
    free_cash_flow_per_share_usd: float | None
    working_capital_usd_mil: int | None


class ProfitabilityMargin(BaseModel):
    date: str

    revenue: float | None
    cogs: float | None
    gross_margin: float | None
    sg_and_a: float | None
    r_and_d: float | None
    other: float | None
    operating_margin: float | None
    net_interest_income_and_other: float | None
    ebt_margin: float | None


class Profitability(BaseModel):
    date: str

    tax_rate_perc: float | None
    net_margin_perc: float | None
    asset_turnover: float | None
    return_on_assets: float | None
    financial_leverage: float | None
    return_on_equity: float | None
    return_on_invested_capital: float | None
    interest_coverage: float | None


class Growth(BaseModel):
    date: str

    revenue_perc_over_1_year_average: float | None
    revenue_perc_over_3_years_average: float | None
    revenue_perc_over_5_years_average: float | None
    revenue_perc_over_10_years_average: float | None

    operating_income_perc_over_1_year_average: float | None
    operating_income_perc_over_3_years_average: float | None
    operating_income_perc_over_5_years_average: float | None
    operating_income_perc_over_10_years_average: float | None

    net_income_perc_over_1_year_average: float | None
    net_income_perc_over_3_years_average: float | None
    net_income_perc_over_5_years_average: float | None
    net_income_perc_over_10_years_average: float | None

    eps_perc_over_1_year_average: float | None
    eps_perc_over_3_years_average: float | None
    eps_perc_over_5_years_average: float | None
    eps_perc_over_10_years_average: float | None


class CashFlow(BaseModel):
    date: str

    operating_cash_flow_growth_perc_yoy: float | None
    free_cash_flow_growth_perc_yoy: float | None
    cap_ex_as_growth_perc_of_sales: float | None
    free_cash_flow_over_sales_perc: float | None
    free_cash_flow_over_net_income: float | None


class FinancialHealth(BaseModel):
    date: str

    cash_and_short_term_investments: float | None
    accounts_receivable: float | None
    inventory: float | None
    other_current_assets: float | None
    total_current_assets: float | None
    net_pp_and_e: float | None
    intangibles: float | None
    other_long_term_assets: float | None
    total_assets: float | None
    accounts_payable: float | None
    short_term_debt: float | None
    taxes_payable: float | None
    accrued_liabilities: float | None
    other_short_term_liabilities: float | None
    total_current_liabilities: float | None
    long_term_debt: float | None
    other_long_term_liabilities: float | None
    total_liabilities: float | None
    total_stockholders_equity: float | None
    total_liabilities_and_equity: float | None


class Liquidity(BaseModel):
    date: str

    current_ratio: float | None
    quick_ratio: float | None
    financial_leverage: float | None
    debt_over_equity: float | None


class Efficiency(BaseModel):
    date: str

    days_sales_outstanding: float | None
    days_inventory: float | None
    payable_period: float | None
    cash_conversion_cycle: float | None
    receivable_turnover: float | None
    inventory_turnover: float | None
    fixed_asset_turnover: float | None
    asset_turnover: float | None


class Record(BaseModel):
    id: int

    company_name: str  # use this like an ID
    symbol: str  # APL and so on
    date: str

    growth_profitability: GrowthProfitability
    profitability_margin: ProfitabilityMargin
    profitability: Profitability
    growth: Growth
    cash_flow: CashFlow
    financial_health: FinancialHealth
    liquidity: Liquidity
    efficiency: Efficiency
