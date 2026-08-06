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


PHOTO_REQUIRED = {
    "imageId", "placeId", "title", "source", "sourcePage", "originalFile",
    "creator", "license", "licenseUrl", "changes", "downloadDate", "usage",
    "role", "status", "altKo", "captionKo", "originalWidth", "originalHeight",
    "originalPath", "originalSha256", "variants",
}


def load_photo_manifest(root: Path) -> dict:
    """Load the responsive Pilot manifest and fail closed on incomplete records."""
    path = root / "data" / "images" / "image-manifest.json"
    if not path.exists():
        return {"images": []}
    payload = json.loads(path.read_text(encoding="utf-8"))
    seen = set()
    for asset in payload.get("images", []):
        image_id = asset.get("imageId", "")
        missing = sorted(field for field in PHOTO_REQUIRED if not asset.get(field))
        if missing:
            raise ValueError(f"photo manifest incomplete {image_id}: {', '.join(missing)}")
        if not image_id or image_id in seen:
            raise ValueError(f"duplicate or missing photo imageId: {image_id!r}")
        seen.add(image_id)
        if asset.get("licenseCode") not in {"public-domain", "cc0", "cc-by", "cc-by-sa"}:
            raise ValueError(f"disallowed photo license: {image_id}")
        if asset.get("status") not in {"processed", "inserted"}:
            raise ValueError(f"photo not processed: {image_id}")
        for variants in asset["variants"].values():
            for variant in variants:
                if not (root / variant["path"]).is_file():
                    raise ValueError(f"photo derivative missing: {image_id} {variant['path']}")
    return payload


def photos(manifest: dict) -> list[dict]:
    return manifest.get("images", [])


def photo_by_place(manifest: dict, place_id: str) -> dict | None:
    return next((item for item in photos(manifest) if item.get("placeId") == place_id), None)


def photos_for_usage(manifest: dict, usage: str) -> list[dict]:
    return [item for item in photos(manifest) if usage in item.get("usage", [])]


def photo_region_hero(manifest: dict) -> dict | None:
    return next((item for item in photos(manifest) if item.get("regionHero")), None)


def _photo_variants(asset: dict, variant: str) -> list[dict]:
    role = "thumbnail" if variant in {"card", "thumbnail", "gallery"} else variant
    found = list(asset["variants"].get(role, []))
    if not found and role == "hero":
        found = list(asset["variants"].get("content", []))
    return sorted(found, key=lambda item: item["width"])


def photo_figure(asset: dict | None, rel: str, variant: str = "content",
                 show_caption: bool = True, priority: bool = False) -> str:
    if not asset:
        return ""
    variants = _photo_variants(asset, variant)
    if not variants:
        return ""
    default = min(variants, key=lambda item: abs(item["width"] - 1280))
    srcset = ", ".join(f'{rel}/{item["sitePath"]} {item["width"]}w' for item in variants)
    sizes = ("100vw" if variant == "hero" else
             "(max-width: 720px) 100vw, 720px" if variant == "content" else
             "(max-width: 720px) 44vw, 320px")
    loading = "eager" if priority else "lazy"
    fetch_priority = ' fetchpriority="high"' if priority else ""
    credit = (f'<span class="media-credit">Photo: {html.escape(asset["creator"])} · '
              f'<a href="{html.escape(asset["licenseUrl"], quote=True)}" target="_blank" '
              f'rel="noopener license">{html.escape(asset["license"])}</a> · '
              f'<a href="{rel}/about/photo-credits.html#{html.escape(asset["imageId"])}">사진 정보</a></span>')
    caption = (f'<figcaption><span>{html.escape(asset["captionKo"])}</span>{credit}</figcaption>'
               if show_caption else f'<figcaption class="media-credit-only">{credit}</figcaption>')
    return f'''<figure class="guide-photo guide-photo--{html.escape(variant)}" data-photo-id="{html.escape(asset["imageId"])}">
  <picture>
    <source type="image/webp" srcset="{srcset}" sizes="{sizes}">
    <img src="{rel}/{default["sitePath"]}" alt="{html.escape(asset["altKo"])}"
      width="{default["width"]}" height="{default["height"]}" loading="{loading}"
      decoding="async"{fetch_priority}>
  </picture>
  {caption}
</figure>'''


def photo_gallery(items: list[dict], rel: str, heading: str, limit: int = 5) -> str:
    selected = items[:limit]
    if not selected:
        return ""
    figures = "".join(photo_figure(item, rel, variant="gallery") for item in selected)
    return (f'<section class="media-gallery guide-photo-gallery" aria-label="{html.escape(heading)}">'
            f'<h2 class="media-gallery-title">{html.escape(heading)}</h2>'
            f'<div class="media-gallery-grid">{figures}</div></section>')


def copy_photo_assets(root: Path, site: Path, manifest: dict) -> None:
    for asset in photos(manifest):
        for variants in asset["variants"].values():
            for variant in variants:
                source = root / variant["path"]
                target = site / variant["sitePath"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)


def photo_attribution_rows(manifest: dict, rel: str = "..") -> str:
    rows = []
    for asset in photos(manifest):
        variants = _photo_variants(asset, "thumbnail")
        thumb = variants[0]
        used = "".join(f"<li><code>/{html.escape(page)}</code></li>" for page in asset["usage"])
        rows.append(f'''<article class="credit-item" id="{html.escape(asset["imageId"])}">
<img src="{rel}/{thumb["sitePath"]}" alt="{html.escape(asset["altKo"])}"
 width="{thumb["width"]}" height="{thumb["height"]}" loading="lazy" decoding="async">
<div><h2>{html.escape(asset["titleKo"])}</h2>
<p><b>Photo:</b> {html.escape(asset["creator"])}</p>
<p><b>Source:</b> <a target="_blank" rel="noopener" href="{html.escape(asset["sourcePage"], quote=True)}">Wikimedia Commons 원본 설명 페이지</a></p>
<p><b>License:</b> <a target="_blank" rel="noopener license" href="{html.escape(asset["licenseUrl"], quote=True)}">{html.escape(asset["license"])}</a></p>
<p><b>Changes:</b> {html.escape(asset["changes"])}</p>
<p><b>Used in:</b></p><ul>{used}</ul></div>
</article>''')
    return "".join(rows)


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
