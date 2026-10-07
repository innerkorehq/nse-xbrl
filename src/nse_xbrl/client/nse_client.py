"""
nse_xbrl.client.nse_client

Asynchronous client for interacting with NSE corporate filings and archive downloads.
"""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import aiohttp

from ..core.models import XBRLInstance
from ..core.parser import AsyncXBRLParser
from ..taxonomy.downloader import AsyncTaxonomyDownloader
from ..taxonomy.registry import TaxonomyInfo, TaxonomyRegistry


class AsyncNSEClient:
    """Asynchronous client for downloading and parsing NSE XBRL disclosures."""

    DEFAULT_USER_AGENT = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    def __init__(
        self,
        cookie_string: Optional[str] = None,
        cache_dir: Optional[Path] = None,
    ) -> None:
        self.cookie_string = cookie_string
        self.parser = AsyncXBRLParser()
        self.registry = TaxonomyRegistry()
        self.downloader = AsyncTaxonomyDownloader(cache_dir=cache_dir)
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            headers = {
                "User-Agent": self.DEFAULT_USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Referer": "https://www.nseindia.com/",
            }
            if self.cookie_string:
                headers["Cookie"] = self.cookie_string
            self._session = aiohttp.ClientSession(headers=headers)
        return self._session

    async def close(self) -> None:
        """Close client session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self) -> AsyncNSEClient:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()

    async def download_bytes(self, url: str) -> bytes:
        """Download raw bytes from URL asynchronously."""
        session = await self._get_session()
        async with session.get(url) as response:
            if response.status != 200:
                raise ConnectionError(f"HTTP GET failed with status {response.status} for {url}")
            return await response.read()

    async def parse_url(self, url: str) -> XBRLInstance:
        """Download XBRL instance document from URL and parse it."""
        data = await self.download_bytes(url)
        return await self.parser.parse(data, source_name=url)

    async def parse_url_archive(self, zip_url: str) -> List[XBRLInstance]:
        """Download ZIP archive from URL and parse all contained XBRL filings."""
        data = await self.download_bytes(zip_url)
        return await self.parser.parse_zip(data)

    async def get_taxonomy_schema(self, taxonomy_id: int):
        """Fetch schema for any of the 58 NSE taxonomies."""
        info = self.registry.get_by_id(taxonomy_id)
        if not info:
            raise KeyError(f"Taxonomy ID {taxonomy_id} not found in registry (1-58)")
        schema, _ = await self.downloader.load_taxonomy_metadata(info)
        return schema

    async def get_taxonomy_labels(self, taxonomy_id: int):
        """Fetch label dictionary for any of the 58 NSE taxonomies."""
        info = self.registry.get_by_id(taxonomy_id)
        if not info:
            raise KeyError(f"Taxonomy ID {taxonomy_id} not found in registry (1-58)")
        _, linkbase = await self.downloader.load_taxonomy_metadata(info)
        return linkbase
