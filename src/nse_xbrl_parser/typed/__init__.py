"""
nse_xbrl_parser.typed

High-level strongly typed models for standardized Indian regulatory filings.
"""
from __future__ import annotations

from .corporate_governance import CorporateGovernanceModel, DirectorInfo
from .financial_results import FinancialResultsModel
from .investor_complaints import InvestorComplaintsModel
from .shareholding import ShareholderCategory, ShareholdingPatternModel

__all__ = [
    "FinancialResultsModel",
    "ShareholdingPatternModel",
    "ShareholderCategory",
    "CorporateGovernanceModel",
    "DirectorInfo",
    "InvestorComplaintsModel",
]
