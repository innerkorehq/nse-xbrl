"""
nse_xbrl.typed.financial_results

High-level typed model for Regulation 33 Financial Results
(Ind AS, Banking, NBFC, Insurance, Integrated Filings).
"""
from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from ..core.models import XBRLInstance


class FinancialResultsModel(BaseModel):
    """Normalized, strongly typed representation of NSE/BSE Financial Results filing."""

    # General Information
    company_name: Optional[str] = None
    scrip_code: Optional[str] = None
    symbol: Optional[str] = None
    isin: Optional[str] = None
    industry_type: Optional[str] = None
    nature_of_report: Optional[str] = None  # Standalone vs Consolidated
    reporting_quarter: Optional[str] = None
    date_of_start_financial_year: Optional[date] = None
    date_of_end_financial_year: Optional[date] = None
    period_start_date: Optional[date] = None
    period_end_date: Optional[date] = None

    # Income Statement Items (Quarterly / Duration)
    revenue_from_operations: Optional[float] = None
    other_income: Optional[float] = None
    total_income: Optional[float] = None

    # Expenses
    cost_of_materials_consumed: Optional[float] = None
    purchases_of_stock_in_trade: Optional[float] = None
    changes_in_inventories: Optional[float] = None
    employee_benefit_expense: Optional[float] = None
    finance_costs: Optional[float] = None
    depreciation_amortization: Optional[float] = None
    other_expenses: Optional[float] = None
    total_expenses: Optional[float] = None

    # Profitability
    ebitda: Optional[float] = None
    profit_before_exceptional_items_and_tax: Optional[float] = None
    exceptional_items: Optional[float] = None
    profit_before_tax: Optional[float] = None
    tax_expense: Optional[float] = None
    current_tax: Optional[float] = None
    deferred_tax: Optional[float] = None
    profit_after_tax: Optional[float] = None  # PAT / Net Profit

    # Other Comprehensive Income
    other_comprehensive_income: Optional[float] = None
    total_comprehensive_income: Optional[float] = None

    # Earnings Per Share
    basic_eps: Optional[float] = None
    diluted_eps: Optional[float] = None

    # Balance Sheet Snapshot (Instant)
    paid_up_equity_capital: Optional[float] = None
    face_value: Optional[float] = None
    reserves_and_surplus: Optional[float] = None
    net_worth: Optional[float] = None
    total_assets: Optional[float] = None
    total_equity_and_liabilities: Optional[float] = None

    # Raw Instance Reference
    raw_facts_count: int = 0

    @classmethod
    def from_instance(cls, instance: XBRLInstance) -> FinancialResultsModel:
        """Construct a strongly typed FinancialResultsModel from any parsed XBRLInstance."""
        model = cls()

        # Company Metadata
        model.company_name = instance.get_fact_value("NameOfTheCompany")
        model.scrip_code = (
            str(instance.get_fact_value("ScripCode"))
            if instance.get_fact_value("ScripCode") is not None
            else instance.get_entity_id()
        )
        model.symbol = instance.get_fact_value("NSESymbol")
        model.isin = instance.get_fact_value("ISIN")
        model.nature_of_report = instance.get_fact_value("NatureOfReportStandaloneConsolidated")
        model.reporting_quarter = instance.get_fact_value("ReportingQuarter")

        # Dates
        model.date_of_start_financial_year = instance.get_fact_value("DateOfStartOfFinancialYear")
        model.date_of_end_financial_year = instance.get_fact_value("DateOfEndOfFinancialYear")

        # Detect primary duration context (prefer OneD or current quarter duration)
        primary_duration_ctx = None
        for ctx_id, ctx in instance.contexts.items():
            if ctx.is_duration:
                if ctx_id in {"OneD", "current", "Quarter"}:
                    primary_duration_ctx = ctx_id
                    break
                if primary_duration_ctx is None:
                    primary_duration_ctx = ctx_id

        if primary_duration_ctx and primary_duration_ctx in instance.contexts:
            ctx = instance.contexts[primary_duration_ctx]
            model.period_start_date = ctx.start_date
            model.period_end_date = ctx.end_date

        # Revenue & Income
        model.revenue_from_operations = (
            instance.get_fact_float("RevenueFromOperations", context_ref=primary_duration_ctx)
            or instance.get_fact_float("RevenueFromOperations")
            or instance.get_fact_float("IncomeFromOperations")
        )
        model.other_income = (
            instance.get_fact_float("OtherIncome", context_ref=primary_duration_ctx)
            or instance.get_fact_float("OtherIncome")
        )
        model.total_income = (
            instance.get_fact_float("Income", context_ref=primary_duration_ctx)
            or instance.get_fact_float("TotalIncome")
            or instance.get_fact_float("TotalRevenue")
        )

        # Expenses
        model.cost_of_materials_consumed = instance.get_fact_float(
            "CostOfMaterialsConsumed", context_ref=primary_duration_ctx
        ) or instance.get_fact_float("CostOfMaterialsConsumed")
        model.purchases_of_stock_in_trade = instance.get_fact_float(
            "PurchasesOfStockInTrade", context_ref=primary_duration_ctx
        )
        model.changes_in_inventories = instance.get_fact_float(
            "ChangesInInventoriesOfFinishedGoodsWorkInProgressAndStockInTrade",
            context_ref=primary_duration_ctx,
        )
        model.employee_benefit_expense = instance.get_fact_float(
            "EmployeeBenefitExpense", context_ref=primary_duration_ctx
        ) or instance.get_fact_float("EmployeeBenefitExpense")
        model.finance_costs = instance.get_fact_float(
            "FinanceCosts", context_ref=primary_duration_ctx
        ) or instance.get_fact_float("FinanceCosts")
        model.depreciation_amortization = instance.get_fact_float(
            "DepreciationDepletionAndAmortisationExpense", context_ref=primary_duration_ctx
        ) or instance.get_fact_float("DepreciationAndAmortisationExpense")
        model.other_expenses = instance.get_fact_float(
            "OtherExpenses", context_ref=primary_duration_ctx
        )
        model.total_expenses = instance.get_fact_float(
            "Expenses", context_ref=primary_duration_ctx
        ) or instance.get_fact_float("TotalExpenses")

        # Profits
        model.profit_before_exceptional_items_and_tax = instance.get_fact_float(
            "ProfitBeforeExceptionalItemsAndTax", context_ref=primary_duration_ctx
        )
        model.exceptional_items = instance.get_fact_float(
            "ExceptionalItems", context_ref=primary_duration_ctx
        )
        model.profit_before_tax = instance.get_fact_float(
            "ProfitBeforeTax", context_ref=primary_duration_ctx
        ) or instance.get_fact_float("ProfitLossBeforeTax")

        model.tax_expense = instance.get_fact_float(
            "TaxExpense", context_ref=primary_duration_ctx
        ) or instance.get_fact_float("TotalTaxExpenses")
        model.current_tax = instance.get_fact_float(
            "CurrentTax", context_ref=primary_duration_ctx
        )
        model.deferred_tax = instance.get_fact_float(
            "DeferredTax", context_ref=primary_duration_ctx
        )
        model.profit_after_tax = (
            instance.get_fact_float("ProfitLossForPeriod", context_ref=primary_duration_ctx)
            or instance.get_fact_float("NetProfitLossForPeriod")
            or instance.get_fact_float("ProfitLossFromContinuingOperations")
        )

        # EBITDA computation helper if missing
        if model.profit_before_tax is not None:
            ebitda = model.profit_before_tax
            if model.finance_costs is not None:
                ebitda += model.finance_costs
            if model.depreciation_amortization is not None:
                ebitda += model.depreciation_amortization
            model.ebitda = round(ebitda, 2)

        # EPS
        model.basic_eps = (
            instance.get_fact_float("BasicEarningsLossPerShare", context_ref=primary_duration_ctx)
            or instance.get_fact_float("BasicEarningsLossPerShareContinuingOperations")
            or instance.get_fact_float("BasicEPS")
        )
        model.diluted_eps = (
            instance.get_fact_float("DilutedEarningsLossPerShare", context_ref=primary_duration_ctx)
            or instance.get_fact_float("DilutedEarningsLossPerShareContinuingOperations")
            or instance.get_fact_float("DilutedEPS")
        )

        # Balance sheet items (instant)
        model.paid_up_equity_capital = (
            instance.get_fact_float("PaidUpValueOfEquityShareCapital")
            or instance.get_fact_float("EquityShareCapital")
        )
        model.face_value = instance.get_fact_float("FaceValueOfEquityShareCapital")
        model.reserves_and_surplus = instance.get_fact_float("ReservesExcludingRevaluationReserves")
        model.total_assets = instance.get_fact_float("Assets") or instance.get_fact_float("TotalAssets")
        model.total_equity_and_liabilities = (
            instance.get_fact_float("EquityAndLiabilities")
            or instance.get_fact_float("TotalEquityAndLiabilities")
        )

        model.raw_facts_count = len(instance.facts)
        return model
