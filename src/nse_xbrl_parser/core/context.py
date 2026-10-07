"""
nse_xbrl_parser.core.context

XBRL Context representation (entity, period, and dimensions).
"""
from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

from ..utils.dates import parse_date


class PeriodType(str, Enum):
    INSTANT = "instant"
    DURATION = "duration"
    FOREVER = "forever"


class ExplicitMember(BaseModel):
    """Represents a dimensional explicit member axis/member pair."""
    dimension: str
    member: str


class XBRLContext(BaseModel):
    """Represents an XBRL context element."""

    context_id: str
    entity_id: str = ""
    entity_scheme: str = ""
    period_type: PeriodType = PeriodType.DURATION
    instant: Optional[date] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    dimensions: Dict[str, str] = Field(default_factory=dict)
    scenario_dimensions: Dict[str, str] = Field(default_factory=dict)

    @property
    def is_instant(self) -> bool:
        return self.period_type == PeriodType.INSTANT

    @property
    def is_duration(self) -> bool:
        return self.period_type == PeriodType.DURATION

    @property
    def is_standalone(self) -> bool:
        """Check if context explicitly targets Standalone filing."""
        for dim, member in self.dimensions.items():
            if "standalone" in member.lower() or "standalone" in dim.lower():
                return True
        return False

    @property
    def is_consolidated(self) -> bool:
        """Check if context explicitly targets Consolidated filing."""
        for dim, member in self.dimensions.items():
            if "consolidated" in member.lower() or "consolidated" in dim.lower():
                return True
        return False
