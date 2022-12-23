from __future__ import annotations

from datetime import date
import typing
from pydantic import BaseModel

if typing.TYPE_CHECKING:
    from src.models import Record


class MinimalRecord(BaseModel):
    id: int
    cnm: str
    tck: str
    dt: date | str

    gp_rum: int | None
    gp_gm: float | None
    gp_oim: float | None
    gp_om: float | None
    gp_nim: int | None
    gp_eps: float | None
    gp_d: float | None
    gp_pr: float | None
    gp_sm: int | None
    gp_bvps: float | None
    gp_ocf: int | None
    gp_csp: int | None
    gp_fcf: int | None
    gp_fcfps: float | None
    gp_wc: int | None

    pm_r: float | None
    pm_cogs: float | None
    pm_gm: float | None
    pm_sga: float | None
    pm_rd: float | None
    pm_o: float | None
    pm_om: float | None
    pm_nii: float | None
    pm_ebm: float | None

    p_trp: float | None
    p_nm: float | None
    p_at: float | None
    p_roa: float | None
    p_fl: float | None
    p_roe: float | None
    p_roic: float | None
    p_ic: float | None

    g_rp_1: float | None
    g_rp_3: float | None
    g_rp_5: float | None
    g_rp_10: float | None

    g_opi_1: float | None
    g_opi_3: float | None
    g_opi_5: float | None
    g_opi_10: float | None

    g_ni_1: float | None
    g_ni_3: float | None
    g_ni_5: float | None
    g_ni_10: float | None

    g_eps_1: float | None
    g_eps_3: float | None
    g_eps_5: float | None
    g_eps_10: float | None

    cf_ocf: float | None
    cf_fcfgp: float | None
    cf_ceag: float | None
    cf_fcfos: float | None
    cf_fcfoni: float | None

    fh_casti: float | None
    fh_ar: float | None
    fh_inv: float | None
    fh_oca: float | None
    fh_tca: float | None
    fh_nppe: float | None
    fh_int: float | None
    fh_olta: float | None
    fh_ta: float | None
    fh_ap: float | None
    fh_std: float | None
    fh_tp: float | None
    fh_al: float | None
    fh_ostl: float | None
    fh_tcl: float | None
    fh_ltd: float | None
    fh_oltl: float | None
    fh_tl: float | None
    fh_tse: float | None
    fh_tle: float | None

    lqd_cr: float | None
    lqd_qr: float | None
    lqd_fl: float | None
    lqd_doe: float | None

    efc_dso: float | None
    efc_di: float | None
    efc_pp: float | None
    efc_ccc: float | None
    efc_rt: float | None
    efc_it: float | None
    efc_fat: float | None
    efc_at: float | None


    @classmethod
    def from_record(cls, record: Record) -> MinimalRecord:
        return cls(
            id=record.id,
            cnm=record.company_name,
            tck=record.symbol,
            dt=record.symbol_date,

            gp_rum=record.growth_profitability.gp_revenue_usd_mil,
            gp_gm=record.growth_profitability.gp_gross_margin,
            gp_oim=record.growth_profitability.gp_operating_income_usd_mil,
            gp_om=record.growth_profitability.gp_operating_margin,
            gp_nim=record.growth_profitability.gp_net_income_usd_mil,
            gp_eps=record.growth_profitability.gp_earnings_per_share_usd,
            gp_d=record.growth_profitability.gp_dividends_usd,
            gp_pr=record.growth_profitability.gp_payout_ratio,
            gp_sm=record.growth_profitability.gp_shares_mil,
            gp_bvps=record.growth_profitability.gp_book_value_per_share_usd,
            gp_ocf=record.growth_profitability.gp_operation_cash_flow_usd_mil,
            gp_csp=record.growth_profitability.gp_cap_spending_usd_mil,
            gp_fcf=record.growth_profitability.gp_free_cash_flow_usd_mil,
            gp_fcfps=record.growth_profitability.gp_free_cash_flow_per_share_usd,
            gp_wc=record.growth_profitability.gp_working_capital_usd_mil,

            pm_r=record.profitability_margin.pm_revenue,
            pm_cogs=record.profitability_margin.pm_cogs,
            pm_gm=record.profitability_margin.pm_gross_margin,
            pm_sga=record.profitability_margin.pm_sg_and_a,
            pm_rd=record.profitability_margin.pm_r_and_d,
            pm_o=record.profitability_margin.pm_other,
            pm_om=record.profitability_margin.pm_operating_margin,
            pm_nii=record.profitability_margin.pm_net_interest_income_and_other,
            pm_ebm=record.profitability_margin.pm_ebt_margin,

            p_trp=record.profitability.p_tax_rate_perc,
            p_nm=record.profitability.p_net_margin_perc,
            p_at=record.profitability.p_asset_turnover,
            p_roa=record.profitability.p_return_on_assets,
            p_fl=record.profitability.p_financial_leverage,
            p_roe=record.profitability.p_return_on_equity,
            p_roic=record.profitability.p_return_on_invested_capital,
            p_ic=record.profitability.p_interest_coverage,

            g_rp_1=record.growth.g_revenue_perc_over_1_year_average,
            g_rp_3=record.growth.g_revenue_perc_over_3_years_average,
            g_rp_5=record.growth.g_revenue_perc_over_5_years_average,
            g_rp_10=record.growth.g_revenue_perc_over_10_years_average,
            g_opi_1=record.growth.g_operating_income_perc_over_1_year_average,
            g_opi_3=record.growth.g_operating_income_perc_over_3_years_average,
            g_opi_5=record.growth.g_operating_income_perc_over_5_years_average,
            g_opi_10=record.growth.g_operating_income_perc_over_10_years_average,
            g_ni_1=record.growth.g_net_income_perc_over_1_year_average,
            g_ni_3=record.growth.g_net_income_perc_over_3_years_average,
            g_ni_5=record.growth.g_net_income_perc_over_5_years_average,
            g_ni_10=record.growth.g_net_income_perc_over_10_years_average,
            g_eps_1=record.growth.g_eps_perc_over_1_year_average,
            g_eps_3=record.growth.g_eps_perc_over_3_years_average,
            g_eps_5=record.growth.g_eps_perc_over_5_years_average,
            g_eps_10=record.growth.g_eps_perc_over_10_years_average,

            cf_ocf=record.cash_flow.cf_operating_cash_flow_growth_perc_yoy,
            cf_fcfgp=record.cash_flow.cf_free_cash_flow_growth_perc_yoy,
            cf_ceag=record.cash_flow.cf_cap_ex_as_growth_perc_of_sales,
            cf_fcfos=record.cash_flow.cf_free_cash_flow_over_sales_perc,
            cf_fcfoni=record.cash_flow.cf_free_cash_flow_over_net_income,

            fh_casti=record.financial_health.fh_cash_and_short_term_investments,
            fh_ar=record.financial_health.fh_accounts_receivable,
            fh_inv=record.financial_health.fh_inventory,
            fh_oca=record.financial_health.fh_other_current_assets,
            fh_tca=record.financial_health.fh_total_current_assets,
            fh_nppe=record.financial_health.fh_net_pp_and_e,
            fh_int=record.financial_health.fh_intangibles,
            fh_olta=record.financial_health.fh_other_long_term_assets,
            fh_ta=record.financial_health.fh_total_assets,
            fh_ap=record.financial_health.fh_accounts_payable,
            fh_std=record.financial_health.fh_short_term_debt,
            fh_tp=record.financial_health.fh_taxes_payable,
            fh_al=record.financial_health.fh_accrued_liabilities,
            fh_ostl=record.financial_health.fh_other_short_term_liabilities,
            fh_tcl=record.financial_health.fh_total_current_liabilities,
            fh_ltd=record.financial_health.fh_long_term_debt,
            fh_oltl=record.financial_health.fh_other_long_term_liabilities,
            fh_tl=record.financial_health.fh_total_liabilities,
            fh_tse=record.financial_health.fh_total_stockholders_equity,
            fh_tle=record.financial_health.fh_total_liabilities_and_equity,

            lqd_cr=record.liquidity.lqd_current_ratio,
            lqd_qr=record.liquidity.lqd_quick_ratio,
            lqd_fl=record.liquidity.lqd_financial_leverage,
            lqd_doe=record.liquidity.lqd_debt_over_equity,

            efc_dso=record.efficiency.efc_days_sales_outstanding,
            efc_di=record.efficiency.efc_days_inventory,
            efc_pp=record.efficiency.efc_payable_period,
            efc_ccc=record.efficiency.efc_cash_conversion_cycle,
            efc_rt=record.efficiency.efc_receivable_turnover,
            efc_it=record.efficiency.efc_inventory_turnover,
            efc_fat=record.efficiency.efc_fixed_asset_turnover,
            efc_at=record.efficiency.efc_asset_turnover,
        )
