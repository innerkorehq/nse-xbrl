import pytest
from nse_xbrl import (
    TaxonomyRegistry,
    AsyncTaxonomyDownloader,
)


@pytest.mark.asyncio
async def test_live_download_investor_complaints_metadata():
    registry = TaxonomyRegistry()
    downloader = AsyncTaxonomyDownloader()

    tax1 = registry.get_by_id(1)
    assert tax1 is not None

    schema, linkbase = await downloader.load_taxonomy_metadata(tax1)
    assert schema is not None
    assert len(schema.elements) > 100
    assert "ScripCode" in schema.elements

    assert linkbase is not None
    assert len(linkbase.labels) > 100
    assert linkbase.get_label("ScripCode") == "Scrip Code"


@pytest.mark.asyncio
async def test_live_download_financial_results_metadata():
    registry = TaxonomyRegistry()
    downloader = AsyncTaxonomyDownloader()

    tax6 = registry.get_by_id(6)
    assert tax6 is not None

    schema, linkbase = await downloader.load_taxonomy_metadata(tax6)
    assert schema is not None
    assert "RevenueFromOperations" in schema.elements

    assert linkbase is not None
    assert linkbase.get_label("RevenueFromOperations") == "Revenue from operations"
