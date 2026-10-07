# nse-xbrl

Modern Asynchronous Python 3.14 library for parsing XBRL Filing Information across **all 58 taxonomies** of the National Stock Exchange of India (NSE) and Bombay Stock Exchange (BSE).

---

## Features

- **Universal XBRL 2.1 & Dimensions Parser**:
  - Asynchronous stream and file parsing using Python 3.14 native `asyncio` and `lxml`.
  - Automatically resolves contexts (`instant`, `duration`), entity identifiers (CIN, Scrip Code), units (`INR`, `shares`, ratios), and dimensional segments.
  - Zero requirement for custom parsers per filing type—parses *any* NSE/BSE filing format.
- **Coverage of all 58 NSE & BSE Taxonomies**:
  - Built-in catalog indexing all 58 taxonomies from [NSE XBRL Information Portal](https://www.nseindia.com/static/companies-listing/xbrl-information).
  - Automatically downloads and caches official schemas (`.xsd`), label linkbases (`*-lab.xml`), calculations, and presentations.
- **High-Level Typed Model Adapters**:
  - `FinancialResultsModel`: Regulation 33 Financial Results (`Ind AS`, `Banking`, `NBFC`, `Insurance`, `Integrated Filings`).
  - `ShareholdingPatternModel`: Regulation 31 Shareholding Patterns with promoter & public breakdown.
  - `CorporateGovernanceModel`: Regulation 27(2) Board composition & committee details.
- **Async HTTP Client (`AsyncNSEClient`)**:
  - Automated download and extraction of filing ZIP packages and instance XML documents.

---

## Installation

```bash
# Using uv (recommended)
uv add nse-xbrl

# Or with pip
pip install nse-xbrl
```

---

## Quickstart

### 1. Parse an XBRL Filing Asynchronously

```python
import asyncio
from nse_xbrl import parse_file, FinancialResultsModel

async def main():
    # Parse any filing XML
    instance = await parse_file("RELIANCE_Financial_Results.xml")

    # Universal Fact Lookups
    print("Company:", instance.get_fact_value("NameOfTheCompany"))
    print("Scrip Code:", instance.get_fact_value("ScripCode"))
    print("Revenue:", instance.get_fact_float("RevenueFromOperations"))

    # Convert to Strongly-Typed Model
    results = FinancialResultsModel.from_instance(instance)
    print(f"PAT: ₹{results.profit_after_tax:,.2f}")
    print(f"EBITDA: ₹{results.ebitda:,.2f}")
    print(f"Basic EPS: ₹{results.basic_eps:.2f}")

asyncio.run(main())
```

### 2. Inspect Any of the 58 NSE/BSE Taxonomies

```python
import asyncio
from nse_xbrl import TaxonomyRegistry, AsyncTaxonomyDownloader

async def main():
    registry = TaxonomyRegistry()

    # Total 58 taxonomies registered
    print("Total Taxonomies:", registry.count())

    # Get Regulation 31 Shareholding Pattern Taxonomy (ID 4)
    shp_tax = registry.get_by_id(4)
    print(shp_tax.name)
    print("Download URL:", shp_tax.primary_taxonomy_url)

    # Download schema & label linkbase on the fly
    downloader = AsyncTaxonomyDownloader()
    schema, linkbase = await downloader.load_taxonomy_metadata(shp_tax)

    print(f"Total concepts declared: {len(schema.elements)}")
    print("Human friendly label:", linkbase.get_label("PublicShareholdingAsAPercentageOfTotalNumberOfShares"))

asyncio.run(main())
```

### 3. Parse Shareholding Patterns & Corporate Governance

```python
from nse_xbrl import parse_xbrl_sync, ShareholdingPatternModel, CorporateGovernanceModel

xml_content = open("TCS_SHP.xml", "rb").read()
instance = parse_xbrl_sync(xml_content)

shp = ShareholdingPatternModel.from_instance(instance)
print(f"Promoter Holding: {shp.promoter_holding_percentage}%")
print(f"Public Holding: {shp.public_holding_percentage}%")
```

---

## Supported Taxonomies (All 58 Categories)

1. `Regulation 13 (3)` - Statement of Investor complaints
2. `Investor complaints` - REITs / InvITs
3. `Regulation 27 (2)` - Corporate Governance
4. `Regulation 31` - Shareholding Pattern
5. `Reconciliation of Share Capital Audit`
6. `Regulation 33` - Financial Results - Ind AS & Integrated Filing
7. `Regulation 33` - Financial Results - Other than Banks
8. `Regulation 33` - Financial Results - REITs / InvITs
9. `Regulation 33` - Financial Results - General Insurance
10. `Regulation 33` - Financial Results - Life Insurance
11. `Regulation 33` - Financial Results - Banking
12. `Regulation 33` - Financial Results - NBFC
13. `Regulation 44` - Voting Results
14. `Regulation 7(2) & 7(3)` - Insider Trading
15. `Regulation 32 (1)` - Statement of Deviation/Variation
16. `Regulation 24A` - Secretarial Compliance Report
17. `Regulation 60` - Record Date / Book Closure
18. `Unit Holding Pattern`
19. `Regulation 23 (9)` - Related Party Transactions
20. `Business Responsibility and Sustainability Reporting (BRSR)`
21. `Credit Rating`
22. `Default History Information`
23. `Interest Payment`
24. `Redemption Payment`
25. `Regulation 50` - Prior Intimation of Board Meeting
26. `Regulation 29` - Prior Intimation of Board Meeting
27. `Regulation 30` - Change in Directors / KMP / SMP / Auditor
28. `Regulation 30` - Acquisitions / Scheme of Arrangement / Restructuring
29. `Regulation 30` - Outcome of Board Meeting (Dividend, Bonus, Buyback)
30. `Regulation 30` - Issuance / Forfeiture / Alteration of Securities
31. `Regulation 30` - Material Agreements / Joint Ventures
32. `Regulation 30` - Fraud / Defaults / Arrests
33. `Regulation 30` - One Time Settlement (OTS)
34. `Regulation 30` - Resolution Plan / Debt Restructuring
35. `Regulation 30` - Notice of Shareholders Meeting
36. `Regulation 30` - Closure of Trading Window
37. `Regulation 39` - Loss of Share Certificate / Duplicate Issue
38. `Regulation 30` - Corporate Insolvency Resolution Process (CIRP)
39. `Regulation 33` - Statement on Impact of Audit Qualifications
40. `Insider Trading Plan`
41. `Integrated Filing - Governance`
42. `Regulation 30` - Awarding / Bagging of Orders
43. `ISD` - Buy-back from Open Market Route
44. `ISD` - Buy-back through Tender Offer Route
45. `Initial Public Offer (IPO)` - In-principle
46. `ADR / GDR` - In-principle and Post Allotment
47. `FCCB` - In-principle and Post Allotment
48. `Preferential Issue` - In-principle and Post Allotment
49. `QIP` - In-principle and Post Allotment
50. `Rights Issue` - In-principle and Post Allotment
51. `Initial Public Offer (IPO)` - Final Listing
52. `Resignation of Director / KMP / SMP / Compliance Officer`
53. `Regulation 30` - Resignation of Statutory Auditor
54. `Regulation 30` - Forensic Audit
55. `Regulation 30` - Actions initiated / taken or orders passed
56. `Regulation 30` - Analyst / Investor Meet
57. `Violation of Code of Conduct` (Insider Trading)
58. `Regulation 30` - Para B of Part A of Schedule III

---

## Testing

```bash
uv run pytest
```
