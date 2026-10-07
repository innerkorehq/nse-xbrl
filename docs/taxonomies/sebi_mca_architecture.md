# SEBI & MCA Taxonomy Architecture

Stock exchanges in India (NSE & BSE) mandate XBRL reporting aligned with the Ministry of Corporate Affairs (MCA) and Securities and Exchange Board of India (SEBI).

## Joint Standardization

Historically, filers prepared separate disclosure files for BSE and NSE. Since 2020–2024, the exchanges jointly harmonized their taxonomy schemas:

- **SEBI Capital Markets Core (`in-capmkt.xsd`)**: The universal base taxonomy used across all Regulation 30 corporate announcements, investor grievances, and debt filings. Target namespace: `https://www.sebi.gov.in/xbrl/2024-05-31/in-capmkt`.
- **BSE Financial Results (`in-bse-fin-*.xsd`)**: Core taxonomy for Ind AS and Indian GAAP financial statements, balance sheets, and cash flows. Target namespace: `http://www.bseindia.com/xbrl/fin/2020-03-31/in-bse-fin`.
- **BSE Shareholding Pattern (`in-bse-shp-*.xsd`)**: Target namespace: `http://www.bseindia.com/xbrl/shp/2025-10-31/in-bse-shp`.
- **BSE Corporate Governance (`in-bse-cg-*.xsd`)**: Target namespace: `http://www.bseindia.com/xbrl/cg/2024-03-31/in-bse-cg`.

## Interoperability

Because these schemas are standardized:
1. An XBRL filing generated using the official BSE Excel utility can be parsed identically to one submitted via NSE NEAPS.
2. The `nse-xbrl` library abstracts taxonomy differences by utilizing local tag lookups and linkbase mapping.
