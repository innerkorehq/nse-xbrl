# Financial Results Guide (Regulation 33)

Regulation 33 mandates quarterly and annual financial statements in XBRL format. In 2024–2026, the NSE transitioned to Integrated Financial Filings (`IFIndAs`), consolidating multiple statements into single submissions.

## The Standard Four-Context Structure

Indian financial filings follow a four-context matrix:

| Context ID | Type | Description | Example Period |
|---|---|---|---|
| `OneD` | Duration | Current Quarter | 2025-10-01 to 2025-12-31 |
| `FourD` | Duration | Year-to-Date (YTD) | 2025-04-01 to 2025-12-31 |
| `OneI` | Instant | Balance Sheet Snapshot (Current) | 2025-12-31 |
| `PY_I` | Instant | Balance Sheet Snapshot (Prior Year) | 2024-03-31 |

`FinancialResultsModel` automatically maps facts against these contexts.

## Using `FinancialResultsModel`

```python
from nse_xbrl_parser import parse_file, FinancialResultsModel

instance = await parse_file("Q3_Results.xml")
model = FinancialResultsModel.from_instance(instance)
```

### Accessing Metadata
```python
print(model.company_name)      # e.g. "RELIANCE INDUSTRIES LIMITED"
print(model.scrip_code)        # e.g. "500325"
print(model.symbol)            # e.g. "RELIANCE"
print(model.reporting_quarter) # e.g. "Third Quarter"
print(model.nature_of_report)  # e.g. "Consolidated"
```

### Income Statement
```python
print("Revenue from Operations:", model.revenue_from_operations)
print("Other Income:", model.other_income)
print("Total Income:", model.total_income)

# Expenses
print("Cost of Materials:", model.cost_of_materials_consumed)
print("Employee Benefits:", model.employee_benefit_expense)
print("Finance Costs:", model.finance_costs)
print("Depreciation:", model.depreciation_amortization)
print("Total Expenses:", model.total_expenses)
```

### Profitability & Returns
```python
print("Profit Before Tax (PBT):", model.profit_before_tax)
print("Tax Expense:", model.tax_expense)
print("Profit After Tax (PAT):", model.profit_after_tax)
print("EBITDA:", model.ebitda)
print("Basic EPS:", model.basic_eps)
print("Diluted EPS:", model.diluted_eps)
```

### Balance Sheet
```python
print("Paid-up Equity Capital:", model.paid_up_equity_capital)
print("Reserves & Surplus:", model.reserves_and_surplus)
print("Total Assets:", model.total_assets)
```
