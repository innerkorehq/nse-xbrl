"""
nse_xbrl_parser.taxonomy.registry

Registry of all 58 NSE & BSE XBRL Taxonomies.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TaxonomyInfo(BaseModel):
    """Metadata describing a specific NSE/BSE filing taxonomy."""

    id: int
    name: str
    regulation: str
    all_links: List[str] = Field(default_factory=list)
    taxonomy_links: List[str] = Field(default_factory=list)
    utility_links: List[str] = Field(default_factory=list)

    @property
    def primary_taxonomy_url(self) -> Optional[str]:
        """Return the direct download URL for the taxonomy package if available."""
        if self.taxonomy_links:
            return self.taxonomy_links[0]
        if self.all_links:
            return self.all_links[0]
        return None

    @property
    def primary_utility_url(self) -> Optional[str]:
        """Return the direct download URL for the Excel utility if available."""
        if self.utility_links:
            return self.utility_links[0]
        return None


class TaxonomyRegistry:
    """Registry managing all 58 official taxonomy definitions."""

    def __init__(self, catalog_path: Optional[Path] = None) -> None:
        if catalog_path is None:
            catalog_path = Path(__file__).parent / "taxonomies.json"
        self._catalog_path = catalog_path
        self._taxonomies: Dict[int, TaxonomyInfo] = {}
        self._load_catalog()

    def _load_catalog(self) -> None:
        if not self._catalog_path.exists():
            return
        data = json.loads(self._catalog_path.read_text(encoding="utf-8"))
        for item in data:
            # Extract clean regulation name
            full_name = item.get("name", "")
            info = TaxonomyInfo(
                id=item["id"],
                name=full_name,
                regulation=full_name.split("-")[0].strip() if "-" in full_name else full_name,
                all_links=item.get("all_links", []),
                taxonomy_links=item.get("taxonomy_links", []),
                utility_links=item.get("utility_links", []),
            )
            self._taxonomies[info.id] = info

    def count(self) -> int:
        """Total number of registered taxonomies (58)."""
        return len(self._taxonomies)

    def get_all(self) -> List[TaxonomyInfo]:
        """Get all registered taxonomies ordered by ID."""
        return sorted(self._taxonomies.values(), key=lambda t: t.id)

    def get_by_id(self, taxonomy_id: int) -> Optional[TaxonomyInfo]:
        """Lookup taxonomy by its ID (1 to 58)."""
        return self._taxonomies.get(taxonomy_id)

    def find_by_name(self, search_term: str) -> List[TaxonomyInfo]:
        """Search taxonomies by keyword in name or regulation (e.g. 'Shareholding', 'Financial', 'Governance')."""
        term = search_term.lower()
        return [
            t for t in self._taxonomies.values()
            if term in t.name.lower() or term in t.regulation.lower()
        ]

    def get_financial_taxonomies(self) -> List[TaxonomyInfo]:
        """Get all Regulation 33 Financial Results taxonomies."""
        return [t for t in self._taxonomies.values() if "financial results" in t.name.lower()]

    def get_corporate_governance_taxonomy(self) -> Optional[TaxonomyInfo]:
        """Get Regulation 27(2) Corporate Governance taxonomy."""
        matches = self.find_by_name("Corporate Governance")
        return matches[0] if matches else None

    def get_shareholding_pattern_taxonomy(self) -> Optional[TaxonomyInfo]:
        """Get Regulation 31 Shareholding Pattern taxonomy."""
        matches = self.find_by_name("Shareholding Pattern")
        return matches[0] if matches else None
