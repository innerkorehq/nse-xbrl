"""
nse_xbrl_parser.typed.investor_complaints

High-level typed model for Regulation 13(3) Statement of Investor Complaints.
"""
from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from ..core.models import XBRLInstance


class InvestorComplaintsModel(BaseModel):
    """Normalized typed representation of Regulation 13(3) Investor Complaints filing."""

    company_name: Optional[str] = None
    scrip_code: Optional[str] = None
    symbol: Optional[str] = None
    reporting_quarter: Optional[str] = None
    period_start_date: Optional[date] = None
    period_end_date: Optional[date] = None

    # Grievance Metrics
    complaints_pending_at_start: Optional[int] = None
    complaints_received_during_period: Optional[int] = None
    complaints_disposed_during_period: Optional[int] = None
    complaints_unresolved_at_end: Optional[int] = None

    raw_facts_count: int = 0

    @classmethod
    def from_instance(cls, instance: XBRLInstance) -> InvestorComplaintsModel:
        """Construct InvestorComplaintsModel from an XBRLInstance."""
        model = cls()
        model.company_name = instance.get_fact_value("NameOfTheCompany")
        model.scrip_code = (
            str(instance.get_fact_value("ScripCode"))
            if instance.get_fact_value("ScripCode") is not None
            else instance.get_entity_id()
        )
        model.symbol = instance.get_fact_value("NSESymbol")
        model.reporting_quarter = instance.get_fact_value("ReportingQuarter")

        # Period dates
        for ctx in instance.contexts.values():
            if ctx.is_duration and ctx.start_date and ctx.end_date:
                model.period_start_date = ctx.start_date
                model.period_end_date = ctx.end_date
                break

        # Fact values
        for f in instance.facts:
            name_lower = f.local_name.lower()
            val_int = int(f.value) if isinstance(f.value, (int, float)) else None
            if "pending" in name_lower and "beginning" in name_lower:
                model.complaints_pending_at_start = val_int
            elif "received" in name_lower and "period" in name_lower:
                model.complaints_received_during_period = val_int
            elif ("disposed" in name_lower or "resolved" in name_lower) and "during" in name_lower:
                model.complaints_disposed_during_period = val_int
            elif "unresolved" in name_lower or ("pending" in name_lower and "end" in name_lower):
                model.complaints_unresolved_at_end = val_int

        model.raw_facts_count = len(instance.facts)
        return model
