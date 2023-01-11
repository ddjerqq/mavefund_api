from __future__ import annotations

import logging.config
import os
from os.path import dirname, realpath, join
import asyncpg
import asyncio as aio
import aiofiles

from src.utilities.csv_parser import CsvDataParser
from src.models import User

# mavefund_api/
PATH = dirname(realpath(__file__))


logging.config.fileConfig(join(PATH, "logging.conf"))
log = logging.getLogger("setup")



files = [
    join(PATH, "sample_data", file)
    for file in os.listdir(join(PATH, "sample_data"))
    if file.endswith(".csv")
]

records = (
    record
    for file in files
    for record in CsvDataParser.parse(file)
)


conn: asyncpg.Connection | None = None


async def init():
    global conn
    log.info("populate initializing")
    conn = await asyncpg.connect(
        host=os.getenv("HOST"),
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD")
    )
    log.info("populate initialized")


async def _record_up():
    log.info("records going UP")
    record_payload = (
        tuple(record.flat_dict().values())
        for record in records
    )

    try:
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
        """, record_payload)
    except:
        log.exception(
            "error occurred while inserting records inside the database",
            exc_info=True
        )
    else:
        log.info("records are UP")


async def _test_users_up():
    # password is "password"
    log.info("test users going UP")
    pw = "$2b$08$Fr4c.uB6ZlVzH8kXJ8Kmyu0G0RjobQtZ1slNMbWXI5NEJdMVgE2zq"
    users = [
        User(id=1001, username="free", email="free@mavefund.com", password_hash=pw, rank=-1, verified=True),
        User(id=1002, username="basic", email="basic@mavefund.com", password_hash=pw, rank=0, verified=True),
        User(id=1003, username="premium", email="premium@mavefund.com", password_hash=pw, rank=1, verified=True),
        User(id=1004, username="super", email="super@mavefund.com", password_hash=pw, rank=2, verified=True),
        User(id=1005, username="admin", email="admin@mavefund.com", password_hash=pw, rank=3, verified=True),
    ]

    try:
        await conn.execute("""
            INSERT INTO app_user
            (id, username, email, password_hash, rank, verified)
            VALUES 
            (
                $1,
                $2,
                $3,
                $4,
                $5,
                $6
            )
            """, map(lambda user: user.dict().values(), users))
    except:
        log.exception(
            "error occurred while inserting test users inside the database",
            exc_info=True
        )
    else:
        log.info("test users are UP")


async def _read_file(filepath: str) -> tuple[str, str]:
    _, tail = os.path.split(filepath)
    symbol, *_ = tail.split(" ")
    async with aiofiles.open(filepath) as f:
        content = await f.read()
    return symbol, content


async def _csv_data_up():
    log.info("csv files going UP")
    symbol_filenames = await aio.gather(*[
        _read_file(join(PATH, "sample_data", file))
        for file in os.listdir("sample_data")
        if file.endswith(".csv")
    ])

    await conn.executemany("""
    INSERT INTO csv_data
    VALUES 
    (
        $1,
        $2
    )
    """, symbol_filenames)
    log.info("csv files are UP")


async def up():
    log.info("starting populating the database")
    # await _record_up()
    # await _test_users_up()
    await _csv_data_up()
    log.info("populating the database finished successfully")


async def down():
    log.info("starting tearing DOWN the data")
    await conn.execute("""
    DELETE FROM stock_record;
    DELETE FROM app_user;
    DELETE FROM csv_data;
    """)
    log.info("tearing DOWN data done")



async def main():
    os.environ["host"] = "31.220.57.57"
    await init()
    await up()


if __name__ == "__main__":
    aio.run(main())
