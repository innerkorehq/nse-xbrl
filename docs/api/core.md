# Core API Reference

Universal models and parsing engine in `nse_xbrl.core`.

## Functions

::: nse_xbrl.core.parser.AsyncXBRLParser
    options:
      members:
        - parse
        - parse_file
        - parse_zip
        - parse_sync

::: nse_xbrl.parse_xbrl

::: nse_xbrl.parse_file

::: nse_xbrl.parse_archive

::: nse_xbrl.parse_xbrl_sync

## Models

::: nse_xbrl.core.models.XBRLInstance
    options:
      members:
        - get_facts_by_tag
        - get_fact_value
        - get_fact_float
        - search_facts
        - to_dict

::: nse_xbrl.core.models.XBRLFact

::: nse_xbrl.core.context.XBRLContext

::: nse_xbrl.core.unit.XBRLUnit
