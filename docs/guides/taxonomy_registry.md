# Taxonomy Registry & Caching

The library maintains an embedded, up-to-date registry of all **58 official taxonomies** published on the [NSE XBRL Information Portal](https://www.nseindia.com/static/companies-listing/xbrl-information).

## Exploring the Registry

```python
from nse_xbrl_parser import TaxonomyRegistry

registry = TaxonomyRegistry()
print("Registered Taxonomies:", registry.count())
```

### Searching by Name or Regulation
```python
# Search for voting results
voting_tax = registry.find_by_name("Voting Result")
for t in voting_tax:
    print(t.id, t.name, t.primary_taxonomy_url)
```

## Downloading Schemas and Labels

`AsyncTaxonomyDownloader` handles downloading and caching official ZIP archives into `~/.cache/nse_xbrl_parser/taxonomies/`.

```python
import asyncio
from nse_xbrl_parser import TaxonomyRegistry, AsyncTaxonomyDownloader

async def main():
    registry = TaxonomyRegistry()
    downloader = AsyncTaxonomyDownloader()

    # Get Regulation 13(3) Investor Complaints
    tax_info = registry.get_by_id(1)
    
    # Download and load schema and label linkbase
    schema, linkbase = await downloader.load_taxonomy_metadata(tax_info)
    
    # Inspect concepts declared in the XSD
    print(f"Declared concepts: {len(schema.elements)}")
    for concept in list(schema.elements.values())[:5]:
        print(concept.name, concept.type, concept.period_type)

    # Inspect English labels
    label = linkbase.get_label("ScripCode")
    print("Label:", label)

asyncio.run(main())
```
