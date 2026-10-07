# NSE XBRL Parser Documentation

```{toctree}
:maxdepth: 2
:hidden:

getting_started/index
guides/index
taxonomies/index
api/index
```

---

**nse-xbrl-parser** is a modern, high-performance asynchronous Python 3.14 library designed to discover, download, parse, and normalize **all XBRL filings and taxonomies** published across the National Stock Exchange of India (NSE) and Bombay Stock Exchange (BSE).

---

## Key Highlights

::::{grid} 1 2 2 3
:gutter: 3

:::{grid-item-card} 🚀 Python 3.14 Async Native
Built from the ground up for asynchronous I/O using Python 3.14 native concurrency and `lxml` C-bindings. Non-blocking stream and batch processing.
:::

:::{grid-item-card} 📚 All 58 Taxonomies
Covers every single taxonomy category published by NSE & BSE—from Ind AS Financial Results to Shareholding Patterns, Corporate Governance, and Material Announcements.
:::

:::{grid-item-card} 🧩 Universal Parsing Engine
Automatically resolves contexts (`instant`, `duration`), units (`INR`, `shares`, `pure`), and dimensional segment qualifiers without requiring hard-coded rules per document.
:::

:::{grid-item-card} 🎯 Strongly Typed Adapters
Provides ergonomic Pydantic models for the most common filings: `FinancialResultsModel`, `ShareholdingPatternModel`, and `CorporateGovernanceModel`.
:::

:::{grid-item-card} 🔄 Taxonomy Registry & Caching
Built-in automated registry with on-demand schema (`.xsd`) and label linkbase (`*-lab.xml`) downloading and local caching.
:::

:::{grid-item-card} 🌐 Built-in Client
`AsyncNSEClient` provides automated downloading, session handling, and direct URL-to-model extraction.
:::

::::

---

## Quick Example

```python
import asyncio
from nse_xbrl_parser import parse_file, FinancialResultsModel

async def main():
    # 1. Parse any XBRL XML filing
    instance = await parse_file("RELIANCE_Q3_Results.xml")

    # 2. Universal Fact Lookups
    print("Company:", instance.get_fact_value("NameOfTheCompany"))
    print("Revenue:", instance.get_fact_float("RevenueFromOperations"))

    # 3. High-level Typed Adapter
    financials = FinancialResultsModel.from_instance(instance)
    print(f"Profit After Tax: ₹{financials.profit_after_tax:,.2f}")
    print(f"Basic EPS: ₹{financials.basic_eps:.2f}")
    print(f"EBITDA: ₹{financials.ebitda:,.2f}")

asyncio.run(main())
```

---

## Next Steps

- Check out {doc}`getting_started/installation` to set up the library.
- Walk through the {doc}`getting_started/quickstart` to parse your first filing in under 2 minutes.
- Browse the complete list of {doc}`taxonomies/all_taxonomies` supported out of the box.
