"""
nse_xbrl_parser.typed.corporate_governance

High-level typed model for Regulation 27(2) Corporate Governance filings.
"""
from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from ..core.models import XBRLInstance


class DirectorInfo(BaseModel):
    """Information for a company director in Corporate Governance report."""

    din: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None  # e.g. Executive, Non-Executive, Independent
    date_of_appointment: Optional[date] = None
    tenure: Optional[float] = None
    board_meetings_attended: Optional[int] = None


class CorporateGovernanceModel(BaseModel):
    """Normalized typed representation of Regulation 27(2) Corporate Governance filing."""

    company_name: Optional[str] = None
    scrip_code: Optional[str] = None
    symbol: Optional[str] = None
    reporting_quarter: Optional[str] = None
    date_of_report: Optional[date] = None

    has_risk_management_committee: Optional[bool] = None
    directors: List[DirectorInfo] = Field(default_factory=list)
    raw_facts_count: int = 0

    @classmethod
    def from_instance(cls, instance: XBRLInstance) -> CorporateGovernanceModel:
        """Construct CorporateGovernanceModel from XBRLInstance."""
        model = cls()
        model.company_name = instance.get_fact_value("NameOfTheCompany")
        model.scrip_code = (
            str(instance.get_fact_value("ScripCode"))
            if instance.get_fact_value("ScripCode") is not None
            else instance.get_entity_id()
        )
        model.symbol = instance.get_fact_value("NSESymbol")
        model.reporting_quarter = instance.get_fact_value("ReportingQuarter")
        model.date_of_report = instance.get_fact_value("DateOfReport")
        model.has_risk_management_committee = instance.get_fact_value("RiskManagementCommittee")

        model.raw_facts_count = len(instance.facts)
        return model
