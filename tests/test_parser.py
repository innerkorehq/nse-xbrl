import pytest
from pathlib import Path

from nse_xbrl_parser import (
    parse_file,
    parse_xbrl,
    parse_xbrl_sync,
    XBRLInstance,
    PeriodType,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.mark.asyncio
async def test_parse_financial_results_async():
    file_path = FIXTURES_DIR / "sample_financial_results.xml"
    instance = await parse_file(file_path)

    assert isinstance(instance, XBRLInstance)
    assert len(instance.facts) > 10
    assert "OneD" in instance.contexts
    assert "OneI" in instance.contexts
    assert "INR" in instance.units

    # Check context
    ctx_1d = instance.contexts["OneD"]
    assert ctx_1d.period_type == PeriodType.DURATION
    assert str(ctx_1d.start_date) == "2025-10-01"
    assert str(ctx_1d.end_date) == "2025-12-31"

    # Check facts extraction
    scrip = instance.get_fact_value("ScripCode")
    assert str(scrip) == "500325"
    assert instance.get_fact_value("NSESymbol") == "RELIANCE"
    assert instance.get_fact_value("NameOfTheCompany") == "RELIANCE INDUSTRIES LIMITED"

    # Numeric facts
    rev = instance.get_fact_float("RevenueFromOperations")
    assert rev == 23548100000.0

    eps = instance.get_fact_float("BasicEarningsLossPerShare")
    assert eps == 28.72


def test_parse_financial_results_sync():
    file_path = FIXTURES_DIR / "sample_financial_results.xml"
    content = file_path.read_bytes()
    instance = parse_xbrl_sync(content)

    assert len(instance.facts) > 10
    assert instance.get_fact_value("ISIN") == "INE002A01018"


@pytest.mark.asyncio
async def test_search_facts_regex():
    file_path = FIXTURES_DIR / "sample_financial_results.xml"
    instance = await parse_file(file_path)

    # Search for all income tags
    income_facts = instance.search_facts("income|revenue")
    assert len(income_facts) >= 2
    tags = [f.local_name for f in income_facts]
    assert "RevenueFromOperations" in tags
    assert "OtherIncome" in tags
