from __future__ import annotations

import sqlite3

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

    # NOTE: website name
    company_name: str  # use this like an ID
    # NOTE: stock ticker symbol
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

    @classmethod
    def from_db(cls, row: sqlite3.Row) -> Record:
        return cls(
            id=row[0],
            company_name=row[1],
            symbol=row[2],
            date=row[3],

            growth_profitability=GrowthProfitability(
                date=row[3],
                revenue_usd_mil=row[4],
                gross_margin=row[5],
                operating_income_usd_mil=row[6],
                operating_margin=row[7],
                net_income_usd_mil=row[8],
                earnings_per_share_usd=row[9],
                dividends_usd=row[10],
                payout_ratio=row[11],
                shares_mil=row[12],
                book_value_per_share_usd=row[13],
                operation_cash_flow_usd_mil=row[14],
                cap_spending_usd_mil=row[15],
                free_cash_flow_usd_mil=row[16],
                free_cash_flow_per_share_usd=row[17],
                working_capital_usd_mil=row[18],
            ),
            profitability_margin=ProfitabilityMargin(
                date=row[3],
                revenue=row[19],
                cogs=row[20],
                gross_margin=row[21],
                sg_and_a=row[22],
                r_and_d=row[23],
                other=row[24],
                operating_margin=row[25],
                net_interest_income_and_other=row[26],
                ebt_margin=row[27],
            ),
            profitability=Profitability(
                date=row[3],
                tax_rate_perc=row[28],
                net_margin_perc=row[29],
                asset_turnover=row[30],
                return_on_assets=row[31],
                financial_leverage=row[32],
                return_on_equity=row[33],
                return_on_invested_capital=row[34],
                interest_coverage=row[35],
            ),
            growth=Growth(
                date=row[3],
                revenue_perc_over_1_year_average=row[36],
                revenue_perc_over_3_years_average=row[37],
                revenue_perc_over_5_years_average=row[38],
                revenue_perc_over_10_years_average=row[39],
                operating_income_perc_over_1_year_average=row[40],
                operating_income_perc_over_3_years_average=row[50],
                operating_income_perc_over_5_years_average=row[51],
                operating_income_perc_over_10_years_average=row[42],
                net_income_perc_over_1_year_average=row[44],
                net_income_perc_over_3_years_average=row[45],
                net_income_perc_over_5_years_average=row[46],
                net_income_perc_over_10_years_average=row[47],
                eps_perc_over_1_year_average=row[48],
                eps_perc_over_3_years_average=row[49],
                eps_perc_over_5_years_average=row[50],
                eps_perc_over_10_years_average=row[51],
            ),
            cash_flow=CashFlow(
                date=row[3],
                operating_cash_flow_growth_perc_yoy=row[52],
                free_cash_flow_growth_perc_yoy=row[53],
                cap_ex_as_growth_perc_of_sales=row[54],
                free_cash_flow_over_sales_perc=row[55],
                free_cash_flow_over_net_income=row[56],
            ),
            financial_health=FinancialHealth(
                date=row[3],
                cash_and_short_term_investments=row[57],
                accounts_receivable=row[58],
                inventory=row[59],
                other_current_assets=row[60],
                total_current_assets=row[61],
                net_pp_and_e=row[62],
                intangibles=row[63],
                other_long_term_assets=row[64],
                total_assets=row[65],
                accounts_payable=row[66],
                short_term_debt=row[67],
                taxes_payable=row[68],
                accrued_liabilities=row[69],
                other_short_term_liabilities=row[70],
                total_current_liabilities=row[71],
                long_term_debt=row[72],
                other_long_term_liabilities=row[73],
                total_liabilities=row[74],
                total_stockholders_equity=row[75],
                total_liabilities_and_equity=row[76],
            ),
            liquidity=Liquidity(
                date=row[3],
                current_ratio=row[77],
                quick_ratio=row[78],
                financial_leverage=row[79],
                debt_over_equity=row[80],
            ),
            efficiency=Efficiency(
                date=row[3],
                days_sales_outstanding=row[81],
                days_inventory=row[82],
                payable_period=row[83],
                cash_conversion_cycle=row[84],
                receivable_turnover=row[85],
                inventory_turnover=row[84],
                fixed_asset_turnover=row[85],
                asset_turnover=row[86],
            ),
        )

    def flat_dict(self) -> dict[str, ...]:
        return {
            'id': self.id,
            'company_name': self.company_name,
            'symbol': self.symbol,
            'date': self.date,
            **self.growth_profitability.dict(),
            **self.profitability_margin.dict(),
            **self.profitability.dict(),
            **self.growth.dict(),
            **self.cash_flow.dict(),
            **self.financial_health.dict(),
            **self.liquidity.dict(),
            **self.efficiency.dict(),
        }
