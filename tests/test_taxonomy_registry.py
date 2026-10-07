import pytest
from nse_xbrl import TaxonomyRegistry, TaxonomyInfo


def test_taxonomy_registry_count():
    registry = TaxonomyRegistry()
    assert registry.count() == 58


def test_taxonomy_registry_all():
    registry = TaxonomyRegistry()
    all_tax = registry.get_all()
    assert len(all_tax) == 58
    assert all_tax[0].id == 1
    assert all_tax[-1].id == 58


def test_find_taxonomies_by_name():
    registry = TaxonomyRegistry()
    
    # Financial results
    fin = registry.get_financial_taxonomies()
    assert len(fin) >= 6

    # Shareholding
    shp = registry.get_shareholding_pattern_taxonomy()
    assert shp is not None
    assert "Shareholding Pattern" in shp.name
    assert shp.primary_taxonomy_url is not None

    # Corporate Governance
    cg = registry.get_corporate_governance_taxonomy()
    assert cg is not None
    assert "Corporate Governance" in cg.name
    assert cg.primary_taxonomy_url is not None


def test_taxonomy_links_validity():
    registry = TaxonomyRegistry()
    for tax in registry.get_all():
        assert tax.name
        assert tax.id >= 1
        assert len(tax.all_links) > 0
        assert tax.primary_taxonomy_url.startswith("http")
