#!/usr/bin/env bash
# 선별한 관광 조망지도의 '지도 면'만 큰 JPEG 로 뽑는다 — SP-FR-guidebook MP-05
#
#   bash render_tourist_maps.sh
#
# _maps_download/files/ 의 원본에서 tourist_maps_pages.tsv 가 지정한 쪽만
# _maps_download/render/<slug>.jpg 로 뽑는다. 원본 PDF 는 316MB 라 저장소에
# 넣지 않는다 — 여기서 뽑은 JPEG 만 클라우드로 옮겨 WebP 로 줄인다.
#
# 이미 뽑아 둔 파일은 건너뛴다. 원본이 없으면 조용히 넘어가고 끝에 모아 알린다.

set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
DL="$(cd "$HERE/../_maps_download" 2>/dev/null && pwd)" || { echo "_maps_download 를 못 찾았다"; exit 1; }

TABLE="$HERE/tourist_maps_pages.tsv"
SRC="$DL/files"
OUT="$DL/render"
PX=2600          # 긴 변 기준. 휴대폰에서 확대해도 글자가 읽히는 선.
Q=88             # 여기서는 넉넉히 — 최종 압축은 클라우드에서 한 번만 한다.

[ -f "$TABLE" ] || { echo "$TABLE 이 없다"; exit 1; }
command -v pdftoppm >/dev/null || { echo "pdftoppm(poppler-utils) 이 없다"; exit 1; }

mkdir -p "$OUT"
missing=(); made=0; skipped=0

while IFS=$'\t' read -r slug src page; do
  [ "$slug" = "slug" ] && continue
  [ -n "${slug:-}" ] || continue
  dest="$OUT/$slug.jpg"

  if [ -s "$dest" ]; then
    printf '  · %-26s 이미 있음\n' "$slug"; skipped=$((skipped+1)); continue
  fi
  if [ ! -s "$SRC/$src" ]; then
    printf '  ? %-26s 원본 없음 (%s)\n' "$slug" "$src"; missing+=("$slug ← $src"); continue
  fi

  printf '  → %-26s ' "$slug"
  if [ "$page" = "0" ]; then
    # 이미 이미지다 — 크기만 맞춘다
    if command -v convert >/dev/null; then
      convert "$SRC/$src" -resize "${PX}x${PX}>" -quality "$Q" "$dest" 2>/dev/null
    else
      cp "$SRC/$src" "$dest"
    fi
  else
    pdftoppm -jpeg -jpegopt "quality=$Q" -scale-to "$PX" -f "$page" -l "$page" \
             -singlefile "$SRC/$src" "${dest%.jpg}" 2>/dev/null
  fi

  if [ -s "$dest" ]; then
    printf 'OK  %s KB\n' "$(( $(wc -c < "$dest") / 1024 ))"; made=$((made+1))
  else
    printf '실패\n'; missing+=("$slug ← $src p$page")
  fi
done < "$TABLE"

echo
echo "─────────────────────────────────────────────"
echo "새로 뽑음 $made · 건너뜀 $skipped · 못 뽑음 ${#missing[@]}"
du -sh "$OUT" 2>/dev/null
if [ ${#missing[@]} -gt 0 ]; then
  echo
  echo "못 뽑은 것 — manifest-gap.tsv 를 아직 안 받았으면 그것부터:"
  printf '  %s\n' "${missing[@]}"
fi
echo "─────────────────────────────────────────────"
