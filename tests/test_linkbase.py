import pytest
from nse_xbrl_parser import (
    TaxonomySchema,
    TaxonomyLinkbase,
)

SAMPLE_XSD = b"""<?xml version="1.0" encoding="UTF-8"?>
<xsd:schema targetNamespace="https://www.sebi.gov.in/xbrl/2024-05-31/in-capmkt"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema"
            xmlns:xbrli="http://www.xbrl.org/2003/instance">
  <xsd:element name="RevenueFromOperations" id="in-capmkt_RevenueFromOperations"
               type="xbrli:monetaryItemType" substitutionGroup="xbrli:item"
               xbrli:periodType="duration" xbrli:balance="credit"/>
  <xsd:element name="ScripCode" id="in-capmkt_ScripCode"
               type="xbrli:stringItemType" substitutionGroup="xbrli:item"
               xbrli:periodType="instant"/>
</xsd:schema>
"""

SAMPLE_LABEL_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<link:linkbase xmlns:link="http://www.xbrl.org/2003/linkbase"
               xmlns:xlink="http://www.w3.org/1999/xlink">
  <link:labelLink xlink:type="extended" xlink:role="http://www.xbrl.org/2003/role/link">
    <link:loc xlink:type="locator" xlink:href="in-capmkt.xsd#in-capmkt_RevenueFromOperations" xlink:label="loc_rev"/>
    <link:labelArc xlink:type="arc" xlink:from="loc_rev" xlink:to="lbl_rev" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
    <link:label xlink:type="resource" xlink:label="lbl_rev" xml:lang="en">Revenue from operations</link:label>

    <link:loc xlink:type="locator" xlink:href="in-capmkt.xsd#in-capmkt_ScripCode" xlink:label="loc_scrip"/>
    <link:labelArc xlink:type="arc" xlink:from="loc_scrip" xlink:to="lbl_scrip" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label"/>
    <link:label xlink:type="resource" xlink:label="lbl_scrip" xml:lang="en">Scrip Code</link:label>
  </link:labelLink>
</link:linkbase>
"""


def test_taxonomy_schema_parsing():
    schema = TaxonomySchema.from_xsd_content(SAMPLE_XSD)
    assert schema.target_namespace == "https://www.sebi.gov.in/xbrl/2024-05-31/in-capmkt"
    assert "RevenueFromOperations" in schema.elements
    assert "ScripCode" in schema.elements

    rev = schema.elements["RevenueFromOperations"]
    assert rev.period_type == "duration"
    assert rev.balance == "credit"
    assert rev.is_monetary is True

    scrip = schema.elements["ScripCode"]
    assert scrip.period_type == "instant"
    assert scrip.is_monetary is False


def test_taxonomy_label_linkbase_parsing():
    linkbase = TaxonomyLinkbase.from_label_xml(SAMPLE_LABEL_XML)
    assert linkbase.get_label("RevenueFromOperations") == "Revenue from operations"
    assert linkbase.get_label("ScripCode") == "Scrip Code"
    assert linkbase.get_label("UnknownTag", default="Unknown") == "Unknown"
