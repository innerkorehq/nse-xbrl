"""
nse_xbrl.typed.shareholding

High-level typed model for Regulation 31 Shareholding Pattern (SHP) filings.
"""
from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from ..core.models import XBRLInstance


class ShareholderCategory(BaseModel):
    """Holding summary for a shareholder group (Promoter, Public, Non-Promoter)."""

    category_name: str
    number_of_shareholders: Optional[int] = None
    number_of_fully_paid_shares: Optional[int] = None
    total_shares: Optional[int] = None
    shareholding_percentage: Optional[float] = None
    voting_rights_percentage: Optional[float] = None
    shares_pledged_or_encumbered: Optional[int] = None
    pledge_percentage: Optional[float] = None


class ShareholdingPatternModel(BaseModel):
    """Normalized typed representation of Regulation 31 Shareholding Pattern."""

    company_name: Optional[str] = None
    scrip_code: Optional[str] = None
    symbol: Optional[str] = None
    quarter_ended: Optional[date] = None
    declaration_quarter: Optional[str] = None

    # Summary Percentages
    promoter_holding_percentage: Optional[float] = None
    public_holding_percentage: Optional[float] = None
    non_promoter_non_public_percentage: Optional[float] = None
    promoter_shares_pledged_percentage: Optional[float] = None

    # Granular Breakdown
    categories: List[ShareholderCategory] = Field(default_factory=list)
    raw_facts_count: int = 0

    @classmethod
    def from_instance(cls, instance: XBRLInstance) -> ShareholdingPatternModel:
        """Construct a strongly typed ShareholdingPatternModel from XBRLInstance."""
        model = cls()

        model.company_name = instance.get_fact_value("NameOfTheCompany")
        model.scrip_code = (
            str(instance.get_fact_value("ScripCode"))
            if instance.get_fact_value("ScripCode") is not None
            else instance.get_entity_id()
        )
        model.symbol = instance.get_fact_value("NSESymbol")
        model.quarter_ended = instance.get_fact_value("QuarterEnded") or instance.get_fact_value("DateOfReport")
        model.declaration_quarter = instance.get_fact_value("ReportingQuarter")

        # Extract promoter & public percentages
        for fact in instance.facts:
            name_lower = fact.local_name.lower()
            if "promoterandpromotergroup" in name_lower and "percentage" in name_lower:
                if model.promoter_holding_percentage is None:
                    model.promoter_holding_percentage = fact.as_float
            elif "publicshareholding" in name_lower and "percentage" in name_lower:
                if model.public_holding_percentage is None:
                    model.public_holding_percentage = fact.as_float
            elif "pledged" in name_lower and "percentage" in name_lower:
                if model.promoter_shares_pledged_percentage is None:
                    model.promoter_shares_pledged_percentage = fact.as_float

        model.raw_facts_count = len(instance.facts)
        return model
