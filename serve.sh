#!/usr/bin/env bash
# 가이드북 로컬 서버 실행 (PC·모바일 열람용)
cd "$(dirname "$0")"
PORT="${1:-8000}"

IP=$(hostname -I 2>/dev/null | awk '{print $1}')
[ -z "$IP" ] && IP=$(ipconfig getifaddr en0 2>/dev/null)  # macOS

echo "=============================================="
echo " TP 유럽 여행 가이드북 서버 시작"
echo "   PC에서:      http://localhost:${PORT}"
[ -n "$IP" ] && echo "   모바일에서:  http://${IP}:${PORT}  (같은 Wi-Fi)"
echo "   종료: Ctrl+C"
echo "=============================================="

python3 -m http.server "$PORT" --directory site
