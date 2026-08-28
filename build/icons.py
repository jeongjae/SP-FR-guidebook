"""아이콘 — CSS 마스크 data URI 로 굽는다.

선 데이터는 여기가 원본이다. 출력은 style.css 뒤에 붙는다.

스프라이트를 페이지마다 인라인하면 314쪽 × 2KB 가 붙는다. 마스크로 두면
CSS 한 번만 받고 페이지 무게는 0 이다. 색은 currentColor 가 그대로 온다.
"""
from urllib.parse import quote

# 24 그리드 · 선 굵기 1.7 · 끝은 둥글게. 면이 아니라 선으로 그린다 —
# 국기 원색이 아이콘으로 새는 것을 막는다.
ICONS = {
 "today":   '<circle cx="12" cy="12" r="8.2"/><circle cx="12" cy="12" r="3.2" fill="currentColor" stroke="none"/>',
 "list":    '<path d="M4 6.5h16M4 12h16M4 17.5h16"/>',
 "back":    '<path d="M19 12H5.5M11.5 6l-6 6 6 6"/>',
 # 가이드 탭 = 나침반. 장소 핀(ic-pin)과 겹치던 물방울 핀에서 교체 (HIG 진단 1-6).
 # ic-region 은 하단탭 '가이드' 한 곳에만 쓰인다 — 지역 위치 마커로는 안 쓴다.
 "region":  '<circle cx="12" cy="12" r="8.4"/><path d="M12 6.6 14.1 12 12 17.4 9.9 12Z" fill="currentColor" stroke="none"/>',
 "topic":   '<rect x="3.8" y="3.8" width="7" height="7" rx="1.6"/><rect x="13.2" y="3.8" width="7" height="7" rx="1.6"/><rect x="3.8" y="13.2" width="7" height="7" rx="1.6"/><rect x="13.2" y="13.2" width="7" height="7" rx="1.6"/>',
 # 지도 = 접힌 지도. 원+십자(나침반처럼 읽히던 것)에서 교체 (HIG 진단 1-6).
 "map":     '<path d="M3 6.2 9 3.8l6 2.4 6-2.4v13.6l-6 2.4-6-2.4-6 2.4Z"/><path d="M9 3.8v13.6M15 6.2v13.6"/>',
 "clock":   '<circle cx="12" cy="12" r="8.4"/><path d="M12 7.2V12l3.4 2.1"/>',
 "gauge":   '<path d="M4 16.5a8.6 8.6 0 1 1 16 0"/><path d="M12 16.5 16 10"/><circle cx="12" cy="16.5" r="1.4" fill="currentColor" stroke="none"/>',
 "note":    '<path d="M6 3.6h8.2L19 8.4v12H6z"/><path d="M14 3.6v5h5"/><path d="M9 13h7M9 16.6h5"/>',
 "check":   '<path d="M5.2 4.6h13.6v14.8H5.2z" rx="2"/><path d="M8.6 12.2l2.5 2.5 4.6-5"/>',
 "pin":     '<path d="M12 21s6.6-6 6.6-10.6a6.6 6.6 0 1 0-13.2 0C5.4 15 12 21 12 21Z"/><circle cx="12" cy="10.3" r="2.4"/>',
 "book":    '<path d="M4.4 4.6h6.2A2.4 2.4 0 0 1 12 6.6v13a2 2 0 0 0-1.4-1.2H4.4z"/><path d="M19.6 4.6h-6.2A2.4 2.4 0 0 0 12 6.6v13a2 2 0 0 1 1.4-1.2h6.2z"/>',
 "food":    '<path d="M6.4 3.4v7.4a2.6 2.6 0 0 0 5.2 0V3.4M9 11v9.6"/><path d="M17.4 3.4c-1.6 1.4-2.2 3.2-2.2 5.2 0 1.7.8 2.8 2.2 3.1v8.9"/>',
 "train":   '<rect x="5.4" y="3.6" width="13.2" height="13.4" rx="3"/><path d="M5.4 10.6h13.2"/><path d="M8.6 21l1.8-4M15.4 21l-1.8-4"/><circle cx="9" cy="13.8" r="1"  fill="currentColor" stroke="none"/><circle cx="15" cy="13.8" r="1" fill="currentColor" stroke="none"/>',
 "stay":    '<path d="M3.4 19.4v-9.2M3.4 14.6h17.2v4.8M20.6 14.6v-3a2.6 2.6 0 0 0-2.6-2.6h-6.2v5.6"/><circle cx="7.4" cy="11.4" r="1.9"/>',
 "lock":    '<rect x="4.8" y="10.4" width="14.4" height="9.8" rx="2.4"/><path d="M8.4 10.4V7.8a3.6 3.6 0 0 1 7.2 0v2.6"/>',
 "cost":    '<circle cx="12" cy="12" r="8.4"/><path d="M12 7v10M14.6 9.4c-.6-.7-1.6-1-2.6-1-1.6 0-2.6.8-2.6 1.9 0 2.6 5.2 1.4 5.2 4 0 1.2-1.1 2-2.6 2-1.1 0-2.1-.4-2.7-1.1"/>',
 "tip":     '<path d="M9.4 18.4h5.2M10.2 21h3.6"/><path d="M12 3.2a5.8 5.8 0 0 0-3.4 10.5c.6.5.9 1.1.9 1.8v.9h5v-.9c0-.7.3-1.3.9-1.8A5.8 5.8 0 0 0 12 3.2Z"/>',
 "source":  '<path d="M9.6 6.4C7 7.8 5.6 10 5.6 12.8c0 2.2 1.3 3.6 3.1 3.6 1.7 0 2.9-1.2 2.9-2.8 0-1.6-1.1-2.7-2.6-2.7-.3 0-.6 0-.8.1"/><path d="M19 6.4c-2.6 1.4-4 3.6-4 6.4 0 2.2 1.3 3.6 3.1 3.6 1.7 0 2.9-1.2 2.9-2.8 0-1.6-1.1-2.7-2.6-2.7-.3 0-.6 0-.8.1"/>',
 "download":'<path d="M12 3.6v11.2M7.6 10.6 12 15l4.4-4.4"/><path d="M4.6 18.4v1.4h14.8v-1.4"/>',
 "table":   '<rect x="3.6" y="4.6" width="16.8" height="14.8" rx="2.4"/><path d="M3.6 9.6h16.8M9.4 9.6v9.8"/>',
 "license": '<circle cx="12" cy="12" r="8.4"/><path d="M14.6 9.6a3.4 3.4 0 1 0 0 4.8"/>',
 "search":  '<circle cx="10.8" cy="10.8" r="6.4"/><path d="M15.6 15.6 20.4 20.4"/>',
 "close":   '<path d="M5.6 5.6 18.4 18.4M18.4 5.6 5.6 18.4"/>',
 "up":      '<path d="M12 19.4V5.2M5.8 11.4 12 5.2l6.2 6.2"/>',
 "link":    '<path d="M13.6 10.4a4.2 4.2 0 0 0-6 0l-3 3a4.24 4.24 0 0 0 6 6l1.2-1.2"/><path d="M10.4 13.6a4.2 4.2 0 0 0 6 0l3-3a4.24 4.24 0 0 0-6-6l-1.2 1.2"/>',
 "photo":   '<rect x="3.4" y="5.4" width="17.2" height="13.2" rx="2.4"/><circle cx="8.8" cy="10.2" r="1.7"/><path d="M4 16.4 9.4 12l4 3.4 3-2.4 4.2 3.4"/>',
 "flag":    '<path d="M5.6 21V3.8M5.6 4.6h12.8l-2.4 4 2.4 4H5.6"/>',
 # 비상 = 경고 삼각형. 깃발은 이 프로젝트에서 국기(국가) 은유를 이미 쓴다 (진단 1-6).
 "alert":   '<path d="M12 3.6 21.6 19.8a1 1 0 0 1-.9 1.4H3.3a1 1 0 0 1-.9-1.4Z"/><path d="M12 9.6v5"/><circle cx="12" cy="17.6" r="1.1" fill="currentColor" stroke="none"/>',
 # 공연 = 프로시니엄(무대 개구부 + 양쪽 막). 실데이터가 오페라·발레·연극이라
 # 음표(콘서트)가 안 맞았다 (진단 1-6). 20px 에서 트로피로 읽히던 1안을 버렸다.
 "stage":   '<path d="M3.4 3.8h17.2v16.4H3.4z"/><path d="M3.4 3.8q4.3 2.2 4.3 8.2 0 5-1.9 8.2M20.6 3.8q-4.3 2.2-4.3 8.2 0 5 1.9 8.2"/><path d="M3.4 6.4h17.2" opacity=".55"/>',
 # 예약 카테고리 — 숙소·철도는 stay·train 을 그대로 쓴다.
 "car":     '<rect x="3.2" y="10.2" width="17.6" height="6.4" rx="2"/><path d="M5.8 10.2 7.3 6.4a1.9 1.9 0 0 1 1.8-1.2h5.8a1.9 1.9 0 0 1 1.8 1.2l1.5 3.8"/><path d="M5.4 16.6v2.2M18.6 16.6v2.2"/><circle cx="7.4" cy="13.4" r="1" fill="currentColor" stroke="none"/><circle cx="16.6" cy="13.4" r="1" fill="currentColor" stroke="none"/>',
 "plane":   '<path d="M10.4 4.2a1.6 1.6 0 0 1 3.2 0v4.6l7 4.1v2.2l-7-2.1v3.9l2.3 1.7v1.4L12 19.2l-3.9.8v-1.4l2.3-1.7v-3.9l-7 2.1v-2.2l7-4.1z"/>',
 "ticket":  '<path d="M3.6 7.6h16.8v2.6a1.9 1.9 0 0 0 0 3.6v2.6H3.6v-2.6a1.9 1.9 0 0 0 0-3.6z"/><path d="M13.4 7.6v1.6M13.4 11.2v1.6M13.4 14.8v1.6"/>',
 "music":   '<path d="M9.4 17.4V6.1l9.2-2v11.3"/><ellipse cx="6.8" cy="17.6" rx="2.6" ry="2.2"/><ellipse cx="16" cy="15.4" rx="2.6" ry="2.2"/>',
 "filter":  '<path d="M3.8 5.6h16.4l-6.4 7.4v5.6l-3.6 1.8v-7.4z"/>',
 "sound":   '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M19 5a9.5 9.5 0 0 1 0 14"/>',
 "copy":    '<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
 "star":    '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
 "chat":    '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
}

# 장소 추천등급 5종. 유니코드 도형(■●○◇▨)을 마스크로 바꾼다 — CLAUDE.md 가
# 금지한 방식이고 번들 폰트 범위 밖이라 기기에 따라 두부(□)가 된다 (HIG 진단 1-1).
# 모양 언어는 그대로다: 채움=중요, 외곽선=보조, 사선=회피. 색맹 대비가 색이
# 아니라 모양에 실려 있어야 한다. 채운 도형은 fill=currentColor 로 마스크에 싣는다.
GRADE_ICONS = {
 "essential":   '<path d="M12 2.6 21.4 12 12 21.4 2.6 12Z" fill="currentColor" stroke="none"/>',
 "priority":    '<circle cx="12" cy="12" r="7.6" fill="currentColor" stroke="none"/>',
 "optional":    '<circle cx="12" cy="12" r="7" stroke-width="2.4"/>',
 "alternative": '<path d="M12 3 21 12 12 21 3 12Z" stroke-width="2.2"/>',
 "excluded":    '<circle cx="12" cy="12" r="7.4" stroke-width="2.2"/><path d="M6.9 6.9 17.1 17.1" stroke-width="2.2"/>',
}

def uri(body):
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
           'stroke="#000" stroke-width="1.7" stroke-linecap="round" '
           f'stroke-linejoin="round">{body}</svg>')
    return 'url("data:image/svg+xml,' + quote(svg, safe="") + '")'

def css():
    """마스크 변수만 내보낸다. 상자·크기는 style.css 의 `.ic`·`.grade` 가 정한다."""
    out = ["/* ===== 아이콘 — build/icons.py 가 구운 마스크. 직접 고치지 마라. ===== */"]
    out += [f".ic-{n}::before {{ --ic: {uri(b)}; }}" for n, b in ICONS.items()]
    # 등급 마커도 같은 마스크 파이프라인. 색은 .grade-* 가 currentColor 로 정한다.
    out += [f".grade-{n}::before {{ --ic: {uri(b)}; }}" for n, b in GRADE_ICONS.items()]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    print(css())
