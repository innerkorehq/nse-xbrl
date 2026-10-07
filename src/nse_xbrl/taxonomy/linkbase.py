"""
nse_xbrl.taxonomy.linkbase

XBRL Linkbase Parsers:
- Label Linkbase (*-lab.xml): human readable labels for concepts
- Presentation Linkbase (*-pre.xml): UI tree and hierarchy
- Calculation Linkbase (*-cal.xml): summation-item relationships
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from lxml import etree
from pydantic import BaseModel, Field

from ..utils.xml_utils import clean_xml_bytes, parse_xml_tree, strip_namespace

LINKBASE_NS = "http://www.xbrl.org/2003/linkbase"
XLINK_NS = "http://www.w3.org/1999/xlink"


class ConceptLabel(BaseModel):
    """Represents a human-readable concept label from a label linkbase."""

    concept_id: str
    label_role: str = "http://www.xbrl.org/2003/role/label"
    lang: str = "en"
    text: str


class CalculationArc(BaseModel):
    """Represents a parent-child calculation relationship."""

    parent: str
    child: str
    weight: float = 1.0
    order: Optional[float] = None


class TaxonomyLinkbase(BaseModel):
    """Container for parsed linkbase data."""

    labels: Dict[str, str] = Field(default_factory=dict)  # concept_name -> English label text
    calculations: List[CalculationArc] = Field(default_factory=list)

    @classmethod
    def from_label_xml(cls, content: bytes | str) -> TaxonomyLinkbase:
        """Parse a label linkbase file (*-lab.xml, *-label.xml)."""
        root = parse_xml_tree(content)
        labels: Dict[str, str] = {}

        # 1. Map locators (loc: label -> concept)
        loc_map: Dict[str, str] = {}
        for loc in root.xpath(
            "//*[local-name()='loc']",
            namespaces={"link": LINKBASE_NS, "xlink": XLINK_NS},
        ):
            loc_label = loc.attrib.get(f"{{{XLINK_NS}}}label") or loc.attrib.get("label")
            loc_href = loc.attrib.get(f"{{{XLINK_NS}}}href") or loc.attrib.get("href")
            if loc_label and loc_href:
                # href typically looks like 'in-capmkt.xsd#in-capmkt_ScripCode'
                concept_name = loc_href.split("#")[-1]
                # strip standard prefixes
                concept_clean = concept_name.split("_")[-1]
                loc_map[loc_label] = concept_clean

        # 2. Map label arcs (labelArc: from loc to label resource)
        arc_map: Dict[str, str] = {}
        for arc in root.xpath(
            "//*[local-name()='labelArc']",
            namespaces={"link": LINKBASE_NS, "xlink": XLINK_NS},
        ):
            arc_from = arc.attrib.get(f"{{{XLINK_NS}}}from") or arc.attrib.get("from")
            arc_to = arc.attrib.get(f"{{{XLINK_NS}}}to") or arc.attrib.get("to")
            if arc_from and arc_to:
                arc_map[arc_to] = arc_from

        # 3. Read label text
        for lbl in root.xpath(
            "//*[local-name()='label']",
            namespaces={"link": LINKBASE_NS, "xlink": XLINK_NS},
        ):
            lbl_key = lbl.attrib.get(f"{{{XLINK_NS}}}label") or lbl.attrib.get("label")
            text = (lbl.text or "").strip()
            if not text or not lbl_key:
                continue

            # Determine concept name
            loc_label = arc_map.get(lbl_key, lbl_key)
            concept_name = loc_map.get(loc_label)
            if not concept_name:
                # Direct label heuristic (e.g. label_ScripCode -> ScripCode)
                if lbl_key.startswith("label_"):
                    concept_name = lbl_key[len("label_") :]
                else:
                    concept_name = lbl_key

            labels[concept_name] = text

        return cls(labels=labels)

    def get_label(self, concept_name: str, default: Optional[str] = None) -> str:
        """Get the human-readable label for a concept name."""
        clean = strip_namespace(concept_name)
        return self.labels.get(clean, default or clean)
