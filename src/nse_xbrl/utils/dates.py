"""
nse_xbrl.utils.dates

Date and quarter parsing helpers.
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from dateutil import parser as dateutil_parser


def parse_date(value: str | date | datetime | None) -> Optional[date]:
    """Parse date string into a standard datetime.date object."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        return None
    
    val_str = value.strip()
    if not val_str:
        return None
    
    try:
        # Common ISO format YYYY-MM-DD
        if len(val_str) == 10 and val_str[4] == "-" and val_str[7] == "-":
            return date.fromisoformat(val_str)
        return dateutil_parser.parse(val_str).date()
    except Exception:
        return None
