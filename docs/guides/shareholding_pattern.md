# Shareholding Pattern Guide (Regulation 31)

Regulation 31 of SEBI (LODR) requires quarterly submission of Shareholding Patterns (SHP) by listed entities.

## Model Overview

The `ShareholdingPatternModel` adapter parses the filing and structures the breakdown into high-level summary figures and individual shareholder categories.

## Example Usage

```python
from nse_xbrl import parse_file, ShareholdingPatternModel

instance = await parse_file("TCS_SHP.xml")
shp = ShareholdingPatternModel.from_instance(instance)

print("Company:", shp.company_name)
print("Quarter Ended:", shp.quarter_ended)
print(f"Promoter Holding: {shp.promoter_holding_percentage:.2f}%")
print(f"Public Holding: {shp.public_holding_percentage:.2f}%")
print(f"Promoter Pledged: {shp.promoter_shares_pledged_percentage:.2f}%")
```

## Extracting Granular Categories

You can iterate through individual category holdings:

```python
for category in shp.categories:
    print(category.category_name)
    print("  Shares:", category.total_shares)
    print("  Percentage:", category.shareholding_percentage)
```
