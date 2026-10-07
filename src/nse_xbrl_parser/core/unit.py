"""
nse_xbrl_parser.core.unit

XBRL Unit representations (monetary currencies, shares, pure numbers).
"""
from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class XBRLUnit(BaseModel):
    """Represents an XBRL unit element (e.g. INR, Shares, Pure)."""

    unit_id: str
    measure: str
    measure_namespace: Optional[str] = None
    divide_numerator: Optional[str] = None
    divide_denominator: Optional[str] = None

    @property
    def is_currency(self) -> bool:
        """Return True if unit represents a currency (e.g. INR, USD)."""
        m = self.measure.upper()
        return m in {"INR", "USD", "EUR", "GBP", "JPY"}

    @property
    def is_shares(self) -> bool:
        """Return True if unit represents shares."""
        return "shares" in self.measure.lower()

    @property
    def is_ratio(self) -> bool:
        """Return True if unit is a dimensionless ratio/percentage."""
        return self.measure.lower() in {"pure", "ratio"}
