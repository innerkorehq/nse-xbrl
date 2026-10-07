"""
nse-xbrl

Async Python 3.14 library for parsing XBRL Filing Information of NSE & BSE across all taxonomies.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Union

from .client.nse_client import AsyncNSEClient
from .core.context import ExplicitMember, PeriodType, XBRLContext
from .core.models import XBRLFact, XBRLInstance
from .core.parser import AsyncXBRLParser
from .core.unit import XBRLUnit
from .taxonomy.downloader import AsyncTaxonomyDownloader
from .taxonomy.linkbase import ConceptLabel, TaxonomyLinkbase
from .taxonomy.registry import TaxonomyInfo, TaxonomyRegistry
from .taxonomy.schema import SchemaElement, TaxonomySchema
from .typed.corporate_governance import CorporateGovernanceModel
from .typed.financial_results import FinancialResultsModel
from .typed.shareholding import ShareholdingPatternModel

__version__ = "0.1.0"

_parser = AsyncXBRLParser()


async def parse_xbrl(
    content: Union[str, bytes],
    source_name: str | None = None,
) -> XBRLInstance:
    """Parse an XBRL XML instance document asynchronously.
    
    Args:
        content: XML string or raw bytes.
        source_name: Optional file or URL name for tracking.
        
    Returns:
        XBRLInstance: Universal representation of facts, contexts, and units.
    """
    return await _parser.parse(content, source_name=source_name)


async def parse_file(file_path: Union[str, Path]) -> XBRLInstance:
    """Parse a local XBRL file asynchronously."""
    return await _parser.parse_file(file_path)


async def parse_archive(zip_bytes: bytes) -> List[XBRLInstance]:
    """Parse all XBRL filings within a zip archive asynchronously."""
    return await _parser.parse_zip(zip_bytes)


def parse_xbrl_sync(
    content: Union[str, bytes],
    source_name: str | None = None,
) -> XBRLInstance:
    """Synchronous parsing convenience function."""
    return _parser.parse_sync(content, source_name=source_name)


__all__ = [
    "parse_xbrl",
    "parse_file",
    "parse_archive",
    "parse_xbrl_sync",
    "AsyncXBRLParser",
    "XBRLInstance",
    "XBRLFact",
    "XBRLContext",
    "XBRLUnit",
    "PeriodType",
    "ExplicitMember",
    "TaxonomyRegistry",
    "TaxonomyInfo",
    "TaxonomySchema",
    "SchemaElement",
    "TaxonomyLinkbase",
    "ConceptLabel",
    "AsyncTaxonomyDownloader",
    "FinancialResultsModel",
    "ShareholdingPatternModel",
    "CorporateGovernanceModel",
    "AsyncNSEClient",
]
