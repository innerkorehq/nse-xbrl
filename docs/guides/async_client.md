# Async Client Guide

`AsyncNSEClient` provides an asynchronous interface for downloading filing documents and taxonomy files directly from exchange portals.

## Basic Usage

```python
import asyncio
from nse_xbrl_parser import AsyncNSEClient

async def main():
    async with AsyncNSEClient() as client:
        # Download and parse an XBRL file directly from a URL
        url = "https://nsearchives.nseindia.com/corporate/xbrl/sample_filing.xml"
        try:
            instance = await client.parse_url(url)
            print("Parsed:", instance.get_fact_value("NameOfTheCompany"))
        except Exception as e:
            print("Download or parse error:", e)

asyncio.run(main())
```

## Session Cookies for Bot-Protected Endpoints

Dynamic NSE endpoints (such as `www.nseindia.com/api/*`) employ Akamai bot protection and require valid browser session cookies:

```python
client = AsyncNSEClient(cookie_string="_ga=...; bm_sz=...; ak_bmsc=...")
```
