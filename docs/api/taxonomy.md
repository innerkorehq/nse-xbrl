# Taxonomy API Reference

Taxonomy registry and metadata loader in `nse_xbrl.taxonomy`.

## TaxonomyRegistry

::: nse_xbrl.taxonomy.registry.TaxonomyRegistry
    options:
      members:
        - count
        - get_all
        - get_by_id
        - find_by_name
        - get_financial_taxonomies
        - get_shareholding_pattern_taxonomy
        - get_corporate_governance_taxonomy

::: nse_xbrl.taxonomy.registry.TaxonomyInfo

## Downloader & Linkbase

::: nse_xbrl.taxonomy.downloader.AsyncTaxonomyDownloader
    options:
      members:
        - download_taxonomy_archive
        - load_taxonomy_metadata

::: nse_xbrl.taxonomy.linkbase.TaxonomyLinkbase
    options:
      members:
        - get_label

::: nse_xbrl.taxonomy.schema.TaxonomySchema
