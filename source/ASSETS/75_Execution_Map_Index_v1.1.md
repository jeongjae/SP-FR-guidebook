# 75. Execution Map Index v1.1

## 사용법

- **HTML:** 브라우저에서 실행. Leaflet·OpenStreetMap 배경과 Google Maps 링크 때문에 인터넷 연결이 필요하다.
- **GeoJSON:** QGIS, geojson.io, 일부 모바일 지도 앱에서 불러오기 가능하다.
- **KML:** Google My Maps·Google Earth 등에서 가져오기 가능하다.
- 지도 선은 대략적인 거점 연결선이며 도보·운전 경로가 아니다.
- `숙소 후보` 핀은 예약 전 후보 위치다. Girona 지도는 Phase 8 확정 예약에 따라 `확정 숙소` 핀으로 교체했다.

| 거점 | 대상일 | HTML | GeoJSON | KML | 포인트 | 분류 |
|---|---|---|---|---|---:|---|
| Barcelona·Sitges | Day 1–4 | [HTML](75_Execution_Maps/Barcelona_Execution_Map_v0.2.html) | [GeoJSON](75_Execution_Maps/Barcelona_Execution_Map_v0.2.geojson) | [KML](75_Execution_Maps/Barcelona_Execution_Map_v0.2.kml) | 8 | 숙소 후보 1 · 핵심 방문지 5 · 교통 1 · 근교·이동지 1 |
| Bàscara·Girona·Empordà | Day 4–7 | [HTML](75_Execution_Maps/Girona_Execution_Map_v0.2.html) | [GeoJSON](75_Execution_Maps/Girona_Execution_Map_v0.2.geojson) | [KML](75_Execution_Maps/Girona_Execution_Map_v0.2.kml) | 11 | 확정 숙소 1 · 핵심 방문지 5 · 대체안 2 · 기준점 2 |
| Nice·Côte d’Azur | Day 7–12 | [HTML](75_Execution_Maps/Nice_Execution_Map_v0.2.html) | [GeoJSON](75_Execution_Maps/Nice_Execution_Map_v0.2.geojson) | [KML](75_Execution_Maps/Nice_Execution_Map_v0.2.kml) | 8 | 숙소 후보 1 · 시장·생활 2 · 핵심 방문지 1 · 교통 2 · 근교·이동지 2 |
| Aix-en-Provence | Day 12–16 | [HTML](75_Execution_Maps/Aix_Execution_Map_v0.2.html) | [GeoJSON](75_Execution_Maps/Aix_Execution_Map_v0.2.geojson) | [KML](75_Execution_Maps/Aix_Execution_Map_v0.2.kml) | 7 | 숙소 후보 1 · 교통 1 · 핵심 방문지 3 · 근교·이동지 2 |
| Luberon | Day 16–20 | [HTML](75_Execution_Maps/Luberon_Execution_Map_v0.2.html) | [GeoJSON](75_Execution_Maps/Luberon_Execution_Map_v0.2.geojson) | [KML](75_Execution_Maps/Luberon_Execution_Map_v0.2.kml) | 8 | 숙소 후보 1 · 시장·생활 1 · 근교·이동지 6 |
| Avignon·Alpilles | Day 20–24 | [HTML](75_Execution_Maps/Avignon_Execution_Map_v0.2.html) | [GeoJSON](75_Execution_Maps/Avignon_Execution_Map_v0.2.geojson) | [KML](75_Execution_Maps/Avignon_Execution_Map_v0.2.kml) | 8 | 숙소 후보 1 · 시장·생활 1 · 핵심 방문지 2 · 근교·이동지 4 |
| Lyon·Annecy | Day 24–28 | [HTML](75_Execution_Maps/Lyon_Execution_Map_v0.2.html) | [GeoJSON](75_Execution_Maps/Lyon_Execution_Map_v0.2.geojson) | [KML](75_Execution_Maps/Lyon_Execution_Map_v0.2.kml) | 8 | 숙소 후보 1 · 핵심 방문지 5 · 시장·생활 1 · 근교·이동지 1 |
| Paris | Day 28–43 | [HTML](75_Execution_Maps/Paris_Execution_Map_v0.2.html) | [GeoJSON](75_Execution_Maps/Paris_Execution_Map_v0.2.geojson) | [KML](75_Execution_Maps/Paris_Execution_Map_v0.2.kml) | 10 | 숙소 후보 1 · 핵심 방문지 7 · 근교·이동지 2 |

## Phase 6 검증결과

- 8개 거점 × HTML·GeoJSON·KML = 24개 파일 존재
- GeoJSON 65개 포인트의 좌표 형식·필수속성 검증 완료
- HTML 8개에 숙소 상태 경고·범례·Google Maps 링크 반영
- KML 8개에 카테고리 접두어 반영
- HTML은 완전 오프라인 지도가 아니며, 이 제한을 각 파일과 본문에 명시
