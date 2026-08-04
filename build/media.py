"""Licensed local media catalog helpers for the static-site builder."""

from __future__ import annotations

import html
import json
import shutil
from pathlib import Path


ALLOWED_LICENSES = {
    "public-domain", "cc0", "cc-by", "cc-by-sa",
    "unsplash", "pexels", "pixabay", "official-permitted",
}


def load_catalog(root: Path) -> dict:
    path = root / "data" / "media-catalog.json"
    catalog = json.loads(path.read_text(encoding="utf-8"))
    seen = set()
    for asset in catalog.get("assets", []):
        media_id = asset.get("id", "")
        if not media_id or media_id in seen:
            raise ValueError(f"duplicate or missing media id: {media_id!r}")
        seen.add(media_id)
        if asset.get("license") not in ALLOWED_LICENSES:
            raise ValueError(f"disallowed media license: {media_id}")
        if not asset.get("altKo") or not asset.get("sourcePageUrl", "").startswith("https://"):
            raise ValueError(f"incomplete media metadata: {media_id}")
        if asset.get("attributionRequired") and not asset.get("author"):
            raise ValueError(f"attribution author missing: {media_id}")
        if asset.get("score", {}).get("total", 0) < 75:
            raise ValueError(f"media score below acceptance threshold: {media_id}")
        if not (root / asset["sourceFile"]).is_file():
            raise ValueError(f"media source file missing: {media_id}")
    return catalog


def assets(catalog: dict) -> list[dict]:
    return catalog.get("assets", [])


def by_id(catalog: dict, media_id: str) -> dict | None:
    return next((a for a in assets(catalog) if a["id"] == media_id), None)


def by_place(catalog: dict, place_slug: str) -> dict | None:
    return next((a for a in assets(catalog) if a.get("placeSlug") == place_slug), None)


def region_hero(catalog: dict, region_slug: str) -> dict | None:
    return next((a for a in assets(catalog)
                 if a.get("regionSlug") == region_slug and a.get("role") == "hero"), None)


def region_extras(catalog: dict, region_slug: str, roles: tuple[str, ...]) -> list[dict]:
    return [a for a in assets(catalog)
            if a.get("regionSlug") == region_slug and a.get("role") in roles]


def figure(asset: dict | None, rel: str, variant: str = "place",
           show_caption: bool = True, priority: bool = False) -> str:
    if not asset:
        return ""
    author = html.escape(asset.get("author") or asset["sourceName"])
    caption = html.escape(asset.get("captionKo") or asset["subjectName"])
    loading = "eager" if priority else "lazy"
    fetch_priority = ' fetchpriority="high"' if priority else ""
    credit = (
        f'<span class="media-credit">Photo: {author} / '
        f'<a href="{html.escape(asset["sourcePageUrl"], quote=True)}" target="_blank" '
        f'rel="noopener">{html.escape(asset["sourceName"])}</a> · '
        f'<a href="{html.escape(asset.get("licenseUrl") or asset["sourcePageUrl"], quote=True)}" '
        f'target="_blank" rel="noopener license">{html.escape(asset["licenseName"])}</a></span>'
    )
    if show_caption:
        caption_html = f'<figcaption><span>{caption}</span>{credit}</figcaption>'
    else:
        caption_html = f'<figcaption class="media-credit-only">{credit}</figcaption>'
    src = f'{rel}/{asset["localPath"]}'
    return f'''<figure class="guidebook-image guidebook-image--{html.escape(variant)}" data-media-id="{html.escape(asset["id"])}">
  <a class="media-zoom" href="{src}" target="_blank" rel="noopener" aria-label="{html.escape(asset["subjectName"])} 이미지 확대">
    <img src="{src}" alt="{html.escape(asset["altKo"])}" width="{asset["width"]}" height="{asset["height"]}" loading="{loading}" decoding="async"{fetch_priority} data-media-image>
  </a>
  <span class="media-fallback" hidden role="status">이미지를 불러오지 못했습니다.</span>
  {caption_html}
</figure>'''


def gallery(items: list[dict], rel: str, heading: str = "대표 이미지") -> str:
    if not items:
        return ""
    figures = "".join(figure(a, rel, variant="gallery") for a in items)
    return (f'<section class="media-gallery" aria-label="{html.escape(heading)}">'
            f'<h2 class="media-gallery-title">{html.escape(heading)}</h2>'
            f'<div class="media-gallery-grid">{figures}</div></section>')


def copy_assets(root: Path, site: Path, catalog: dict) -> None:
    for asset in assets(catalog):
        source = root / asset["sourceFile"]
        target = site / asset["localPath"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def attribution_rows(catalog: dict, rel: str = ".") -> str:
    rows = []
    for asset in assets(catalog):
        rows.append(f'''<figure class="credit-item">
<img src="{rel}/{asset["localPath"]}" alt="{html.escape(asset["altKo"])}" width="{asset["width"]}" height="{asset["height"]}" loading="lazy">
<figcaption><b>{html.escape(asset["subjectName"])}</b>
<span>저작자 {html.escape(asset.get("author") or "표시 의무 없음")}</span>
<span>출처 <a target="_blank" rel="noopener" href="{html.escape(asset["sourcePageUrl"], quote=True)}">{html.escape(asset["sourceName"])}</a></span>
<span>라이선스 <a target="_blank" rel="noopener license" href="{html.escape(asset.get("licenseUrl") or asset["sourcePageUrl"], quote=True)}">{html.escape(asset["licenseName"])}</a></span>
<span>수정 {html.escape(asset.get("modificationNote") or "없음")}</span></figcaption>
</figure>''')
    return "".join(rows)
