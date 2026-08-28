#!/usr/bin/env bash
# 관광 조망지도 일괄 내려받기 — SP-FR-guidebook MP-05
#
#   bash fetch-maps.sh                    # manifest.tsv 를 읽는다
#   bash fetch-maps.sh manifest-gap.tsv   # 다른 목록을 읽는다
#
# 목록을 읽어 같은 폴더의 files/ 아래로 받는다.
# 이미 받은 파일은 건너뛴다 — 몇 번 돌려도 안전하다.
#
# 끝나면 result-<목록이름>.tsv 에 파일별 성패·용량·형식이 남는다. 그 파일과 files/ 를
# 그대로 두면 다음 단계(조망형 육안 판정)에서 쓴다.
#
# 실패는 정상이다. 관광청 사이트 몇 곳은 봇을 막거나(403) 인증서가
# 어긋나 있다(Roussillon). 무엇이 실패했는지만 알면 된다.

set -uo pipefail
cd "$(dirname "$0")"

MANIFEST="${1:-manifest.tsv}"
OUT="files"
RESULT="result-$(basename "$MANIFEST" .tsv).tsv"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

[ -f "$MANIFEST" ] || { echo "manifest.tsv 가 없다"; exit 1; }
command -v curl >/dev/null || { echo "curl 이 없다"; exit 1; }

mkdir -p "$OUT"
printf 'id\tcity\tfilename\tstatus\tbytes\tkind\turl\n' > "$RESULT"

ok=0; skip=0; fail=0; total=0

# 헤더 한 줄 건너뛰고 읽는다
tail -n +2 "$MANIFEST" | while IFS=$'\t' read -r id region city rank publisher official year license filename url; do
  [ -n "${url:-}" ] || continue
  total=$((total+1))
  dest="$OUT/$filename"

  if [ -s "$dest" ]; then
    size=$(wc -c < "$dest" | tr -d ' ')
    printf '%s\t%s\t%s\tSKIP\t%s\t-\t%s\n' "$id" "$city" "$filename" "$size" "$url" >> "$RESULT"
    printf '  · %-3s %-26s 이미 있음 (%s bytes)\n' "$id" "$city" "$size"
    skip=$((skip+1))
    continue
  fi

  printf '  → %-3s %-26s ' "$id" "$city"
  # -f 실패 시 본문 저장 안 함 · -L 리다이렉트 추적 · --retry 일시 오류 재시도
  if curl -fsSL --retry 2 --retry-delay 1 --max-time 180 \
          -A "$UA" -e "$(printf '%s' "$url" | sed -E 's#(https?://[^/]+).*#\1/#')" \
          -o "$dest" "$url" 2>/dev/null; then
    size=$(wc -c < "$dest" | tr -d ' ')
    if [ "$size" -lt 2000 ]; then
      # 2KB 미만이면 오류 페이지를 받았을 가능성이 크다
      kind=$(file -b --mime-type "$dest" 2>/dev/null || echo "?")
      printf '의심 (%s bytes, %s)\n' "$size" "$kind"
      printf '%s\t%s\t%s\tSUSPECT\t%s\t%s\t%s\n' "$id" "$city" "$filename" "$size" "$kind" "$url" >> "$RESULT"
      fail=$((fail+1))
    else
      kind=$(file -b --mime-type "$dest" 2>/dev/null || echo "?")
      printf 'OK  %s KB  %s\n' "$((size/1024))" "$kind"
      printf '%s\t%s\t%s\tOK\t%s\t%s\t%s\n' "$id" "$city" "$filename" "$size" "$kind" "$url" >> "$RESULT"
      ok=$((ok+1))
    fi
  else
    rm -f "$dest"
    printf '실패\n'
    printf '%s\t%s\t%s\tFAIL\t0\t-\t%s\n' "$id" "$city" "$filename" "$url" >> "$RESULT"
    fail=$((fail+1))
  fi
done

echo
echo "─────────────────────────────────────────────"
echo "결과는 $RESULT 에 있다. 요약:"
awk -F'\t' 'NR>1{c[$4]++} END{for(k in c) printf "  %-8s %d건\n", k, c[k]}' "$RESULT"
echo
echo "받은 파일: $OUT/"
du -sh "$OUT" 2>/dev/null
echo
echo "실패한 것:"
awk -F'\t' 'NR>1 && ($4=="FAIL" || $4=="SUSPECT"){printf "  %-3s %-26s %s\n", $1, $2, $4}' "$RESULT"
echo "─────────────────────────────────────────────"
