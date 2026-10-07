# Universal XBRL Parsing

The Universal Parsing Engine (`nse_xbrl.core`) is the foundation of the library. It can parse any XBRL 2.1 document filed with NSE or BSE, regardless of whether a specialized typed model exists for that specific filing.

## How It Works

1. **Namespace Normalization**: XBRL files often mix namespaces like `in-bse-fin`, `in-capmkt`, `in-ind-as`, or `xbrli`. The engine indexes tags both by their canonical local name and Clark notation.
2. **Context Resolution**: The parser identifies instant snapshots (e.g. Balance Sheet dates) vs. duration periods (e.g. Quarter or Year-To-Date), along with explicit dimensional members (e.g. Standalone vs Consolidated).
3. **Unit Coercion**: Automatically recognizes currency symbols (`iso4217:INR`), share counts, and ratios (`pure`).

```{mermaid}
flowchart LR
    A[XML Stream / File] --> B[AsyncXBRLParser]
    B --> C[XBRLContexts]
    B --> D[XBRLUnits]
    B --> E[XBRLFacts]
    C & D & E --> F[XBRLInstance]
```

## Parsing from Multiple Sources

### From a Local File
```python
from nse_xbrl import parse_file

instance = await parse_file("filing.xml")
```

### From Raw Bytes or Strings
```python
from nse_xbrl import parse_xbrl

xml_data = b"<xbrl>...</xbrl>"
instance = await parse_xbrl(xml_data)
```

### From a ZIP Archive
NSE and BSE frequently bundle filing XML files inside `.zip` archives. Use `parse_archive`:

```python
from nse_xbrl import parse_archive

with open("filing_package.zip", "rb") as f:
    zip_bytes = f.read()

instances = await parse_archive(zip_bytes)
for inst in instances:
    print(inst.get_fact_value("NameOfTheCompany"))
```

## Querying Facts

### Direct Tag Lookup
```python
val = instance.get_fact_value("RevenueFromOperations")
```

### Specific Context Lookup
When multiple contexts exist (e.g. Current Quarter `OneD` vs YTD `FourD`):
```python
val = instance.get_fact_value("RevenueFromOperations", context_ref="OneD")
```

### Regex Search
Search for concepts matching a regex pattern:
```python
matching = instance.search_facts("profit|income")
for fact in matching:
    print(fact.local_name, fact.value)
```
