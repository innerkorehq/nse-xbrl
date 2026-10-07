"""
nse_xbrl_parser.core.models

Universal XBRL fact, instance, and metadata models.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

from .context import XBRLContext
from .unit import XBRLUnit


class XBRLFact(BaseModel):
    """Represents a single parsed XBRL Fact."""

    tag: str
    namespace: str = ""
    prefix: str = ""
    context_ref: str
    unit_ref: Optional[str] = None
    decimals: Optional[str] = None
    scale: Optional[int] = None
    raw_value: str
    value: Union[float, int, bool, str, None] = None

    @property
    def local_name(self) -> str:
        """Return the tag name without any prefix or namespace."""
        if ":" in self.tag:
            return self.tag.split(":", 1)[1]
        return self.tag

    @property
    def is_numeric(self) -> bool:
        return isinstance(self.value, (int, float))

    @property
    def as_float(self) -> Optional[float]:
        if isinstance(self.value, (int, float)):
            return float(self.value)
        try:
            return float(self.raw_value.replace(",", "").strip())
        except (ValueError, TypeError, AttributeError):
            return None


class XBRLInstance(BaseModel):
    """Universal model representing a parsed XBRL instance document."""

    source: Optional[str] = None
    target_namespaces: Dict[str, str] = Field(default_factory=dict)
    schema_refs: List[str] = Field(default_factory=list)
    contexts: Dict[str, XBRLContext] = Field(default_factory=dict)
    units: Dict[str, XBRLUnit] = Field(default_factory=dict)
    facts: List[XBRLFact] = Field(default_factory=list)

    # Fast lookup cache: tag_lower -> list of facts
    _fact_map: Dict[str, List[XBRLFact]] = {}

    def model_post_init(self, __context: Any) -> None:
        self._build_index()

    def _build_index(self) -> None:
        index: Dict[str, List[XBRLFact]] = {}
        for f in self.facts:
            name_lower = f.local_name.lower()
            if name_lower not in index:
                index[name_lower] = []
            index[name_lower].append(f)
        self._fact_map = index

    def get_facts_by_tag(self, tag_name: str) -> List[XBRLFact]:
        """Lookup facts by case-insensitive tag name (e.g. 'RevenueFromOperations' or 'ScripCode')."""
        return self._fact_map.get(tag_name.lower(), [])

    def get_fact_value(
        self,
        tag_name: str,
        context_ref: Optional[str] = None,
        default: Any = None,
    ) -> Any:
        """Get parsed value for a tag. If context_ref is specified, returns match for that context."""
        matching = self.get_facts_by_tag(tag_name)
        if not matching:
            return default
        if context_ref:
            for f in matching:
                if f.context_ref == context_ref:
                    return f.value
            return default
        return matching[0].value

    def get_fact_float(
        self,
        tag_name: str,
        context_ref: Optional[str] = None,
        default: Optional[float] = None,
    ) -> Optional[float]:
        """Get numeric float value for a tag."""
        val = self.get_fact_value(tag_name, context_ref=context_ref)
        if val is None:
            return default
        if isinstance(val, (int, float)):
            return float(val)
        try:
            return float(str(val).replace(",", "").strip())
        except (ValueError, TypeError):
            return default

    def get_entity_id(self) -> Optional[str]:
        """Extract first available entity identifier (e.g. Scrip code or CIN)."""
        for ctx in self.contexts.values():
            if ctx.entity_id:
                return ctx.entity_id
        return None

    def search_facts(self, regex_pattern: str) -> List[XBRLFact]:
        """Search all facts whose local tag matches a regular expression."""
        pattern = re.compile(regex_pattern, re.IGNORECASE)
        return [f for f in self.facts if pattern.search(f.local_name)]

    def to_dict(self) -> Dict[str, Any]:
        """Convert facts into flat dictionary of tag -> value for simple context."""
        out: Dict[str, Any] = {}
        for f in self.facts:
            key = f"{f.local_name}@{f.context_ref}"
            out[key] = f.value
        return out
