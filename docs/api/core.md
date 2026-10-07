# Core API Reference

Universal models and parsing engine in `nse_xbrl_parser.core`.

## High-Level Parsing Functions

```{eval-rst}
.. autofunction:: nse_xbrl_parser.parse_xbrl

.. autofunction:: nse_xbrl_parser.parse_file

.. autofunction:: nse_xbrl_parser.parse_archive

.. autofunction:: nse_xbrl_parser.parse_xbrl_sync
```

## Parsing Engine

```{eval-rst}
.. autoclass:: nse_xbrl_parser.core.parser.AsyncXBRLParser
   :members:
   :show-inheritance:
```

## Universal Models

```{eval-rst}
.. autoclass:: nse_xbrl_parser.core.models.XBRLInstance
   :members:
   :show-inheritance:

.. autoclass:: nse_xbrl_parser.core.models.XBRLFact
   :members:
   :show-inheritance:

.. autoclass:: nse_xbrl_parser.core.context.XBRLContext
   :members:
   :show-inheritance:

.. autoclass:: nse_xbrl_parser.core.unit.XBRLUnit
   :members:
   :show-inheritance:
```
