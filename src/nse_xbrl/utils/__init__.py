"""
nse_xbrl.utils

Utility modules for XML and date handling.
"""
from __future__ import annotations

from .dates import parse_date
from .xml_utils import clean_xml_bytes, get_namespace, parse_xml_tree, strip_namespace

__all__ = [
    "parse_date",
    "clean_xml_bytes",
    "get_namespace",
    "parse_xml_tree",
    "strip_namespace",
]
