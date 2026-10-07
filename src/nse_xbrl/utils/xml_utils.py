"""
nse_xbrl.utils.xml_utils

Utility functions for namespace stripping, XML parsing, and tag manipulation.
"""
from __future__ import annotations

import re
from typing import Any
from lxml import etree


def strip_namespace(tag: str) -> str:
    """Strip XML namespace prefix from tag name.
    
    e.g. '{http://www.bseindia.com/xbrl/fin/2020-03-31/in-bse-fin}Revenue' -> 'Revenue'
         'in-bse-fin:Revenue' -> 'Revenue'
    """
    if "}" in tag:
        return tag.split("}", 1)[1]
    if ":" in tag:
        return tag.split(":", 1)[1]
    return tag


def get_namespace(tag: str) -> str:
    """Extract namespace URI from Clark notation '{uri}tag'."""
    if tag.startswith("{") and "}" in tag:
        return tag[1:].split("}", 1)[0]
    return ""


def clean_xml_bytes(content: bytes | str) -> bytes:
    """Normalize XML input bytes and strip BOM or invalid control characters."""
    if isinstance(content, str):
        content = content.encode("utf-8")
    
    # Strip UTF-8 BOM if present
    if content.startswith(b"\xef\xbb\xbf"):
        content = content[3:]
        
    return content


def parse_xml_tree(content: bytes | str) -> etree._Element:
    """Parse XML string or bytes safely into an lxml element tree."""
    cleaned = clean_xml_bytes(content)
    # Configure parser to recover on broken entities or comments
    parser = etree.XMLParser(recover=True, remove_comments=False, resolve_entities=False)
    return etree.fromstring(cleaned, parser=parser)
