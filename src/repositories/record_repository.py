from __future__ import annotations

import aiosqlite

from src.models import Record
from src.repositories.repository_base import RepositoryBase


class RecordRepository(RepositoryBase):
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor):
        self.__conn = connection
        self.__curs = cursor

    async def get_all_by_symbol(self, symbol: str) -> list[Record]:
        await self.__curs.execute("""
        SELECT *
        FROM stock_record
        WHERE
            symbol = :symbol
        ORDER BY 
            symbol_date
        """, {"symbol": symbol})

        rows = await self.__curs.fetchall()
        return list(map(Record.from_db, rows))

    async def save_changes(self) -> None:
        await self.__conn.commit()

    async def get_all(self) -> list[Record]:
        await self.__curs.execute("""
        SELECT *
        FROM stock_record
        """)

        rows = await self.__curs.fetchall()
        return list(map(Record.from_db, rows))

    async def get_by_id(self, id: int) -> Record | None:
        await self.__curs.execute("""
        SELECT *
        FROM stock_record
        WHERE
            id = :id
        """, {"id": id})

        if (row := await self.__curs.fetchone()) is not None:
            return Record.from_db(row)

    async def add(self, entity: Record) -> None:
        await self.__curs.execute("""
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
            :id, 
            :company_name, 
            :symbol, 
            :date, 
            :revenue_usd_mil, 
            :gross_margin, 
            :operating_income_usd_mil, 
            :operating_margin, 
            :net_income_usd_mil, 
            :earnings_per_share_usd, 
            :dividends_usd, 
            :payout_ratio, 
            :shares_mil, 
            :book_value_per_share_usd, 
            :operation_cash_flow_usd_mil, 
            :cap_spending_usd_mil, 
            :free_cash_flow_usd_mil, 
            :free_cash_flow_per_share_usd, 
            :working_capital_usd_mil, 
            :revenue, 
            :cogs, 
            :gross_margin, 
            :sg_and_a, 
            :r_and_d, 
            :other, 
            :operating_margin, 
            :net_interest_income_and_other, 
            :ebt_margin, 
            :tax_rate_perc, 
            :net_margin_perc, 
            :asset_turnover, 
            :return_on_assets, 
            :financial_leverage, 
            :return_on_equity, 
            :return_on_invested_capital, 
            :interest_coverage, 
            :revenue_perc_over_1_year_average, 
            :revenue_perc_over_3_years_average, 
            :revenue_perc_over_5_years_average, 
            :revenue_perc_over_10_years_average, 
            :operating_income_perc_over_1_year_average, 
            :operating_income_perc_over_3_years_average, 
            :operating_income_perc_over_5_years_average, 
            :operating_income_perc_over_10_years_average, 
            :net_income_perc_over_1_year_average, 
            :net_income_perc_over_3_years_average, 
            :net_income_perc_over_5_years_average, 
            :net_income_perc_over_10_years_average, 
            :eps_perc_over_1_year_average, 
            :eps_perc_over_3_years_average, 
            :eps_perc_over_5_years_average, 
            :eps_perc_over_10_years_average, 
            :operating_cash_flow_growth_perc_yoy, 
            :free_cash_flow_growth_perc_yoy, 
            :cap_ex_as_growth_perc_of_sales, 
            :free_cash_flow_over_sales_perc, 
            :free_cash_flow_over_net_income, 
            :cash_and_short_term_investments, 
            :accounts_receivable, 
            :inventory, 
            :other_current_assets, 
            :total_current_assets, 
            :net_pp_and_e, 
            :intangibles, 
            :other_long_term_assets, 
            :total_assets, 
            :accounts_payable, 
            :short_term_debt, 
            :taxes_payable, 
            :accrued_liabilities, 
            :other_short_term_liabilities, 
            :total_current_liabilities, 
            :long_term_debt, 
            :other_long_term_liabilities, 
            :total_liabilities, 
            :total_stockholders_equity, 
            :total_liabilities_and_equity, 
            :current_ratio, 
            :quick_ratio, 
            :financial_leverage, 
            :debt_over_equity, 
            :days_sales_outstanding, 
            :days_inventory, 
            :payable_period, 
            :cash_conversion_cycle, 
            :receivable_turnover, 
            :inventory_turnover, 
            :fixed_asset_turnover, 
            :asset_turnover
        )
        """, entity.flat_dict())

    async def update(self, entity: Record) -> None:
        await self.__curs.execute("""
        UPDATE stock_record
        SET
            company_name = :company_name, 
            symbol = :symbol, 
            symbol_date = :symbol_date, 
            gp_revenue_usd_mil = :gp_revenue_usd_mil, 
            gp_gross_margin = :gp_gross_margin, 
            gp_operating_income_usd_mil = :gp_operating_income_usd_mil, 
            gp_operating_margin = :gp_operating_margin, 
            gp_net_income_usd_mil = :gp_net_income_usd_mil, 
            gp_earnings_per_share_usd = :gp_earnings_per_share_usd, 
            gp_dividends_usd = :gp_dividends_usd, 
            gp_payout_ratio = :gp_payout_ratio, 
            gp_shares_mil = :gp_shares_mil, 
            gp_book_value_per_share_usd = :gp_book_value_per_share_usd, 
            gp_operation_cash_flow_usd_mil = :gp_operation_cash_flow_usd_mil, 
            gp_cap_spending_usd_mil = :gp_cap_spending_usd_mil, 
            gp_free_cash_flow_usd_mil = :gp_free_cash_flow_usd_mil, 
            gp_free_cash_flow_per_share_usd = :gp_free_cash_flow_per_share_usd, 
            gp_working_capital_usd_mil = :gp_working_capital_usd_mil, 
            pm_revenue = :pm_revenue, 
            pm_cogs = :pm_cogs, 
            pm_gross_margin = :pm_gross_margin, 
            pm_sg_and_a = :pm_sg_and_a, 
            pm_r_and_d = :pm_r_and_d, 
            pm_other = :pm_other, 
            pm_operating_margin = :pm_operating_margin, 
            pm_net_interest_income_and_other = :pm_net_interest_income_and_other, 
            pm_ebt_margin = :pm_ebt_margin, 
            p_tax_rate_perc = :p_tax_rate_perc, 
            p_net_margin_perc = :p_net_margin_perc, 
            p_asset_turnover = :p_asset_turnover, 
            p_return_on_assets = :p_return_on_assets, 
            p_financial_leverage = :p_financial_leverage, 
            p_return_on_equity = :p_return_on_equity, 
            p_return_on_invested_capital = :p_return_on_invested_capital, 
            p_interest_coverage = :p_interest_coverage, 
            g_revenue_perc_over_1_year_average = :g_revenue_perc_over_1_year_average, 
            g_revenue_perc_over_3_years_average = :g_revenue_perc_over_3_years_average, 
            g_revenue_perc_over_5_years_average = :g_revenue_perc_over_5_years_average, 
            g_revenue_perc_over_10_years_average = :g_revenue_perc_over_10_years_average, 
            g_operating_income_perc_over_1_year_average = :g_operating_income_perc_over_1_year_average, 
            g_operating_income_perc_over_3_years_average = :g_operating_income_perc_over_3_years_average, 
            g_operating_income_perc_over_5_years_average = :g_operating_income_perc_over_5_years_average, 
            g_operating_income_perc_over_10_years_average = :g_operating_income_perc_over_10_years_average, 
            g_net_income_perc_over_1_year_average = :g_net_income_perc_over_1_year_average, 
            g_net_income_perc_over_3_years_average = :g_net_income_perc_over_3_years_average, 
            g_net_income_perc_over_5_years_average = :g_net_income_perc_over_5_years_average, 
            g_net_income_perc_over_10_years_average = :g_net_income_perc_over_10_years_average, 
            g_eps_perc_over_1_year_average = :g_eps_perc_over_1_year_average, 
            g_eps_perc_over_3_years_average = :g_eps_perc_over_3_years_average, 
            g_eps_perc_over_5_years_average = :g_eps_perc_over_5_years_average, 
            g_eps_perc_over_10_years_average = :g_eps_perc_over_10_years_average, 
            cf_operating_cash_flow_growth_perc_yoy = :cf_operating_cash_flow_growth_perc_yoy, 
            cf_free_cash_flow_growth_perc_yoy = :cf_free_cash_flow_growth_perc_yoy, 
            cf_cap_ex_as_growth_perc_of_sales = :cf_cap_ex_as_growth_perc_of_sales, 
            cf_free_cash_flow_over_sales_perc = :cf_free_cash_flow_over_sales_perc, 
            cf_free_cash_flow_over_net_income = :cf_free_cash_flow_over_net_income, 
            fh_cash_and_short_term_investments = :fh_cash_and_short_term_investments, 
            fh_accounts_receivable = :fh_accounts_receivable, 
            fh_inventory = :fh_inventory, 
            fh_other_current_assets = :fh_other_current_assets, 
            fh_total_current_assets = :fh_total_current_assets, 
            fh_net_pp_and_e = :fh_net_pp_and_e, 
            fh_intangibles = :fh_intangibles, 
            fh_other_long_term_assets = :fh_other_long_term_assets, 
            fh_total_assets = :fh_total_assets, 
            fh_accounts_payable = :fh_accounts_payable, 
            fh_short_term_debt = :fh_short_term_debt, 
            fh_taxes_payable = :fh_taxes_payable, 
            fh_accrued_liabilities = :fh_accrued_liabilities, 
            fh_other_short_term_liabilities = :fh_other_short_term_liabilities, 
            fh_total_current_liabilities = :fh_total_current_liabilities, 
            fh_long_term_debt = :fh_long_term_debt, 
            fh_other_long_term_liabilities = :fh_other_long_term_liabilities, 
            fh_total_liabilities = :fh_total_liabilities, 
            fh_total_stockholders_equity = :fh_total_stockholders_equity, 
            fh_total_liabilities_and_equity = :fh_total_liabilities_and_equity, 
            lqd_current_ratio = :lqd_current_ratio, 
            lqd_quick_ratio = :lqd_cuick_ratio, 
            lqd_financial_leverage = :lqd_financial_leverage, 
            lqd_debt_over_equity = :lqd_debt_over_equity, 
            efc_days_sales_outstanding = :efc_days_sales_outstanding, 
            efc_days_inventory = :efc_days_inventory, 
            efc_payable_period = :efc_payable_period, 
            efc_cash_conversion_cycle = :efc_cash_conversion_cycle, 
            efc_receivable_turnover = :efc_receivable_turnover, 
            efc_inventory_turnover = :efc_inventory_turnover, 
            efc_fixed_asset_turnover = :efc_fixed_asset_turnover, 
            efc_asset_turnover = :efc_asset_turnover
        WHERE
            id = :id
        """, entity.flat_dict())

    async def delete(self, entity: Record) -> None:
        await self.__curs.execute("""
        DELETE FROM stock_record
        WHERE
            id = :id
        """, {"id": id})
