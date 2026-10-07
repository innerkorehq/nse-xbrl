# Facade API Reference

Super-simple unified facade for automatically detecting and parsing any NSE or BSE XBRL filing.

## Auto-Detecting Functions

```{eval-rst}
.. autofunction:: nse_xbrl_parser.parse

.. autofunction:: nse_xbrl_parser.parse_sync
```

## Unified Facade Class

```{eval-rst}
.. autoclass:: nse_xbrl_parser.XBRL
   :members:
   :show-inheritance:
```

## Filing Results & Formats

```{eval-rst}
.. autoclass:: nse_xbrl_parser.ParsedFiling
   :members:
   :show-inheritance:

.. autoclass:: nse_xbrl_parser.FilingFormat
   :members:
   :show-inheritance:

.. autofunction:: nse_xbrl_parser.detect_filing_format
```
