# Corporate Governance Guide (Regulation 27(2))

Listed companies must submit quarterly compliance reports on Corporate Governance under Regulation 27(2) of SEBI (LODR).

## Model Overview

The `CorporateGovernanceModel` adapter parses board composition, committee formations, and regulatory disclosures.

## Example Usage

```python
from nse_xbrl_parser import parse_file, CorporateGovernanceModel

instance = await parse_file("INFY_CG.xml")
cg = CorporateGovernanceModel.from_instance(instance)

print("Company:", cg.company_name)
print("Quarter:", cg.reporting_quarter)
print("Risk Management Committee:", cg.has_risk_management_committee)
```
