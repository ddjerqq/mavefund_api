CREATE TABLE stock_record
(
    id                                INTEGER        NOT NULL
        PRIMARY KEY
        UNIQUE,
    company_name                      VARCHAR(32)    NOT NULL,
    symbol                            VARCHAR(64)    NOT NULL,
    symbol_date                       DATE           NOT NULL,

    -- growth profitability
    gp_revenue_usd_mil                INTEGER,
    gp_gross_margin                   REAL,
    gp_operating_income_usd_mil       REAL,
    gp_operating_margin               REAL,
    gp_net_income_usd_mil             INTEGER,
    gp_earnings_per_share_usd         REAL,
    gp_dividends_usd                  REAL,
    gp_payout_ratio                   REAL,
    gp_shares_mil                     INTEGER,
    gp_book_value_per_share_usd       REAL,
    gp_operation_cash_flow_usd_mil    INTEGER,
    gp_cap_spending_usd_mil           INTEGER,
    gp_free_cash_flow_usd_mil         INTEGER,
    gp_free_cash_flow_per_share_usd   REAL,
    gp_working_capital_usd_mil        INTEGER,

    -- profitability margin
    pm_revenue                        REAL,
    pm_cogs                           REAL,
    pm_gross_margin                   REAL,
    pm_sg_and_a                       REAL,
    pm_r_and_d                        REAL,
    pm_other                          REAL,
    pm_operating_margin               REAL,
    pm_net_interest_income_and_other  REAL,
    pm_ebt_margin                     REAL,

    -- profitability
    p_tax_rate_perc                   REAL,
    p_net_margin_perc                 REAL,
    p_asset_turnover                  REAL,
    p_return_on_assets                REAL,
    p_financial_leverage              REAL,
    p_return_on_equity                REAL,
    p_return_on_invested_capital      REAL,
    p_interest_coverage               REAL,

    -- growth
    g_revenue_perc_over_1_year_average            REAL,
    g_revenue_perc_over_3_years_average           REAL,
    g_revenue_perc_over_5_years_average           REAL,
    g_revenue_perc_over_10_years_average          REAL,

    g_operating_income_perc_over_1_year_average   REAL,
    g_operating_income_perc_over_3_years_average  REAL,
    g_operating_income_perc_over_5_years_average  REAL,
    g_operating_income_perc_over_10_years_average REAL,

    g_net_income_perc_over_1_year_average         REAL,
    g_net_income_perc_over_3_years_average        REAL,
    g_net_income_perc_over_5_years_average        REAL,
    g_net_income_perc_over_10_years_average       REAL,

    g_eps_perc_over_1_year_average                REAL,
    g_eps_perc_over_3_years_average               REAL,
    g_eps_perc_over_5_years_average               REAL,
    g_eps_perc_over_10_years_average              REAL,

    -- cash flow
    cf_operating_cash_flow_growth_perc_yoy         REAL,
    cf_free_cash_flow_growth_perc_yoy              REAL,
    cf_cap_ex_as_growth_perc_of_sales              REAL,
    cf_free_cash_flow_over_sales_perc              REAL,
    cf_free_cash_flow_over_net_income              REAL,

    -- financial health
    fh_cash_and_short_term_investments             REAL,
    fh_accounts_receivable                         REAL,
    fh_inventory                                   REAL,
    fh_other_current_assets                        REAL,
    fh_total_current_assets                        REAL,
    fh_net_pp_and_e                                REAL,
    fh_intangibles                                 REAL,
    fh_other_long_term_assets                      REAL,
    fh_total_assets                                REAL,
    fh_accounts_payable                            REAL,
    fh_short_term_debt                             REAL,
    fh_taxes_payable                               REAL,
    fh_accrued_liabilities                         REAL,
    fh_other_short_term_liabilities                REAL,
    fh_total_current_liabilities                   REAL,
    fh_long_term_debt                              REAL,
    fh_other_long_term_liabilities                 REAL,
    fh_total_liabilities                           REAL,
    fh_total_stockholders_equity                   REAL,
    fh_total_liabilities_and_equity                REAL,

    -- liquidity
    lqd_current_ratio                              REAL,
    lqd_quick_ratio                                REAL,
    lqd_financial_leverage                         REAL,
    lqd_debt_over_equity                            REAL,

    -- efficiency
    efc_days_sales_outstanding                     REAL,
    efc_days_inventory                             REAL,
    efc_payable_period                             REAL,
    efc_cash_conversion_cycle                      REAL,
    efc_receivable_turnover                        REAL,
    efc_inventory_turnover                         REAL,
    efc_fixed_asset_turnover                       REAL,
    efc_asset_turnover                             REAL
);

CREATE UNIQUE INDEX stock_record_id_uindex
    ON stock_record (id);
