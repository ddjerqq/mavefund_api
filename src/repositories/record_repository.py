from __future__ import annotations

import asyncpg

from src.models import Record
from src.repositories.repository_base import RepositoryBase


class RecordRepository(RepositoryBase):
    def __init__(self, pool: asyncpg.Pool):
        self.__pool = pool

    async def get_all_by_company_name(self, name: str) -> dict:
        name = f"%{name}%"
        async with self.__pool.acquire(timeout=60) as conn:
            rows = await conn.fetch("""
            SELECT symbol, company_name
            FROM stock_record
            WHERE company_name LIKE $1
                  OR symbol    LIKE $1
            """, name)

            return {
                symbol: company_name
                for symbol, company_name in rows
            }

    async def get_all_by_symbol(self, symbol: str) -> list[Record]:
        async with self.__pool.acquire(timeout=60) as conn:
            rows = await conn.fetch("""
            SELECT *
            FROM stock_record
            WHERE
                symbol = $1
            ORDER BY 
                symbol_date
            """, symbol)

            return list(map(Record.from_db, rows))

    async def get_all(self) -> list[Record]:
        async with self.__pool.acquire(timeout=60) as conn:
            rows = await conn.fetch("""
            SELECT *
            FROM stock_record
            """)

            return list(map(Record.from_db, rows))

    async def get_by_id(self, id: int) -> Record | None:
        async with self.__pool.acquire(timeout=60) as conn:
            row = await conn.fetchrow("""
            SELECT *
            FROM stock_record
            WHERE
                id = $1
            """, id)

            if row is not None:
                return Record.from_db(row)

    async def add(self, entity: Record) -> None:
        async with self.__pool.acquire(timeout=60) as conn:
            await conn.execute("""
            INSERT INTO stock_record(
                id, 
                company_name, 
                symbol, 
                symbol_date, 
                gp_revenue_usd_mil, 
                gp_gross_margin, 
                gp_operating_income_usd_mil, 
                gp_operating_margin, 
                gp_net_income_usd_mil, 
                gp_earnings_per_share_usd, 
                gp_dividends_usd, 
                gp_payout_ratio, 
                gp_shares_mil, 
                gp_book_value_per_share_usd, 
                gp_operation_cash_flow_usd_mil, 
                gp_cap_spending_usd_mil, 
                gp_free_cash_flow_usd_mil, 
                gp_free_cash_flow_per_share_usd, 
                gp_working_capital_usd_mil, 
                pm_revenue, 
                pm_cogs, 
                pm_gross_margin, 
                pm_sg_and_a, 
                pm_r_and_d, 
                pm_other, 
                pm_operating_margin, 
                pm_net_interest_income_and_other, 
                pm_ebt_margin, 
                p_tax_rate_perc, 
                p_net_margin_perc, 
                p_asset_turnover, 
                p_return_on_assets, 
                p_financial_leverage, 
                p_return_on_equity, 
                p_return_on_invested_capital, 
                p_interest_coverage, 
                g_revenue_perc_over_1_year_average, 
                g_revenue_perc_over_3_years_average, 
                g_revenue_perc_over_5_years_average, 
                g_revenue_perc_over_10_years_average, 
                g_operating_income_perc_over_1_year_average, 
                g_operating_income_perc_over_3_years_average, 
                g_operating_income_perc_over_5_years_average, 
                g_operating_income_perc_over_10_years_average, 
                g_net_income_perc_over_1_year_average, 
                g_net_income_perc_over_3_years_average, 
                g_net_income_perc_over_5_years_average, 
                g_net_income_perc_over_10_years_average, 
                g_eps_perc_over_1_year_average, 
                g_eps_perc_over_3_years_average, 
                g_eps_perc_over_5_years_average, 
                g_eps_perc_over_10_years_average, 
                cf_operating_cash_flow_growth_perc_yoy, 
                cf_free_cash_flow_growth_perc_yoy, 
                cf_cap_ex_as_growth_perc_of_sales, 
                cf_free_cash_flow_over_sales_perc, 
                cf_free_cash_flow_over_net_income, 
                fh_cash_and_short_term_investments, 
                fh_accounts_receivable, 
                fh_inventory, 
                fh_other_current_assets, 
                fh_total_current_assets, 
                fh_net_pp_and_e, 
                fh_intangibles, 
                fh_other_long_term_assets, 
                fh_total_assets, 
                fh_accounts_payable, 
                fh_short_term_debt, 
                fh_taxes_payable, 
                fh_accrued_liabilities, 
                fh_other_short_term_liabilities, 
                fh_total_current_liabilities, 
                fh_long_term_debt, 
                fh_other_long_term_liabilities, 
                fh_total_liabilities, 
                fh_total_stockholders_equity, 
                fh_total_liabilities_and_equity, 
                lqd_current_ratio, 
                lqd_quick_ratio, 
                lqd_financial_leverage, 
                lqd_debt_over_equity, 
                efc_days_sales_outstanding, 
                efc_days_inventory, 
                efc_payable_period, 
                efc_cash_conversion_cycle, 
                efc_receivable_turnover, 
                efc_inventory_turnover, 
                efc_fixed_asset_turnover, 
                efc_asset_turnover
            )
            
            VALUES 
            (
                $1,
                $2,
                $3,
                $4,
                $5,
                $6,
                $7,
                $8,
                $9,
                $10,
                $11,
                $12,
                $13,
                $14,
                $15,
                $16,
                $17,
                $18,
                $19,
                $20,
                $21,
                $22,
                $23,
                $24,
                $25,
                $26,
                $27,
                $28,
                $29,
                $30,
                $31,
                $32,
                $33,
                $34,
                $35,
                $36,
                $37,
                $38,
                $39,
                $40,
                $41,
                $42,
                $43,
                $44,
                $45,
                $46,
                $47,
                $48,
                $49,
                $50,
                $51,
                $52,
                $53,
                $54,
                $55,
                $56,
                $57,
                $58,
                $59,
                $60,
                $61,
                $62,
                $63,
                $64,
                $65,
                $66,
                $67,
                $68,
                $69,
                $70,
                $71,
                $72,
                $73,
                $74,
                $75,
                $76,
                $77,
                $78,
                $79,
                $80,
                $81,
                $82,
                $83,
                $84,
                $85,
                $86,
                $87,
                $88,
                $89
            )
            """, *entity.flat_dict().values())

    async def update(self, entity: Record) -> None:
        async with self.__pool.acquire(timeout=60) as conn:
            await conn.execute("""
        UPDATE stock_record
        SET
            company_name = $2, 
            symbol = $3, 
            symbol_date = $4, 
            gp_revenue_usd_mil = $5, 
            gp_gross_margin = $6, 
            gp_operating_income_usd_mil = $7, 
            gp_operating_margin = $8, 
            gp_net_income_usd_mil = $9, 
            gp_earnings_per_share_usd = $10, 
            gp_dividends_usd = $11, 
            gp_payout_ratio = $12, 
            gp_shares_mil = $13, 
            gp_book_value_per_share_usd = $14, 
            gp_operation_cash_flow_usd_mil = $15, 
            gp_cap_spending_usd_mil = $16, 
            gp_free_cash_flow_usd_mil = $17, 
            gp_free_cash_flow_per_share_usd = $18, 
            gp_working_capital_usd_mil = $19, 
            pm_revenue = $20, 
            pm_cogs = $21, 
            pm_gross_margin = $22, 
            pm_sg_and_a = $23, 
            pm_r_and_d = $24, 
            pm_other = $25, 
            pm_operating_margin = $26, 
            pm_net_interest_income_and_other = $27, 
            pm_ebt_margin = $28, 
            p_tax_rate_perc = $29, 
            p_net_margin_perc = $30, 
            p_asset_turnover = $31, 
            p_return_on_assets = $32, 
            p_financial_leverage = $33, 
            p_return_on_equity = $34, 
            p_return_on_invested_capital = $35, 
            p_interest_coverage = $36, 
            g_revenue_perc_over_1_year_average = $37, 
            g_revenue_perc_over_3_years_average = $38, 
            g_revenue_perc_over_5_years_average = $39, 
            g_revenue_perc_over_10_years_average = $40, 
            g_operating_income_perc_over_1_year_average = $41, 
            g_operating_income_perc_over_3_years_average = $42, 
            g_operating_income_perc_over_5_years_average = $43, 
            g_operating_income_perc_over_10_years_average = $44, 
            g_net_income_perc_over_1_year_average = $45, 
            g_net_income_perc_over_3_years_average = $46, 
            g_net_income_perc_over_5_years_average = $47, 
            g_net_income_perc_over_10_years_average = $48, 
            g_eps_perc_over_1_year_average = $49, 
            g_eps_perc_over_3_years_average = $50, 
            g_eps_perc_over_5_years_average = $51, 
            g_eps_perc_over_10_years_average = $52, 
            cf_operating_cash_flow_growth_perc_yoy = $53, 
            cf_free_cash_flow_growth_perc_yoy = $54, 
            cf_cap_ex_as_growth_perc_of_sales = $55, 
            cf_free_cash_flow_over_sales_perc = $56, 
            cf_free_cash_flow_over_net_income = $57, 
            fh_cash_and_short_term_investments = $58, 
            fh_accounts_receivable = $59, 
            fh_inventory = $60, 
            fh_other_current_assets = $61, 
            fh_total_current_assets = $62, 
            fh_net_pp_and_e = $63, 
            fh_intangibles = $64, 
            fh_other_long_term_assets = $65, 
            fh_total_assets = $66, 
            fh_accounts_payable = $67, 
            fh_short_term_debt = $68, 
            fh_taxes_payable = $69, 
            fh_accrued_liabilities = $70, 
            fh_other_short_term_liabilities = $71, 
            fh_total_current_liabilities = $72, 
            fh_long_term_debt = $73, 
            fh_other_long_term_liabilities = $74, 
            fh_total_liabilities = $75, 
            fh_total_stockholders_equity = $76, 
            fh_total_liabilities_and_equity = $77, 
            lqd_current_ratio = $78, 
            lqd_quick_ratio = $79, 
            lqd_financial_leverage = $80, 
            lqd_debt_over_equity = $81, 
            efc_days_sales_outstanding = $82, 
            efc_days_inventory = $83, 
            efc_payable_period = $84, 
            efc_cash_conversion_cycle = $85, 
            efc_receivable_turnover = $86, 
            efc_inventory_turnover = $87, 
            efc_fixed_asset_turnover = $88, 
            efc_asset_turnover = $89
        WHERE
            id = $1
        """, *entity.flat_dict().values())

    async def delete(self, id: int) -> None:
        async with self.__pool.acquire() as conn:
            await conn.execute("""
        DELETE FROM stock_record
        WHERE
            id = $1
        """, id)
