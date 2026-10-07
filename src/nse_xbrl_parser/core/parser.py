"""
nse_xbrl_parser.core.parser

Asynchronous and synchronous universal XBRL 2.1 parser for NSE and BSE filings.
"""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import zipfile
import io

from lxml import etree

from .context import PeriodType, XBRLContext
from .models import XBRLFact, XBRLInstance
from .unit import XBRLUnit
from ..utils.dates import parse_date
from ..utils.xml_utils import clean_xml_bytes, get_namespace, parse_xml_tree, strip_namespace

XBRLI_NS = "http://www.xbrl.org/2003/instance"
LINKBASE_NS = "http://www.xbrl.org/2003/linkbase"
XLINK_NS = "http://www.w3.org/1999/xlink"
XBRLDI_NS = "http://xbrl.org/2006/xbrldi"


class AsyncXBRLParser:
    """High-performance parser for XBRL instance documents."""

    def __init__(self) -> None:
        pass

    async def parse(
        self,
        content: Union[str, bytes],
        source_name: Optional[str] = None,
    ) -> XBRLInstance:
        """Parse XML string or bytes asynchronously without blocking the event loop."""
        # Run parsing in executor for heavy XML trees
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            self.parse_sync,
            content,
            source_name,
        )

    async def parse_file(self, file_path: Union[str, Path]) -> XBRLInstance:
        """Parse a local XML file asynchronously."""
        path = Path(file_path)
        content = await asyncio.to_thread(path.read_bytes)
        return await self.parse(content, source_name=str(path))

    async def parse_zip(self, zip_content: bytes) -> List[XBRLInstance]:
        """Parse all XBRL XML files contained in a ZIP archive."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._parse_zip_sync, zip_content)

    def _parse_zip_sync(self, zip_content: bytes) -> List[XBRLInstance]:
        results: List[XBRLInstance] = []
        with zipfile.ZipFile(io.BytesIO(zip_content)) as z:
            for name in z.namelist():
                if name.endswith((".xml", ".xbrl")) and not any(
                    x in name.lower()
                    for x in ["_cal", "_pre", "_def", "_lab", "catalog.xml", "types.xsd"]
                ):
                    try:
                        data = z.read(name)
                        tree = parse_xml_tree(data)
                        # Check if it has an xbrl root or context elements
                        local_root = strip_namespace(tree.tag).lower()
                        if local_root == "xbrl" or tree.xpath("//*[local-name()='context']"):
                            parsed = self.parse_sync(data, source_name=name)
                            results.append(parsed)
                    except Exception:
                        continue
        return results

    def parse_sync(
        self,
        content: Union[str, bytes],
        source_name: Optional[str] = None,
    ) -> XBRLInstance:
        """Parse XML synchronously into an XBRLInstance."""
        root = parse_xml_tree(content)

        # Collect target namespaces & schema references
        namespaces = {k: v for k, v in root.nsmap.items() if k is not None}
        schema_refs: List[str] = []
        for ref in root.xpath(
            "//*[local-name()='schemaRef']",
            namespaces={"link": LINKBASE_NS, "xlink": XLINK_NS},
        ):
            href = ref.attrib.get(f"{{{XLINK_NS}}}href") or ref.attrib.get("href")
            if href:
                schema_refs.append(href)

        # 1. Parse Contexts
        contexts = self._parse_contexts(root)

        # 2. Parse Units
        units = self._parse_units(root)

        # 3. Parse Facts
        facts = self._parse_facts(root, contexts, units)

        instance = XBRLInstance(
            source=source_name,
            target_namespaces=namespaces,
            schema_refs=schema_refs,
            contexts=contexts,
            units=units,
            facts=facts,
        )
        return instance

    def _parse_contexts(self, root: etree._Element) -> Dict[str, XBRLContext]:
        contexts: Dict[str, XBRLContext] = {}
        for elem in root.xpath("//*[local-name()='context']"):
            context_id = elem.attrib.get("id")
            if not context_id:
                continue

            entity_id = ""
            entity_scheme = ""
            ident_elem = elem.xpath(".//*[local-name()='identifier']")
            if ident_elem:
                entity_id = (ident_elem[0].text or "").strip()
                entity_scheme = ident_elem[0].attrib.get("scheme", "")

            # Period
            period_type = PeriodType.DURATION
            instant_date = None
            start_date = None
            end_date = None

            instant_elem = elem.xpath(".//*[local-name()='instant']")
            if instant_elem and instant_elem[0].text:
                period_type = PeriodType.INSTANT
                instant_date = parse_date(instant_elem[0].text.strip())
            else:
                start_elem = elem.xpath(".//*[local-name()='startDate']")
                end_elem = elem.xpath(".//*[local-name()='endDate']")
                if start_elem and start_elem[0].text:
                    start_date = parse_date(start_elem[0].text.strip())
                if end_elem and end_elem[0].text:
                    end_date = parse_date(end_elem[0].text.strip())

            # Dimensions (explicitMember)
            dimensions: Dict[str, str] = {}
            for member in elem.xpath(".//*[local-name()='explicitMember']"):
                dim_attr = member.attrib.get("dimension", "")
                member_val = (member.text or "").strip()
                dimensions[strip_namespace(dim_attr)] = strip_namespace(member_val)

            contexts[context_id] = XBRLContext(
                context_id=context_id,
                entity_id=entity_id,
                entity_scheme=entity_scheme,
                period_type=period_type,
                instant=instant_date,
                start_date=start_date,
                end_date=end_date,
                dimensions=dimensions,
            )
        return contexts

    def _parse_units(self, root: etree._Element) -> Dict[str, XBRLUnit]:
        units: Dict[str, XBRLUnit] = {}
        for elem in root.xpath("//*[local-name()='unit']"):
            unit_id = elem.attrib.get("id")
            if not unit_id:
                continue

            measure = ""
            measure_elem = elem.xpath(".//*[local-name()='measure']")
            if measure_elem and measure_elem[0].text:
                measure = strip_namespace(measure_elem[0].text.strip())

            div_num = None
            div_den = None
            num_elem = elem.xpath(".//*[local-name()='unitNumerator']//*[local-name()='measure']")
            den_elem = elem.xpath(".//*[local-name()='unitDenominator']//*[local-name()='measure']")
            if num_elem and num_elem[0].text:
                div_num = strip_namespace(num_elem[0].text.strip())
            if den_elem and den_elem[0].text:
                div_den = strip_namespace(den_elem[0].text.strip())

            units[unit_id] = XBRLUnit(
                unit_id=unit_id,
                measure=measure or (div_num or ""),
                divide_numerator=div_num,
                divide_denominator=div_den,
            )
        return units

    def _parse_facts(
        self,
        root: etree._Element,
        contexts: Dict[str, XBRLContext],
        units: Dict[str, XBRLUnit],
    ) -> List[XBRLFact]:
        facts: List[XBRLFact] = []

        # Find elements that have contextRef attribute
        for elem in root.xpath("//*[@contextRef]"):
            context_ref = elem.attrib.get("contextRef", "")
            unit_ref = elem.attrib.get("unitRef")
            decimals = elem.attrib.get("decimals")
            scale = elem.attrib.get("scale")
            scale_int = int(scale) if scale and scale.isdigit() else None

            # Get text or inner HTML
            raw_text = (elem.text or "").strip()
            if not raw_text and len(elem) > 0:
                raw_text = "".join(etree.tostring(child, encoding="unicode") for child in elem)

            # Determine typed value
            val = self._coerce_value(raw_text, unit_ref, decimals)

            tag_clark = elem.tag
            local_name = strip_namespace(tag_clark)
            ns = get_namespace(tag_clark)
            prefix = elem.prefix or ""

            facts.append(
                XBRLFact(
                    tag=local_name,
                    namespace=ns,
                    prefix=prefix,
                    context_ref=context_ref,
                    unit_ref=unit_ref,
                    decimals=decimals,
                    scale=scale_int,
                    raw_value=raw_text,
                    value=val,
                )
            )
        return facts

    def _coerce_value(
        self,
        raw_text: str,
        unit_ref: Optional[str],
        decimals: Optional[str],
    ) -> Union[float, int, bool, str, None]:
        if not raw_text:
            return None

        # Check boolean
        if raw_text.lower() in {"true", "false"}:
            return raw_text.lower() == "true"

        # Check numeric if unitRef or decimals is present, or if it matches number pattern
        clean = raw_text.replace(",", "").strip()
        try:
            if "." in clean:
                return float(clean)
            return int(clean)
        except ValueError:
            pass

        return raw_text
