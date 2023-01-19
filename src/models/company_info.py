from __future__ import annotations

from datetime import date
from pydantic import BaseModel


class CompanyInfo(BaseModel):
    company_name: str
    ticker: str

    dates: list[date | str] = []

    # region fields

    gp_revenue_usd_mil: list[int | None] = []
    gp_gross_margin: list[float | None] = []
    gp_operating_income_usd_mil: list[float | None] = []
    gp_operating_margin: list[float | None] = []
    gp_net_income_usd_mil: list[int | None] = []
    gp_earnings_per_share_usd: list[float | None] = []
    gp_dividends_usd: list[float | None] = []
    gp_payout_ratio: list[float | None] = []
    gp_shares_mil: list[int | None] = []
    gp_book_value_per_share_usd: list[float | None] = []
    gp_operation_cash_flow_usd_mil: list[int | None] = []
    gp_cap_spending_usd_mil: list[int | None] = []
    gp_free_cash_flow_usd_mil: list[int | None] = []
    gp_free_cash_flow_per_share_usd: list[float | None] = []
    gp_working_capital_usd_mil: list[int | None] = []

    pm_revenue: list[float | None] = []
    pm_cogs: list[float | None] = []
    pm_gross_margin: list[float | None] = []
    pm_sg_and_a: list[float | None] = []
    pm_r_and_d: list[float | None] = []
    pm_other: list[float | None] = []
    pm_operating_margin: list[float | None] = []
    pm_net_interest_income_and_other: list[float | None] = []
    pm_ebt_margin: list[float | None] = []

    p_tax_rate_perc: list[float | None] = []
    p_net_margin_perc: list[float | None] = []
    p_asset_turnover: list[float | None] = []
    p_return_on_assets: list[float | None] = []
    p_financial_leverage: list[float | None] = []
    p_return_on_equity: list[float | None] = []
    p_return_on_invested_capital: list[float | None] = []
    p_interest_coverage: list[float | None] = []

    g_revenue_perc_over_1_year_average: list[float | None] = []
    g_revenue_perc_over_3_years_average: list[float | None] = []
    g_revenue_perc_over_5_years_average: list[float | None] = []
    g_revenue_perc_over_10_years_average: list[float | None] = []

    g_operating_income_perc_over_1_year_average: list[float | None] = []
    g_operating_income_perc_over_3_years_average: list[float | None] = []
    g_operating_income_perc_over_5_years_average: list[float | None] = []
    g_operating_income_perc_over_10_years_average: list[float | None] = []

    g_net_income_perc_over_1_year_average: list[float | None] = []
    g_net_income_perc_over_3_years_average: list[float | None] = []
    g_net_income_perc_over_5_years_average: list[float | None] = []
    g_net_income_perc_over_10_years_average: list[float | None] = []

    g_eps_perc_over_1_year_average: list[float | None] = []
    g_eps_perc_over_3_years_average: list[float | None] = []
    g_eps_perc_over_5_years_average: list[float | None] = []
    g_eps_perc_over_10_years_average: list[float | None] = []

    cf_operating_cash_flow_growth_perc_yoy: list[float | None] = []
    cf_free_cash_flow_growth_perc_yoy: list[float | None] = []
    cf_cap_ex_as_growth_perc_of_sales: list[float | None] = []
    cf_free_cash_flow_over_sales_perc: list[float | None] = []
    cf_free_cash_flow_over_net_income: list[float | None] = []

    fh_cash_and_short_term_investments: list[float | None] = []
    fh_accounts_receivable: list[float | None] = []
    fh_inventory: list[float | None] = []
    fh_other_current_assets: list[float | None] = []
    fh_total_current_assets: list[float | None] = []
    fh_net_pp_and_e: list[float | None] = []
    fh_intangibles: list[float | None] = []
    fh_other_long_term_assets: list[float | None] = []
    fh_total_assets: list[float | None] = []
    fh_accounts_payable: list[float | None] = []
    fh_short_term_debt: list[float | None] = []
    fh_taxes_payable: list[float | None] = []
    fh_accrued_liabilities: list[float | None] = []
    fh_other_short_term_liabilities: list[float | None] = []
    fh_total_current_liabilities: list[float | None] = []
    fh_long_term_debt: list[float | None] = []
    fh_other_long_term_liabilities: list[float | None] = []
    fh_total_liabilities: list[float | None] = []
    fh_total_stockholders_equity: list[float | None] = []
    fh_total_liabilities_and_equity: list[float | None] = []

    lqd_current_ratio: list[float | None] = []
    lqd_quick_ratio: list[float | None] = []
    lqd_financial_leverage: list[float | None] = []
    lqd_debt_over_equity: list[float | None] = []

    efc_days_sales_outstanding: list[float | None] = []
    efc_days_inventory: list[float | None] = []
    efc_payable_period: list[float | None] = []
    efc_cash_conversion_cycle: list[float | None] = []
    efc_receivable_turnover: list[float | None] = []
    efc_inventory_turnover: list[float | None] = []
    efc_fixed_asset_turnover: list[float | None] = []
    efc_asset_turnover: list[float | None] = []

    # endregion
