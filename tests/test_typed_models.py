import pytest
from pathlib import Path

from nse_xbrl_parser import (
    parse_file,
    FinancialResultsModel,
    ShareholdingPatternModel,
    CorporateGovernanceModel,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.mark.asyncio
async def test_financial_results_model():
    file_path = FIXTURES_DIR / "sample_financial_results.xml"
    instance = await parse_file(file_path)
    model = FinancialResultsModel.from_instance(instance)

    assert model.company_name == "RELIANCE INDUSTRIES LIMITED"
    assert model.scrip_code == "500325"
    assert model.symbol == "RELIANCE"
    assert model.nature_of_report == "Consolidated"
    assert model.reporting_quarter == "Third Quarter"

    # Line items
    assert model.revenue_from_operations == 23548100000.0
    assert model.other_income == 384000000.0
    assert model.total_income == 23932100000.0
    assert model.profit_before_tax == 2832100000.0
    assert model.profit_after_tax == 1942100000.0
    assert model.basic_eps == 28.72

    # EBITDA computed
    assert model.ebitda is not None
    assert model.ebitda > model.profit_before_tax


@pytest.mark.asyncio
async def test_shareholding_pattern_model():
    file_path = FIXTURES_DIR / "sample_shareholding.xml"
    instance = await parse_file(file_path)
    model = ShareholdingPatternModel.from_instance(instance)

    assert model.company_name == "TATA CONSULTANCY SERVICES LIMITED"
    assert model.scrip_code == "532540"
    assert model.symbol == "TCS"
    assert model.promoter_holding_percentage == 71.77
    assert model.public_holding_percentage == 28.23
    assert model.promoter_shares_pledged_percentage == 0.0


@pytest.mark.asyncio
async def test_corporate_governance_model():
    file_path = FIXTURES_DIR / "sample_corporate_governance.xml"
    instance = await parse_file(file_path)
    model = CorporateGovernanceModel.from_instance(instance)

    assert model.company_name == "INFOSYS LIMITED"
    assert model.scrip_code == "500209"
    assert model.symbol == "INFY"
    assert model.reporting_quarter == "Third Quarter"
    assert model.has_risk_management_committee is True
