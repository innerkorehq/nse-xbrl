# Quickstart Guide

This guide gets you up and running with `nse-xbrl` in 2 minutes.

## 1. Parsing a Local XBRL File

You can parse any XBRL file asynchronously using `parse_file`:

```python
import asyncio
from nse_xbrl_parser import parse_file

async def main():
    instance = await parse_file("sample_filing.xml")
    
    # Check total facts parsed
    print(f"Extracted {len(instance.facts)} facts")
    
    # Lookup by tag name (Clark notation stripped)
    company = instance.get_fact_value("NameOfTheCompany")
    scrip = instance.get_fact_value("ScripCode")
    print(f"Filer: {company} (Scrip: {scrip})")

asyncio.run(main())
```

If you prefer synchronous parsing:

```python
from nse_xbrl_parser import parse_xbrl_sync

with open("sample_filing.xml", "rb") as f:
    instance = parse_xbrl_sync(f.read())

print(instance.get_fact_value("ScripCode"))
```

---

## 2. Working with Financial Results

Indian financial results follow standardized Ind AS / Banking / Insurance taxonomy tags. Convert the universal `XBRLInstance` into a typed `FinancialResultsModel`:

```python
from nse_xbrl_parser import parse_xbrl_sync, FinancialResultsModel

instance = parse_xbrl_sync(xml_bytes)
model = FinancialResultsModel.from_instance(instance)

print("Quarter:", model.reporting_quarter)
print("Standalone/Consolidated:", model.nature_of_report)
print(f"Revenue: ₹{model.revenue_from_operations:,.2f}")
print(f"Total Expenses: ₹{model.total_expenses:,.2f}")
print(f"PBT: ₹{model.profit_before_tax:,.2f}")
print(f"Tax: ₹{model.tax_expense:,.2f}")
print(f"PAT (Net Profit): ₹{model.profit_after_tax:,.2f}")
print(f"EBITDA: ₹{model.ebitda:,.2f}")
print(f"Basic EPS: ₹{model.basic_eps:.2f}")
```

---

## 3. Accessing Taxonomy Information

Inspect any of the 58 NSE/BSE regulatory taxonomies:

```python
import asyncio
from nse_xbrl_parser import TaxonomyRegistry, AsyncTaxonomyDownloader

async def main():
    registry = TaxonomyRegistry()

    # Search for Shareholding Pattern (Regulation 31)
    shp_info = registry.get_shareholding_pattern_taxonomy()
    print("Name:", shp_info.name)
    print("Download URL:", shp_info.primary_taxonomy_url)

    # Automatically download and parse its XSD schema and Label linkbase
    downloader = AsyncTaxonomyDownloader()
    schema, linkbase = await downloader.load_taxonomy_metadata(shp_info)

    print(f"Elements in schema: {len(schema.elements)}")
    label = linkbase.get_label("PublicShareholdingAsAPercentageOfTotalNumberOfShares")
    print("Human label:", label)

asyncio.run(main())
```
