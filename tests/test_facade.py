import pytest
from pathlib import Path

from nse_xbrl_parser import (
    parse,
    parse_sync,
    XBRL,
    FilingFormat,
    FinancialResultsModel,
    ShareholdingPatternModel,
    CorporateGovernanceModel,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.mark.asyncio
async def test_facade_auto_detect_financials_async():
    file_path = FIXTURES_DIR / "sample_financial_results.xml"
    filing = await parse(file_path)

    assert filing.format == FilingFormat.FINANCIAL_RESULTS
    assert isinstance(filing.data, FinancialResultsModel)
    assert filing.company_name == "RELIANCE INDUSTRIES LIMITED"
    assert filing.scrip_code == "500325"
    assert filing.symbol == "RELIANCE"

    # Direct access through .data or typed property
    assert filing.data.revenue_from_operations == 23548100000.0
    assert filing.financial_results.revenue_from_operations == 23548100000.0
    assert filing.financial_results.profit_after_tax == 1942100000.0


@pytest.mark.asyncio
async def test_facade_auto_detect_shp_async():
    file_path = FIXTURES_DIR / "sample_shareholding.xml"
    filing = await parse(file_path)

    assert filing.format == FilingFormat.SHAREHOLDING_PATTERN
    assert isinstance(filing.data, ShareholdingPatternModel)
    assert filing.company_name == "TATA CONSULTANCY SERVICES LIMITED"
    assert filing.scrip_code == "532540"
    assert filing.symbol == "TCS"
    assert filing.data.promoter_holding_percentage == 71.77
    assert filing.shareholding_pattern.public_holding_percentage == 28.23


def test_facade_auto_detect_corporate_governance_sync():
    file_path = FIXTURES_DIR / "sample_corporate_governance.xml"
    filing = parse_sync(file_path)

    assert filing.format == FilingFormat.CORPORATE_GOVERNANCE
    assert isinstance(filing.data, CorporateGovernanceModel)
    assert filing.company_name == "INFOSYS LIMITED"
    assert filing.scrip_code == "500209"
    assert filing.symbol == "INFY"
    assert filing.data.has_risk_management_committee is True


def test_facade_parse_raw_xml_string():
    xml_str = """<?xml version="1.0" encoding="UTF-8"?>
    <xbrl xmlns="http://www.xbrl.org/2003/instance"
          xmlns:xbrli="http://www.xbrl.org/2003/instance"
          xmlns:in-bse-cg="http://www.bseindia.com/xbrl/cg/2024-03-31/in-bse-cg">
      <xbrli:context id="C1">
        <xbrli:entity><xbrli:identifier scheme="http://www.bseindia.com">500001</xbrli:identifier></xbrli:entity>
        <xbrli:period><xbrli:instant>2025-12-31</xbrli:instant></xbrli:period>
      </xbrli:context>
      <in-bse-cg:NameOfTheCompany contextRef="C1">TEST COMPANY</in-bse-cg:NameOfTheCompany>
      <in-bse-cg:RiskManagementCommittee contextRef="C1">false</in-bse-cg:RiskManagementCommittee>
    </xbrl>
    """
    filing = XBRL.parse_sync(xml_str)
    assert filing.format == FilingFormat.CORPORATE_GOVERNANCE
    assert filing.company_name == "TEST COMPANY"
    assert filing.corporate_governance.has_risk_management_committee is False


def test_facade_to_dict():
    file_path = FIXTURES_DIR / "sample_financial_results.xml"
    filing = parse_sync(file_path)
    d = filing.to_dict()
    assert isinstance(d, dict)
    assert d.get("company_name") == "RELIANCE INDUSTRIES LIMITED"
    assert d.get("revenue_from_operations") == 23548100000.0
