"""
nse_xbrl_parser.taxonomy.schema

XSD Taxonomy Schema Parser (elements, types, substitution groups, period types).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from lxml import etree
from pydantic import BaseModel, Field

from ..utils.xml_utils import clean_xml_bytes, get_namespace, parse_xml_tree, strip_namespace

XSD_NS = "http://www.w3.org/2001/XMLSchema"
XBRLI_NS = "http://www.xbrl.org/2003/instance"


class SchemaElement(BaseModel):
    """Represents a concept element declared in an XBRL taxonomy schema (.xsd)."""

    name: str
    id: Optional[str] = None
    type: Optional[str] = None
    substitution_group: Optional[str] = None
    period_type: Optional[str] = None
    balance: Optional[str] = None
    is_abstract: bool = False
    is_nillable: bool = True
    target_namespace: Optional[str] = None

    @property
    def is_monetary(self) -> bool:
        return self.type is not None and "monetaryItemType" in self.type

    @property
    def is_shares(self) -> bool:
        return self.type is not None and "sharesItemType" in self.type


class TaxonomySchema(BaseModel):
    """Container for parsed taxonomy schemas."""

    target_namespace: str = ""
    elements: Dict[str, SchemaElement] = Field(default_factory=dict)

    @classmethod
    def from_xsd_content(cls, content: bytes | str) -> TaxonomySchema:
        """Parse an XSD file into a TaxonomySchema model."""
        root = parse_xml_tree(content)
        tns = root.attrib.get("targetNamespace", "")
        elements: Dict[str, SchemaElement] = {}

        for elem in root.xpath("//xsd:element", namespaces={"xsd": XSD_NS}):
            name = elem.attrib.get("name")
            if not name:
                continue

            elem_id = elem.attrib.get("id")
            elem_type = elem.attrib.get("type")
            subst = elem.attrib.get("substitutionGroup")
            period = elem.attrib.get(f"{{{XBRLI_NS}}}periodType") or elem.attrib.get("periodType")
            balance = elem.attrib.get(f"{{{XBRLI_NS}}}balance") or elem.attrib.get("balance")
            is_abstract = elem.attrib.get("abstract", "false").lower() == "true"
            is_nillable = elem.attrib.get("nillable", "true").lower() == "true"

            schema_elem = SchemaElement(
                name=name,
                id=elem_id,
                type=elem_type,
                substitution_group=subst,
                period_type=period,
                balance=balance,
                is_abstract=is_abstract,
                is_nillable=is_nillable,
                target_namespace=tns,
            )
            elements[name] = schema_elem

        return cls(target_namespace=tns, elements=elements)
