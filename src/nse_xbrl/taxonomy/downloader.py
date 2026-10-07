"""
nse_xbrl.taxonomy.downloader

Asynchronous downloader and cache manager for official NSE/BSE taxonomy archives.
"""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Dict, Optional, Tuple
import zipfile
import aiohttp

from .linkbase import TaxonomyLinkbase
from .registry import TaxonomyInfo, TaxonomyRegistry
from .schema import TaxonomySchema


class AsyncTaxonomyDownloader:
    """Async downloader and local cache for taxonomy schema and linkbase packages."""

    def __init__(self, cache_dir: Optional[Path] = None) -> None:
        if cache_dir is None:
            cache_dir = Path.home() / ".cache" / "nse_xbrl" / "taxonomies"
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._schema_cache: Dict[int, TaxonomySchema] = {}
        self._linkbase_cache: Dict[int, TaxonomyLinkbase] = {}

    async def download_taxonomy_archive(
        self,
        taxonomy: TaxonomyInfo,
        force_reload: bool = False,
    ) -> Path:
        """Download and cache the ZIP archive for a taxonomy category."""
        target_file = self.cache_dir / f"taxonomy_{taxonomy.id}.zip"
        if target_file.exists() and not force_reload:
            return target_file

        url = taxonomy.primary_taxonomy_url
        if not url:
            raise ValueError(f"No taxonomy URL found for taxonomy {taxonomy.id}: {taxonomy.name}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "*/*",
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise ConnectionError(
                        f"Failed to download taxonomy {taxonomy.id} from {url} (HTTP {response.status})"
                    )
                content = await response.read()

        await asyncio.to_thread(target_file.write_bytes, content)
        return target_file

    async def load_taxonomy_metadata(
        self,
        taxonomy: TaxonomyInfo,
    ) -> Tuple[Optional[TaxonomySchema], Optional[TaxonomyLinkbase]]:
        """Download (if needed) and parse schemas and label linkbases from the taxonomy package."""
        if taxonomy.id in self._schema_cache and taxonomy.id in self._linkbase_cache:
            return self._schema_cache[taxonomy.id], self._linkbase_cache[taxonomy.id]

        archive_path = await self.download_taxonomy_archive(taxonomy)

        schema: Optional[TaxonomySchema] = None
        linkbase: Optional[TaxonomyLinkbase] = None

        def _extract() -> Tuple[Optional[TaxonomySchema], Optional[TaxonomyLinkbase]]:
            s: Optional[TaxonomySchema] = None
            lb: Optional[TaxonomyLinkbase] = None
            with zipfile.ZipFile(archive_path) as z:
                # Look for main schema
                for name in z.namelist():
                    if name.endswith(".xsd") and "roles" not in name and "types" not in name:
                        xsd_bytes = z.read(name)
                        s = TaxonomySchema.from_xsd_content(xsd_bytes)
                        break

                # Look for label linkbase
                for name in z.namelist():
                    if name.endswith(".xml") and any(
                        sub in name.lower() for sub in ["-lab", "-label"]
                    ):
                        lbl_bytes = z.read(name)
                        lb = TaxonomyLinkbase.from_label_xml(lbl_bytes)
                        break

            return s, lb

        schema, linkbase = await asyncio.to_thread(_extract)
        if schema:
            self._schema_cache[taxonomy.id] = schema
        if linkbase:
            self._linkbase_cache[taxonomy.id] = linkbase

        return schema, linkbase
