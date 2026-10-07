"""
nse_xbrl_parser.facade

Unified auto-detecting facade API for parsing any NSE or BSE XBRL filing.
Automatically identifies the filing category and returns a typed model or universal instance.
"""
from __future__ import annotations

import asyncio
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from .core.models import XBRLFact, XBRLInstance
from .core.parser import AsyncXBRLParser
from .typed.corporate_governance import CorporateGovernanceModel
from .typed.financial_results import FinancialResultsModel
from .typed.investor_complaints import InvestorComplaintsModel
from .typed.shareholding import ShareholdingPatternModel


class FilingFormat(str, Enum):
    """Identified filing format of an XBRL filing."""
    FINANCIAL_RESULTS = "financial_results"
    SHAREHOLDING_PATTERN = "shareholding_pattern"
    CORPORATE_GOVERNANCE = "corporate_governance"
    INVESTOR_COMPLAINTS = "investor_complaints"
    GENERIC = "generic"


class ParsedFiling(BaseModel):
    """Unified container returned by the parser facade with auto-detected format and typed model."""

    format: FilingFormat
    raw_instance: XBRLInstance

    # Optional typed representations populated based on identified format
    financial_results: Optional[FinancialResultsModel] = None
    shareholding_pattern: Optional[ShareholdingPatternModel] = None
    corporate_governance: Optional[CorporateGovernanceModel] = None
    investor_complaints: Optional[InvestorComplaintsModel] = None

    @property
    def data(
        self,
    ) -> Union[
        FinancialResultsModel,
        ShareholdingPatternModel,
        CorporateGovernanceModel,
        InvestorComplaintsModel,
        XBRLInstance,
    ]:
        """Convenience property returning the typed model if available, else raw XBRLInstance."""
        if self.financial_results is not None:
            return self.financial_results
        if self.shareholding_pattern is not None:
            return self.shareholding_pattern
        if self.corporate_governance is not None:
            return self.corporate_governance
        if self.investor_complaints is not None:
            return self.investor_complaints
        return self.raw_instance

    @property
    def company_name(self) -> Optional[str]:
        return (
            self.raw_instance.get_fact_value("NameOfTheCompany")
            or getattr(self.data, "company_name", None)
        )

    @property
    def scrip_code(self) -> Optional[str]:
        return (
            str(self.raw_instance.get_fact_value("ScripCode"))
            if self.raw_instance.get_fact_value("ScripCode") is not None
            else getattr(self.data, "scrip_code", None)
        )

    @property
    def symbol(self) -> Optional[str]:
        return (
            self.raw_instance.get_fact_value("NSESymbol")
            or getattr(self.data, "symbol", None)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize data to Python dictionary."""
        if self.data is not self.raw_instance:
            return self.data.model_dump()
        return self.raw_instance.to_dict()


def detect_filing_format(instance: XBRLInstance) -> FilingFormat:
    """Analyze namespaces, schema references, and fact tags to detect the filing type."""
    # 1. Namespace inspection
    all_namespaces = " ".join(instance.target_namespaces.values()).lower()
    all_schemas = " ".join(instance.schema_refs).lower()

    if "shp" in all_namespaces or "shp" in all_schemas:
        return FilingFormat.SHAREHOLDING_PATTERN
    if "/cg/" in all_namespaces or "in-bse-cg" in all_namespaces or "/cg/" in all_schemas:
        return FilingFormat.CORPORATE_GOVERNANCE
    if "fin" in all_namespaces or "in-bse-fin" in all_namespaces or "ind-as" in all_namespaces or "fin" in all_schemas:
        return FilingFormat.FINANCIAL_RESULTS

    # 2. Fact tags heuristics
    fact_names = {f.local_name.lower() for f in instance.facts}

    # Financial results indicators
    if any(k in fact_names for k in [
        "revenuefromoperations",
        "incomefromoperations",
        "profitbeforetax",
        "costofmaterialsconsumed",
        "basicearningslosspershare",
    ]):
        return FilingFormat.FINANCIAL_RESULTS

    # Shareholding indicators
    if any(k in fact_names for k in [
        "shareholdingofpromoterandpromotergroupasapercentageoftotalnumberofshares",
        "publicshareholdingasapercentageoftotalnumberofshares",
        "promotersharespledgedasapercentage",
    ]):
        return FilingFormat.SHAREHOLDING_PATTERN

    # Corporate governance indicators
    if any(k in fact_names for k in [
        "riskmanagementcommittee",
        "compositionofboardofdirectorsabstract",
        "dateofreport",
    ]):
        return FilingFormat.CORPORATE_GOVERNANCE

    # Investor complaints indicators
    if any("investorcomplaint" in k for k in fact_names):
        return FilingFormat.INVESTOR_COMPLAINTS

    return FilingFormat.GENERIC


def create_parsed_filing(instance: XBRLInstance) -> ParsedFiling:
    """Create a ParsedFiling container with auto-detected format and populated typed adapter."""
    fmt = detect_filing_format(instance)

    fin_model = None
    shp_model = None
    cg_model = None
    ic_model = None

    if fmt == FilingFormat.FINANCIAL_RESULTS:
        fin_model = FinancialResultsModel.from_instance(instance)
    elif fmt == FilingFormat.SHAREHOLDING_PATTERN:
        shp_model = ShareholdingPatternModel.from_instance(instance)
    elif fmt == FilingFormat.CORPORATE_GOVERNANCE:
        cg_model = CorporateGovernanceModel.from_instance(instance)
    elif fmt == FilingFormat.INVESTOR_COMPLAINTS:
        ic_model = InvestorComplaintsModel.from_instance(instance)

    return ParsedFiling(
        format=fmt,
        raw_instance=instance,
        financial_results=fin_model,
        shareholding_pattern=shp_model,
        corporate_governance=cg_model,
        investor_complaints=ic_model,
    )


class XBRL:
    """Super-simple unified facade API. Give any XML / file / bytes, and it automatically parses."""

    _parser = AsyncXBRLParser()

    @classmethod
    async def parse(
        cls,
        source: Union[str, bytes, Path],
        source_name: Optional[str] = None,
    ) -> ParsedFiling:
        """Auto-detect format and parse any XML file, path, string, or raw bytes asynchronously.

        Args:
            source: A filepath (str or Path), raw XML string, or XML bytes.
            source_name: Optional name for tracking.

        Returns:
            ParsedFiling: Unified result with .format, .data, and typed fields.
        """
        # If string is a path that exists on disk, read file
        if isinstance(source, Path) or (isinstance(source, str) and not source.strip().startswith("<")):
            path = Path(source)
            if path.exists():
                instance = await cls._parser.parse_file(path)
                return create_parsed_filing(instance)

        # Otherwise parse string or bytes in memory
        instance = await cls._parser.parse(source, source_name=source_name)
        return create_parsed_filing(instance)

    @classmethod
    def parse_sync(
        cls,
        source: Union[str, bytes, Path],
        source_name: Optional[str] = None,
    ) -> ParsedFiling:
        """Synchronous version: auto-detect and parse any XML file, string, or bytes."""
        if isinstance(source, Path) or (isinstance(source, str) and not source.strip().startswith("<")):
            path = Path(source)
            if path.exists():
                data = path.read_bytes()
                instance = cls._parser.parse_sync(data, source_name=str(path))
                return create_parsed_filing(instance)

        instance = cls._parser.parse_sync(source, source_name=source_name)
        return create_parsed_filing(instance)
