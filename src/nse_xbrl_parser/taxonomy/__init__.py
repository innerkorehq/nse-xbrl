"""
nse_xbrl_parser.taxonomy

Taxonomy schemas, label linkbases, downloader, and full 58-taxonomy registry.
"""
from __future__ import annotations

from .downloader import AsyncTaxonomyDownloader
from .linkbase import ConceptLabel, TaxonomyLinkbase
from .registry import TaxonomyInfo, TaxonomyRegistry
from .schema import SchemaElement, TaxonomySchema

__all__ = [
    "TaxonomyInfo",
    "TaxonomyRegistry",
    "TaxonomySchema",
    "SchemaElement",
    "TaxonomyLinkbase",
    "ConceptLabel",
    "AsyncTaxonomyDownloader",
]
