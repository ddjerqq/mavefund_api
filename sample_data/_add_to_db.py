import asyncpg
from rgbprint import rgbprint

from utilities.csv_parser import CsvDataParser
import os
import asyncio as aio


rgbprint("<<< start loading files", color="yellow")
records = (
    record
    for file in os.listdir(".")
    if file.endswith(".csv")
    for record in CsvDataParser.parse(file)
)
rgbprint("<<< files loaded", color="green")


async def main():
    rgbprint(f">>> opening connection to database", color="yellow")
    pool = await asyncpg.create_pool(
        host=os.getenv("HOST"),
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD"),
        database="mavefund",
        loop=aio.get_running_loop(),
        max_size=100,
    )

    rgbprint(f">>> adding records started", color="yellow")

    payload = (
        list(record.flat_dict().values())
        for record in records
    )

    try:
        async with pool.acquire() as conn:
            conn: asyncpg.Connection
            await conn.executemany("""
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
            """, payload)
    except Exception as e:
        rgbprint(f"error: {e}", color="red")

    rgbprint(f"<<< records added successfully completed", color="green")


if __name__ == "__main__":
    aio.run(main())
