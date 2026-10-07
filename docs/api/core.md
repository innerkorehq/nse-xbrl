# Core API Reference

Universal models and parsing engine in `nse_xbrl.core`.

## High-Level Parsing Functions

```{eval-rst}
.. autofunction:: nse_xbrl.parse_xbrl

.. autofunction:: nse_xbrl.parse_file

.. autofunction:: nse_xbrl.parse_archive

.. autofunction:: nse_xbrl.parse_xbrl_sync
```

## Parsing Engine

```{eval-rst}
.. autoclass:: nse_xbrl.core.parser.AsyncXBRLParser
   :members:
   :show-inheritance:
```

## Universal Models

```{eval-rst}
.. autoclass:: nse_xbrl.core.models.XBRLInstance
   :members:
   :show-inheritance:

.. autoclass:: nse_xbrl.core.models.XBRLFact
   :members:
   :show-inheritance:

.. autoclass:: nse_xbrl.core.context.XBRLContext
   :members:
   :show-inheritance:

.. autoclass:: nse_xbrl.core.unit.XBRLUnit
   :members:
   :show-inheritance:
```
