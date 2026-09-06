#!/usr/bin/env python3
"""Synchronize the final Paris Museum Pass itinerary (2026-09-26..10-02)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(day: int) -> dict:
    return json.loads((ROOT / f"data/daily-cards/day-{day}.json").read_text())


def save(day: int, data: dict) -> None:
    (ROOT / f"data/daily-cards/day-{day}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    )


def stop(id, order, start, end, name, category, lat, lng, summary, *,
         statuses=None, note="", url="https://www.paris.fr/", optional=False,
         place_ref=None, menu=None):
    return {
        "id": id, "order": order, "start": start, "end": end, "name": name,
        "category": category, "lat": lat, "lng": lng, "summary": summary,
        "menu": menu, "reservation": None, "executionStatuses": statuses or [],
        "executionNote": note, "officialUrl": url, "optional": optional,
        "place_ref": place_ref,
    }


def leg(a, b, mode, minutes, note):
    return {"from": a, "to": b, "mode": mode, "duration": f"{minutes}분",
            "distance": None, "line": note, "geometryStatus": "coordinate-line"}


def renumber(data):
    for i, item in enumerate(data["stops"], 1):
        item["order"] = i


def main() -> None:
    d29 = load(29)
    morning = d29["stops"][0]
    morning.update(end="13:30", name="오전 생활 일정 · 숙소 휴식", summary="15구 토요 생활권 장보기와 숙소 점심·휴식 후 PMP 첫 입장에 맞춰 출발")
    d29.update(title="파리 뮤지엄 패스 시작 — 생트샤펠·콩시에르주리", endTime="20:30",
               totalDuration="12시간 30분", totalDistance="약 10 km")
    d29["stops"] = [morning,
        stop("sainte-chapelle",2,"15:00","16:00","Sainte-Chapelle (생트샤펠) — PMP 최초 사용","culture",48.8554,2.345,
             "15세기 스테인드글라스를 집중 관람하며 6일/144시간 Paris Museum Pass를 처음 사용한다.",
             statuses=[{"type":"confirmed","label":"PMP FIRST USE","detail":"9/26 15:00 전후 첫 스캔. PMP 6일/144시간 사용 시작."}],
             note="14:45 보안검색 도착. PMP QR을 오프라인 저장.",url="https://www.sainte-chapelle.fr/"),
        stop("conciergerie",3,"16:10","17:10","Conciergerie (콩시에르주리)","culture",48.8554,2.345,
             "생트샤펠에서 이어지는 시테 섬의 중세 왕궁과 프랑스혁명 수감 공간 관람.",
             statuses=[{"type":"confirmed","label":"PMP","detail":"Paris Museum Pass 포함. 생트샤펠 첫 사용 뒤 연속 입장."}],
             note="두 시설 사이 보안 재진입 시간을 고려한다.",url="https://www.paris-conciergerie.fr/"),
        stop("cite-seine-walk",4,"17:15","18:30","Île de la Cité · Seine 산책","sight",48.8554,2.345,
             "시테 섬과 센 강변을 천천히 걸으며 오후 박물관 일정을 마무리한다.",optional=True),
        stop("bouillon-racine-dinner",5,"19:00","20:30","Bouillon Racine 저녁","food",48.8506,2.342,
             "시테 섬에서 생미셸 방향으로 이동해 기존 저녁 일정을 유지한다.",place_ref="bouillon-racine",menu="Œuf mayo · blanquette de veau · crème brûlée"),
        stop("paris-return",6,"20:45","21:15","15구 숙소 귀환","transport",48.841,2.285,"Bouillon Racine 저녁 뒤 메트로로 숙소 생활권에 복귀한다."),
    ]
    d29["legs"]=[leg("morning-routine","sainte-chapelle","metro",35,"15구 숙소 → Cité"),leg("sainte-chapelle","conciergerie","walk",5,"같은 Palais de la Cité 권역"),leg("conciergerie","cite-seine-walk","walk",5,"시테 섬"),leg("cite-seine-walk","bouillon-racine-dinner","walk",15,"생미셸 방면"),leg("bouillon-racine-dinner","paris-return","metro",30,"메트로 10·8호선")]
    d29["highlights"]=["Sainte-Chapelle — PMP 6일권 최초 사용","Conciergerie","Île de la Cité와 센 강 산책"]
    d29["backup"]="입장 지연 시 센 강 산책을 줄이고 Sainte-Chapelle과 Conciergerie 두 PMP 핵심 관람을 우선한다. 저녁 대안은 L'Avant Comptoir."
    d29["map"]={"zoom":15,"center":[48.853,2.343],"routeCache":None}
    save(29,d29)

    d30=load(30); morning=d30["stops"][0]; morning.update(end="09:00")
    d30.update(title="피카소·노트르담 & 고전 파리 도시공간",endTime="21:00",totalDuration="13시간",totalDistance="약 15 km")
    d30["stops"]=[morning,
        stop("musee-picasso",2,"10:30","12:15","Musée Picasso Paris","culture",48.8597,2.3622,
             "Hôtel Salé의 피카소 상설 컬렉션을 PMP 유효기간 안에 집중 관람한다.",
             statuses=[{"type":"confirmed","label":"PMP","detail":"Paris Museum Pass 포함. 10:30 입장 계획."}],note="5 Rue de Thorigny. PMP QR 준비.",url="https://www.museepicassoparis.fr/",place_ref="musee-picasso-paris"),
        stop("marais-lunch",3,"12:15","13:15","Le Marais 점심","food",48.8586,2.355,
             "피카소 관람 뒤 마레에서 가볍게 점심을 먹고 시테 섬으로 이동한다."),
        stop("notre-dame",4,"13:30","14:15","Notre-Dame de Paris","sight",48.853,2.3499,
             "복원된 대성당과 파르비스를 둘러본다. 무료 입장이며 PMP는 필요하지 않다.",
             statuses=[{"type":"check","label":"FREE · PMP NOT NEEDED","detail":"무료 입장. 현장 대기와 운영시간만 확인."}],note="PMP 사용처로 계산하지 않는다.",url="https://www.notredamedeparis.fr/",place_ref="notre-dame-de-paris"),
        stop("tuileries-vendome",5,"15:00","16:00","Jardin des Tuileries & Place Vendôme","sight",48.8635,2.3275,"튀일르리 정원과 방돔 광장을 잇는 고전 파리 산책."),
        stop("palais-royal",6,"16:10","17:15","Palais Royal","sight",48.8638,2.337,"팔레 루아얄 안뜰과 정원을 산책한다."),
        stop("opera-garnier-district",7,"17:30","18:30","Opéra Garnier 권역","sight",48.8719,2.3316,"오페라 가르니에 외관과 인근 벨 에포크 도시공간을 걷는다."),
        d30["stops"][-1],
    ]; renumber(d30)
    d30["legs"]=[leg("morning-routine","musee-picasso","metro",35,"15구 → Saint-Paul"),leg("musee-picasso","marais-lunch","walk",5,"마레"),leg("marais-lunch","notre-dame","walk",20,"시테 섬"),leg("notre-dame","tuileries-vendome","metro",20,"Cité → Concorde"),leg("tuileries-vendome","palais-royal","walk",10,"도보"),leg("palais-royal","opera-garnier-district","walk",15,"도보"),leg("opera-garnier-district","paris-return","metro",25,"Montparnasse")]
    d30["highlights"]=["Musée Picasso Paris — PMP","Notre-Dame — 무료","Tuileries·Place Vendôme·Palais Royal·Opéra Garnier"]
    d30["backup"]="피로 또는 입장 지연 시 도시 산책 구간을 단축하되 Picasso와 Notre-Dame을 우선한다. Petit Palais는 핵심 관람에서 제외한다."
    d30["map"]={"zoom":13,"center":[48.862,2.345],"routeCache":None}; save(30,d30)

    d31=load(31)
    arc=stop("arc-de-triomphe-optional",5,"17:45","18:30","Arc de Triomphe (개선문) — 선택","sight",48.8738,2.295,"저녁 체력과 날씨가 좋을 때만 PMP로 전망대에 오른다.",statuses=[{"type":"optional","label":"OPTIONAL · PMP","detail":"필수 일정 아님. PMP 포함, 현장 운영·마지막 입장 확인."}],optional=True,url="https://www.paris-arc-de-triomphe.fr/")
    d31["stops"]=[s for s in d31["stops"] if s["id"]!="arc-de-triomphe-optional"]
    d31["stops"].insert(-1,arc); d31["stops"][-1].update(start="19:15",end="21:00"); renumber(d31)
    d31["legs"]=[leg("morning-routine","gustave-moreau","metro",35,"15구 → 9구"),leg("gustave-moreau","opera-lunch","walk",10,"도보"),leg("opera-lunch","fashion-week-marais","metro",25,"마레"),leg("fashion-week-marais","arc-de-triomphe-optional","metro",25,"선택 이동"),leg("arc-de-triomphe-optional","paris-return","metro",30,"15구")]
    d31["highlights"]=[h for h in d31["highlights"] if "Arc de Triomphe" not in h]
    d31["highlights"].append("Arc de Triomphe 전망대 — 저녁 Optional · PMP"); save(31,d31)

    d33=load(33)
    guimet=stop("musee-guimet",6,"14:40","16:20","Musée Guimet","culture",48.865,2.2936,"간다라·크메르·동아시아 컬렉션을 PMP 유효기간 안에 집중 관람한다.",statuses=[{"type":"confirmed","label":"PMP","detail":"Paris Museum Pass 포함. 14:40 입장 계획."}],note="6 Place d'Iéna. 16:20 종료 후 Président Wilson 방면 이동.",url="https://www.guimet.fr/",place_ref="musee-guimet")
    for s in d33["stops"]:
        if s["id"]=="champs-elysees-lunch": s.update(end="13:15")
        if s["id"]=="avenue-montaigne": s.update(start="13:20",end="14:00")
        if s["id"]=="grand-palais-fashion-week": s.update(start="14:00",end="14:25")
        if s["id"]=="palais-de-tokyo": s.update(start="16:30",end="17:45")
    d33["stops"]=[s for s in d33["stops"] if s["id"]!="musee-guimet"]
    d33["stops"].insert(-2,guimet); renumber(d33)
    ids=[s["id"] for s in d33["stops"]]
    d33["legs"]=[leg(a,b,"metro" if (a,b) in [("morning-routine","orangerie"),("palais-de-tokyo","paris-return")] else "walk",20,"최신 PMP 실행 동선") for a,b in zip(ids,ids[1:])]
    d33["title"]="모네·패션위크·기메 — 컨템퍼러리 파리"; d33["highlights"]=[h for h in d33["highlights"] if "Guimet" not in h]
    d33["highlights"].append("Musée Guimet — PMP"); d33["highlights"]=d33["highlights"][:4]
    d33["map"]={"zoom":13,"center":[48.863,2.314],"routeCache":None}; save(33,d33)

    d35=load(35)
    for s in d35["stops"]:
        if s["id"]=="morning-routine": s.update(end="10:15",name="Boulangerie Pichard 아침 & Louvre 출발 준비")
        elif s["id"]=="musee-du-louvre":
            s.update(start="11:00",end="15:00")
            s["executionStatuses"]=[{"type":"book","label":"TIMED ENTRY · PMP LAST USE","detail":"Musée du Louvre 11:00 시간예약. 10:40 도착, PMP 6일권 마지막 핵심 사용."}]
            s["executionNote"]="11:00 시간예약자 입구. PMP QR과 Louvre 예약 QR을 함께 준비."
        elif s["id"]=="cour-carree-seine": s.update(start="15:00",end="16:15")
        elif s["id"]=="paris-return": s.update(start="18:00",end="20:00")
    d35.update(title="루브르 11:00 — PMP 마지막 핵심 사용",endTime="20:00",totalDuration="12시간")
    d35["highlights"]=["Musée du Louvre 11:00","PMP 6일/144시간 마지막 핵심 사용","Cour Carrée와 센 강변"]
    d35["needsReview"]=["Musée du Louvre 11:00 슬롯 사전 예매 필수"]
    d35["map"]={"zoom":14,"center":[48.85,2.315],"routeCache":None}
    save(35,d35)

    d37=load(37)
    race=next(s for s in d37["stops"] if s["id"]=="prix-de-l-arc")
    race["reservation"]="confirmed"
    race["executionStatuses"][0]={"type":"confirmed","label":"BOOKED · GENERAL ENTRY","detail":"Qatar Prix de l'Arc de Triomphe General Entry 예약완료. 지정석/VIP가 아님. 모바일 QR 및 신분증 지참."}
    race["executionNote"]="Hippodrome de ParisLongchamp. General Entry 확정 티켓 QR 및 신분증 지참."
    d37["highlights"]=["Qatar Prix de l'Arc de Triomphe","General Entry — 예약완료","ParisLongchamp"]
    save(37,d37)

    d39=load(39); d39["stops"]=[s for s in d39["stops"] if s["id"]!="musee-picasso"]
    for s in d39["stops"]:
        if s["id"]=="musee-carnavalet": s.update(start="16:30",end="18:30")
    renumber(d39); ids=[s["id"] for s in d39["stops"]]
    d39["legs"]=[leg(a,b,"metro" if a in ("morning-routine","chez-janou-dinner") else "walk",20,"특별전 이후 정리된 마레 동선") for a,b in zip(ids,ids[1:])]
    d39["title"]="오르세 Mary Cassatt 특별전 & 마레 산책"
    d39["highlights"]=[h for h in d39["highlights"] if "Picasso" not in h]
    d39["backup"]="Mary Cassatt 특별전을 우선하고 이후 마레·카르나발레 산책은 피로에 따라 단축한다. 저녁 대안은 Au Bourguignon du Marais."
    d39["sourceRefs"]=[x for x in d39["sourceRefs"] if "Picasso" not in x]; save(39,d39)
    d39["needsReview"]=[x for x in d39["needsReview"] if "Picasso" not in x]
    save(39,d39)

    d41=load(41); d41["stops"]=[s for s in d41["stops"] if s["id"]!="musee-guimet"]
    for s in d41["stops"]:
        if s["id"]=="morning-routine": s.update(end="11:15",name="여유 있는 아침 & Iéna 출발")
        elif s["id"]=="iena-lunch": s.update(start="12:00",end="13:15")
    renumber(d41); ids=[s["id"] for s in d41["stops"]]
    d41["legs"]=[leg(a,b,"metro" if a in ("morning-routine","trocadero-sunset") else "walk",25,"현대미술관과 고별 동선") for a,b in zip(ids,ids[1:])]
    d41["title"]="파리 현대미술관 & 트로카데로 고별 일몰"
    d41["highlights"]=[h for h in d41["highlights"] if "Guimet" not in h and "기메" not in h]
    d41["sourceRefs"]=[x for x in d41["sourceRefs"] if "Guimet" not in x and "기메" not in x]
    d41["needsReview"]=[x for x in d41["needsReview"] if "Guimet" not in x and "기메" not in x]
    d41["backup"]=(d41["backup"] or "").replace("Hanok, par Misso(기메 박물관 내부, 도보 0분 — 옛 Le Salon des Porcelaines 자리가 한식당으로 바뀌었다. 국물 국수 기반이라 저녁 만찬 대비 가장 가볍다)","Hanok, par Misso(이에나 권역 한식당 — 국물 국수 기반이라 저녁 만찬 대비 가장 가볍다)")
    save(41,d41)

    # Map query registry mirrors each rendered stop and must not retain stale routes.
    mq_path=ROOT/"data/map-queries.json"; mq=json.loads(mq_path.read_text())
    addresses={
        "sainte-chapelle":"Sainte-Chapelle, 10 Boulevard du Palais, Paris",
        "conciergerie":"Conciergerie, 2 Boulevard du Palais, Paris",
        "cite-seine-walk":"Île de la Cité, Paris",
        "musee-picasso":"Musée Picasso Paris, 5 Rue de Thorigny, Paris",
        "marais-lunch":"Le Marais, Paris",
        "notre-dame":"Cathédrale Notre-Dame de Paris",
        "arc-de-triomphe-optional":"Arc de Triomphe, Place Charles de Gaulle, Paris",
        "musee-guimet":"Musée Guimet, 6 Place d'Iéna, Paris",
    }
    for day in (29,30,31,33,35,37,39,41):
        card=load(day); prefix=f"day-{day}:"
        for key in list(mq["routes"]):
            if key.startswith(prefix): del mq["routes"][key]
        for item in card["stops"]:
            key=prefix+item["id"]
            mq["routes"][key]={"title":item["name"],"origin":addresses.get(item["id"],item["name"]),"destination":addresses.get(item["id"],item["name"]),"travelMode":"walking","evidence":"Canonical Day itinerary synchronized for PMP window","verifiedAt":"2026-09-06"}
    mq_path.write_text(json.dumps(mq,ensure_ascii=False,indent=2)+"\n")

    # Canonical execution routes used by map validation and region/day views.
    routes_path=ROOT/"source/ASSETS/maps/daily-routes.json"; routes=json.loads(routes_path.read_text())
    place_ids={
        "morning-routine":"paris-15e-stay-area","sainte-chapelle":"sainte-chapelle",
        "conciergerie":"conciergerie","cite-seine-walk":"ile-de-la-cite",
        "bouillon-racine-dinner":"bouillon-racine","musee-picasso":"musee-picasso-paris",
        "marais-lunch":"le-marais","notre-dame":"notre-dame-de-paris",
        "tuileries-vendome":"jardin-des-tuileries","palais-royal":"palais-royal",
        "opera-garnier-district":"palais-garnier","paris-return":"paris-15e-stay-area",
        "arc-de-triomphe-optional":"arc-de-triomphe","orangerie":"musee-de-l-orangerie",
        "champs-elysees-lunch":"chez-savy","avenue-montaigne":"avenue-montaigne",
        "grand-palais-fashion-week":"grand-palais","musee-guimet":"musee-guimet",
        "palais-de-tokyo":"palais-de-tokyo","musee-du-louvre":"musee-du-louvre",
        "prix-de-l-arc":"parislongchamp","musee-d-orsay-cassatt":"musee-d-orsay",
        "musee-carnavalet":"musee-carnavalet","musee-art-moderne":"musee-d-art-moderne-de-paris",
        "trocadero-sunset":"trocadero",
    }
    dates={load(d)["date"]:d for d in (29,30,31,33,35,37,39,41)}
    for route in routes["days"]:
        day=dates.get(route.get("date"))
        if not day: continue
        card=load(day); mapped=[]
        for item in card["stops"]:
            pid=place_ids.get(item["id"])
            if pid: mapped.append({"placeId":pid,"order":len(mapped),"plannedTime":f'{item["start"]}–{item["end"]}',"note":item["summary"]})
        route.update(title=card["title"],center=card["map"]["center"],zoom=card["map"]["zoom"],stops=mapped,
                     segments=[{"from":a["placeId"],"to":b["placeId"],"mode":"walking","manual":True} for a,b in zip(mapped,mapped[1:])])
    routes_path.write_text(json.dumps(routes,ensure_ascii=False,indent=2)+"\n")

    registry_path=ROOT/"source/ASSETS/maps/place-registry.json"; registry=json.loads(registry_path.read_text())
    existing={p["id"] for p in registry["places"]}
    coords={}
    for day in (29,30,31,33,35,37,39,41):
        for item in load(day)["stops"]:
            pid=place_ids.get(item["id"])
            if pid: coords[pid]=(item["name"],item["lat"],item["lng"],item["optional"])
    for pid,(name,lat,lng,optional) in coords.items():
        if pid in existing: continue
        registry["places"].append({"id":pid,"name":name,"city":"Paris","type":"attraction","lat":lat,"lng":lng,"googlePlaceId":"","googleMapsUrl":f"https://www.google.com/maps/search/?api=1&query={name}","address":"","private":False,"approximate":False,"optional":optional,"status":"planned","legacySources":["Paris PMP itinerary synchronization 2026-09-06"]})
    registry_path.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+"\n")


if __name__ == "__main__":
    main()
