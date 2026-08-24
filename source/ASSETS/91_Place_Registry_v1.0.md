# 장소 레지스트리 v1.0

가이드북의 **최소 단위**다. 갈 수 있으면 장소, 아니면 섹션이라는 기준으로 나눈다.
빌드가 이 표를 읽어 장소 페이지를 만들고, 지도 핀·본문 헤딩과 대조해 어긋나면 중단한다.

| 열 | 뜻 |
|---|---|
| **타입** | `spot` 갈 곳 · `node` 이동 기준점(역·공항, 페이지 없음) |
| **등급** | 본문 등급 헤딩에서. 없으면 추천등급 표에서. 둘 다 없으면 `미정` |
| **지도 핀** | 실행지도·KML 의 이름. 좌표와 Google Maps 링크의 원천 |
| **본문** | 상세 서술이 있는 페이지. `—` 는 아직 서술이 없다는 뜻 |
| **헤딩** | 그 페이지의 등급 헤딩 원문. 빌드가 이 문자열로 대조한다 |

## barcelona (04)

| 슬러그 | 이름 | 타입 | 등급 | 지도 핀 | 본문 | 헤딩 | 위키 |
|---|---|---|---|---|---|---|---|
| `barcelona-sants` | Barcelona Sants | node | — | Barcelona Sants | — | — | — |
| `barri-gotic` | Barri Gòtic | spot | 필수 | Gòtic | chapters/barcelona/places.html | Barri Gòtic | Gothic Quarter, Barcelona |
| `biblioteca-de-catalunya` | Biblioteca de Catalunya | spot | 우선 추천 | Biblioteca de Catalunya | chapters/barcelona/places.html | Biblioteca de Catalunya | Biblioteca de Catalunya |
| `cau-ferrat` | Cau Ferrat | spot | 필수 | — | chapters/barcelona/places.html | Cau Ferrat | Cau Ferrat Museum |
| `macba` | MACBA | spot | 선택 | MACBA | chapters/barcelona/places.html | MACBA | Museu d'Art Contemporani de Barcelona |
| `palau-de-maricel` | Palau de Maricel | spot | 우선 추천 | — | chapters/barcelona/places.html | Palau de Maricel | Maricel Museum |
| `sagrada-familia` | Sagrada Família | spot | 필수 | Sagrada Família | chapters/barcelona/places.html | Sagrada Família | Sagrada Família |
| `sant-pau-recinte-modernista` | Sant Pau Recinte Modernista | spot | 필수 | Sant Pau | chapters/barcelona/places.html | Sant Pau Recinte Modernista | Hospital de Sant Pau |
| `sitges` | Sitges | spot | 선택 | Sitges | chapters/barcelona/places.html | Sitges | Sitges |
| `bodega-joan` | Bodega Joan | spot | 필수 | Bodega Joan | chapters/barcelona/places.html | Bodega Joan | — |
| `puertecillo-sagrada-familia` | Puertecillo Sagrada Família | spot | 필수 | Puertecillo Sagrada Familia | chapters/barcelona/places.html | Puertecillo Sagrada Família | — |
| `bar-canete` | Bar Cañete | spot | 필수 | Bar Cañete | chapters/barcelona/places.html | Bar Cañete | — |
| `mercat-concepcio` | Mercat de la Concepció | spot | 우선 추천 | Mercat de la Concepció | chapters/barcelona/places.html | Mercat de la Concepció | fr:Marché de la Concepció |
| `la-zorra` | La Zorra | spot | 우선 추천 | La Zorra | chapters/barcelona/places.html | La Zorra | — |
| `barcelona-historic-walk` | Barcelona 역사도심 — Barri Gòtic·Rambla 권역 | walk | 필수 | — | — | — | — |
| `barcelona-modernisme-walk` | Barcelona Modernisme — Eixample 권역 | walk | 필수 | — | — | — | — |

## girona (05)

| 슬러그 | 이름 | 타입 | 등급 | 지도 핀 | 본문 | 헤딩 | 위키 |
|---|---|---|---|---|---|---|---|
| `calella-de-palafrugell` | Calella de Palafrugell | spot | 선택 | Calella de Palafrugell | chapters/girona/places.html | Calella de Palafrugell | Calella de Palafrugell |
| `collioure` | Collioure | spot | 필수 | Collioure | chapters/girona/places.html | Collioure | Collioure |
| `girona-cathedral` | Girona Cathedral | spot | 필수 | Girona Cathedral | chapters/girona/places.html | Girona Cathedral | Girona Cathedral |
| `passeig-de-la-muralla` | Passeig de la Muralla | spot | 필수 | — | chapters/girona/places.html | 성벽 (Passeig de la Muralla) | Passeig de la Muralla |
| `onyar` | Onyar 강변 | spot | 필수 | Onyar Houses | chapters/girona/places.html | Onyar 강변 | Onyar |
| `pals` | Pals | spot | 우선 추천 | Pals | chapters/girona/places.html | Pals | Pals |
| `peralada` | Peralada | spot | 선택 | Peralada | chapters/girona/places.html | Peralada | Peralada |
| `peratallada` | Peratallada | spot | 필수 | Peratallada | chapters/girona/places.html | Peratallada | Peratallada |
| `casa-marieta` | Casa Marieta | spot | 필수 | Casa Marieta | chapters/girona/places.html | Casa Marieta | — |
| `mercat-del-lleo` | Mercat del Lleó | spot | 우선 추천 | Mercat del Lleó | chapters/girona/places.html | Mercat del Lleó | — |
| `girona-old-town-walk` | Girona 구시가지 — Call·성벽·대성당 권역 | walk | 필수 | — | — | — | — |

## nice (06)

| 슬러그 | 이름 | 타입 | 등급 | 지도 핀 | 본문 | 헤딩 | 위키 |
|---|---|---|---|---|---|---|---|
| `cannes` | Cannes | spot | 우선 추천 | Cannes | chapters/nice/places.html | Cannes | Cannes |
| `colline-du-chateau` | Colline du Château (성채 언덕) | spot | 필수 | Castle Hill | chapters/nice/places.html | Colline du Château (성채 언덕) | Castle Hill, Nice |
| `cours-saleya` | Cours Saleya | spot | 필수 | Cours Saleya | chapters/nice/places.html | Cours Saleya | Cours Saleya |
| `le-rocher` | Le Rocher — 모나코 구시가지 | spot | 필수 | — | chapters/nice/places.html | Le Rocher — 모나코 구시가지 | Rock of Monaco |
| `le-suquet` | Le Suquet — 칸 구시가지 | spot | 필수 | — | chapters/nice/places.html | Le Suquet — 칸 구시가지 | Le Suquet |
| `marche-forville` | Marché Forville | spot | 필수 | — | chapters/nice/places.html | Marché Forville | fr:Marché Forville |
| `marche-de-la-liberation` | Marché de la Libération | spot | 우선 추천 | Libération Market | chapters/nice/places.html | Marché de la Libération | — |
| `monaco` | Monaco | spot | 우선 추천 | Monaco | chapters/nice/places.html | Monaco | Monaco |
| `menton` | Menton (멘통) | spot | 필수 | Menton | chapters/nice/places.html | Menton (멘통) | Menton |
| `nice-walk` | Nice Old Town–Castle Hill Walk | walk | 필수 | — | chapters/nice/places.html | Nice Old Town–Castle Hill Walk | — |
| `cannes-walk` | Cannes Forville–Suquet–Croisette Walk | walk | 필수 | — | chapters/nice/places.html | Cannes Forville–Suquet–Croisette Walk | — |
| `monaco-walk` | Monaco Rocher–Port–Monte Carlo Walk | walk | 필수 | — | chapters/nice/places.html | Monaco Rocher–Port–Monte Carlo Walk | — |
| `nce-t2` | NCE T2 | node | — | NCE T2 | — | — | — |
| `nice-ville` | Nice-Ville | node | — | Nice-Ville | — | — | — |
| `promenade-des-anglais` | Promenade des Anglais | spot | 필수 | — | chapters/nice/places.html | Promenade des Anglais | Promenade des Anglais |
| `vieux-nice` | Vieux Nice — 구시가지 | spot | 필수 | — | chapters/nice/places.html | Vieux Nice — 구시가지 | fr:Vieux-Nice |
| `le-figuier-de-saint-esprit` | Le Figuier de Saint-Esprit | spot | 필수 | Le Figuier de Saint-Esprit | chapters/nice/places.html | Le Figuier de Saint-Esprit | — |
| `restaurant-beatrice` | Restaurant & Salon de Thé Béatrice | spot | 필수 | Restaurant Béatrice | chapters/nice/places.html | Restaurant & Salon de Thé Béatrice | — |
| `villa-ephrussi-de-rothschild` | Villa Ephrussi de Rothschild | spot | 우선 추천 | Villa Ephrussi | chapters/nice/places.html | Villa Ephrussi de Rothschild | Villa Ephrussi de Rothschild |

## aix (07)

| 슬러그 | 이름 | 타입 | 등급 | 지도 핀 | 본문 | 헤딩 | 위키 |
|---|---|---|---|---|---|---|---|
| `atelier-des-lauves` | Atelier des Lauves | spot | 필수 | Atelier Cézanne | chapters/aix/places.html | Atelier des Lauves | Atelier de Cézanne |
| `bastide-du-jas-de-bouffan` | Bastide du Jas de Bouffan | spot | 우선 추천 | — | chapters/aix/places.html | Bastide du Jas de Bouffan — 선택 | Bastide du Jas de Bouffan |
| `calanques` | Calanques | spot | 필수 | — | chapters/aix/places.html | Calanques | Calanques National Park |
| `carrieres-de-bibemus` | Carrières de Bibémus | spot | 대체 | — | chapters/aix/places.html | Carrières de Bibémus | fr:Carrières de Bibémus |
| `cassis` | Cassis 항구 | spot | 필수 | Cassis | chapters/aix/places.html | Cassis 항구 | Cassis |
| `cours-mirabeau` | Cours Mirabeau | spot | 필수 | Cours Mirabeau | chapters/aix/places.html | Cours Mirabeau | Cours Mirabeau |
| `grasse` | Grasse | spot | 선택 | — | chapters/aix/places.html | Grasse | Grasse |
| `marseille` | Marseille | spot | 대체 | Marseille Saint-Charles | chapters/aix/places.html | Marseille | Marseille |
| `vieux-port-marseille` | Vieux-Port | spot | 대체 | Vieux-Port | chapters/aix/places.html | Vieux-Port | Old Port of Marseille |
| `le-panier` | Le Panier | spot | 대체 | Le Panier | chapters/aix/places.html | Le Panier | fr:Le Panier |
| `mucem` | Mucem | spot | 대체 | Mucem | chapters/aix/places.html | Mucem | Museum of European and Mediterranean Civilisations |
| `fort-saint-jean` | Fort Saint-Jean | spot | 대체 | Fort Saint-Jean | chapters/aix/places.html | Fort Saint-Jean | Fort Saint-Jean (Marseille) |
| `notre-dame-de-la-garde` | Notre-Dame de la Garde | spot | 선택 | Notre-Dame de la Garde | chapters/aix/places.html | Notre-Dame de la Garde | Notre-Dame de la Garde |
| `montagne-sainte-victoire-terrain-des-peintres` | Montagne Sainte-Victoire · Terrain des Peintres | spot | 우선 추천 | — | chapters/aix/places.html | Montagne Sainte-Victoire · Terrain des Peintres | Montagne Sainte-Victoire |
| `musee-granet` | Musée Granet | spot | 우선 추천 | Musée Granet | chapters/aix/places.html | Musée Granet | Musée Granet |
| `rotonde` | Rotonde | spot | 선택 | Rotonde | chapters/aix/places.html | Rotonde | Fontaine de la Rotonde |
| `saint-paul-de-vence` | Saint-Paul-de-Vence | spot | 우선 추천 | — | chapters/aix/places.html | Saint-Paul-de-Vence | Saint-Paul-de-Vence |
| `place-richelme-place-des-precheurs` | 시장 — Place Richelme · Place des Prêcheurs | spot | 필수 | — | chapters/aix/places.html | 시장 — Place Richelme · Place des Prêcheurs | — |
| `vieil-aix` | Vieil Aix — 구시가지 | spot | 필수 | — | chapters/aix/places.html | Vieil Aix — 구시가지 | fr:Aix-en-Provence |
| `patisserie-weibel` | Pâtisserie Weibel | spot | 필수 | Pâtisserie Weibel | chapters/aix/places.html | Pâtisserie Weibel | — |
| `chez-gilbert-cassis` | Chez Gilbert | spot | 필수 | Chez Gilbert | chapters/aix/places.html | Chez Gilbert | — |

## luberon (08)

| 슬러그 | 이름 | 타입 | 등급 | 지도 핀 | 본문 | 헤딩 | 위키 |
|---|---|---|---|---|---|---|---|
| `abbaye-de-senanque` | Abbaye de Sénanque | spot | 필수 | Abbaye de Sénanque | chapters/luberon/places.html | Abbaye de Sénanque | Sénanque Abbey |
| `bonnieux` | Bonnieux | spot | 선택 | Bonnieux | chapters/luberon/places.html | Bonnieux | Bonnieux |
| `coustellet` | Coustellet 생산자 시장 | spot | 선택 | Coustellet | chapters/luberon/places.html | Coustellet 생산자 시장 | — |
| `gordes` | Gordes | spot | 필수 | Gordes | chapters/luberon/places.html | Gordes | Gordes |
| `goult` | Goult | spot | 선택 | Goult | chapters/luberon/places.html | Goult | Goult |
| `lacoste` | Lacoste | spot | 선택 | Lacoste | chapters/luberon/places.html | Lacoste | Lacoste, Vaucluse |
| `lourmarin` | Lourmarin | spot | 필수 | — | chapters/luberon/places.html | Lourmarin | Lourmarin |
| `l-isle-sur-la-sorgue` | L’Isle-sur-la-Sorgue | spot | 필수 | L’Isle-sur-la-Sorgue | chapters/luberon/places.html | L’Isle-sur-la-Sorgue | L'Isle-sur-la-Sorgue |
| `fontaine-de-vaucluse` | Fontaine-de-Vaucluse | spot | 선택 | Fontaine-de-Vaucluse | chapters/luberon/places.html | Fontaine-de-Vaucluse | Fontaine-de-Vaucluse |
| `menerbes` | Ménerbes | spot | 선택 | Ménerbes | chapters/luberon/places.html | Ménerbes | Ménerbes |
| `oppede-le-vieux` | Oppède-le-Vieux | spot | 선택 | — | chapters/luberon/places.html | Oppède-le-Vieux | Oppède |
| `roussillon-sentier-des-ocres` | Roussillon · Sentier des Ocres | spot | 필수 | Roussillon | chapters/luberon/places.html | Roussillon · Sentier des Ocres | Roussillon, Vaucluse |
| `village-des-bories` | Village des Bories | spot | 우선 추천 | Village des Bories | chapters/luberon/places.html | Village des Bories | Village des Bories |

## avignon (09)

| 슬러그 | 이름 | 타입 | 등급 | 지도 핀 | 본문 | 헤딩 | 위키 |
|---|---|---|---|---|---|---|---|
| `carrieres-des-lumieres` | Carrières des Lumières | spot | 대체 | — | chapters/avignon/places.html | Carrières des Lumières | fr:Carrières de Lumières |
| `glanum` | Glanum | spot | 대체 | — | chapters/avignon/places.html | Glanum | Glanum |
| `les-baux-de-provence` | Les Baux-de-Provence | spot | 필수 | Les Baux | chapters/avignon/places.html | Les Baux-de-Provence | Les Baux-de-Provence |
| `les-halles` | Les Halles | spot | 필수 | Les Halles | chapters/avignon/places.html | Les Halles | Les Halles d'Avignon |
| `palais-des-papes` | Palais des Papes | spot | 필수 | Palais des Papes | chapters/avignon/places.html | Palais des Papes | Palais des Papes |
| `pont-saint-benezet` | Pont Saint-Bénézet | spot | 필수 | Pont Saint-Bénézet | chapters/avignon/places.html | Rocher des Doms · Pont Saint-Bénézet | Pont Saint-Bénézet |
| `pont-du-gard` | Pont du Gard | spot | 필수 | Pont du Gard | chapters/avignon/places.html | Pont du Gard | Pont du Gard |
| `rocher-des-doms` | Rocher des Doms | spot | 필수 | — | chapters/avignon/places.html | Rocher des Doms · Pont Saint-Bénézet | fr:Rocher des Doms |
| `saint-paul-de-mausole` | Saint-Paul-de-Mausole | spot | 대체 | — | chapters/avignon/places.html | Saint-Paul-de-Mausole | Monastery of Saint-Paul de Mausole |
| `orange` | Orange · Théâtre antique | spot | 선택 | Orange | chapters/avignon/places.html | Orange · Théâtre antique | Orange, Vaucluse |
| `saint-remy-de-provence` | Saint-Rémy-de-Provence | spot | 필수 | Saint-Rémy | chapters/avignon/places.html | Saint-Rémy-de-Provence | Saint-Rémy-de-Provence |
| `uzes` | Uzès Place aux Herbes·구시가지 | spot | 필수 | Uzès | chapters/avignon/places.html | Uzès Place aux Herbes·구시가지 | Uzès |
| `arles` | Arles | spot | 필수 | Arles | chapters/avignon/places.html | Arles | Arles |
| `arenes-d-arles` | Arènes d’Arles | spot | 필수 | Arènes d’Arles | chapters/avignon/places.html | Arènes d’Arles | Arles Amphitheatre |
| `theatre-antique-arles` | Théâtre antique | spot | 필수 | Théâtre antique | chapters/avignon/places.html | Théâtre antique | Roman Theatre of Arles |
| `place-du-forum-arles` | Place du Forum | spot | 우선 추천 | Place du Forum | chapters/avignon/places.html | Place du Forum | — |
| `cloitre-saint-trophime` | Cloître Saint-Trophime | spot | 우선 추천 | Cloître Saint-Trophime | chapters/avignon/places.html | Cloître Saint-Trophime | — |
| `fondation-vincent-van-gogh-arles` | Fondation Vincent van Gogh Arles | spot | 선택 | Fondation Vincent van Gogh | chapters/avignon/places.html | Fondation Vincent van Gogh Arles | — |
| `la-roquette` | La Roquette | spot | 우선 추천 | La Roquette | chapters/avignon/places.html | La Roquette | — |
| `fou-de-fafa-avignon` | Fou de Fafa | spot | 필수 | Fou de Fafa | chapters/avignon/places.html | Fou de Fafa | — |
| `les-cocottes-saint-louis` | Les Cocottes Saint-Louis | spot | 필수 | Les Cocottes Saint-Louis | chapters/avignon/places.html | Les Cocottes Saint-Louis | — |
| `le-gibolin-arles` | Le Gibolin | spot | 필수 | Le Gibolin | chapters/avignon/places.html | Le Gibolin | — |
| `arenes-de-nimes` | Arènes de Nîmes | spot | 필수 | Arènes de Nîmes | chapters/avignon/places.html | Arènes de Nîmes | fr:Arènes de Nîmes |
| `maison-carree` | Maison Carrée | spot | 필수 | Maison Carrée | chapters/avignon/places.html | Maison Carrée | Maison Carrée |

## lyon (10)

| 슬러그 | 이름 | 타입 | 등급 | 지도 핀 | 본문 | 헤딩 | 위키 |
|---|---|---|---|---|---|---|---|
| `annecy` | Annecy 구시가지 | spot | 필수 | Annecy | chapters/lyon/places.html | Annecy 구시가지 | Annecy |
| `bellecour` | Bellecour | spot | 우선 추천 | Bellecour | chapters/lyon/places.html | Bellecour | Place Bellecour |
| `croix-rousse` | Croix-Rousse | spot | 필수 | Croix-Rousse | chapters/lyon/places.html | Croix-Rousse | La Croix-Rousse |
| `fourviere` | Fourvière | spot | 필수 | Fourvière | chapters/lyon/places.html | Fourvière | Basilica of Notre-Dame de Fourvière |
| `halles-de-lyon-paul-bocuse` | Halles de Lyon Paul Bocuse | spot | 필수 | Halles Paul Bocuse | chapters/lyon/places.html | Halles de Lyon Paul Bocuse | Les Halles de Lyon-Paul Bocuse |
| `parc-de-la-tete-d-or` | Parc de la Tête d'Or | spot | 우선 추천 | Parc Tête d’Or | chapters/lyon/places.html | Parc de la Tête d'Or | Parc de la Tête d'or |
| `vieux-lyon` | Vieux Lyon · 트라불 | spot | 필수 | Vieux Lyon | chapters/lyon/places.html | Vieux Lyon · 트라불 | Vieux Lyon |
| `cafe-comptoir-abel` | Café Comptoir Abel | spot | 필수 | Café Comptoir Abel | chapters/lyon/places.html | Café Comptoir Abel | — |
| `daniel-et-denise` | Daniel et Denise | spot | 필수 | Daniel et Denise | chapters/lyon/places.html | Daniel et Denise | — |
| `chez-mamie-lise` | Chez Mamie Lise | spot | 필수 | Chez Mamie Lise | chapters/lyon/places.html | Chez Mamie Lise | — |

## paris (11)

| 슬러그 | 이름 | 타입 | 등급 | 지도 핀 | 본문 | 헤딩 | 위키 |
|---|---|---|---|---|---|---|---|
| `bnf-richelieu` | BnF Richelieu | spot | 우선 추천 | BnF Richelieu | chapters/paris/places.html | BnF Richelieu | Bibliothèque nationale de France |
| `bourse-de-commerce-pinault-collection` | Bourse de Commerce — Pinault Collection | spot | 필수 | Bourse de Commerce | chapters/paris/places.html | Bourse de Commerce — Pinault Collection | Bourse de Commerce |
| `centre-pompidou` | Centre Pompidou | spot | 비추천 | — | chapters/paris/places.html | Centre Pompidou | Centre Pompidou |
| `giverny` | Giverny | spot | 우선 추천 | Giverny | chapters/paris/places.html | Giverny — Day 41 A안 | Giverny |
| `grand-palais` | Grand Palais | spot | 필수 | Grand Palais | chapters/paris/places.html | Cezanne et nous — Grand Palais | Grand Palais |
| `latin-quarter` | Latin Quarter | spot | 필수 | — | chapters/paris/places.html | Latin Quarter | Latin Quarter, Paris |
| `le-marais` | Le Marais | spot | 필수 | — | chapters/paris/places.html | Le Marais | The Marais |
| `montmartre-south-pigalle` | Montmartre · South Pigalle | spot | 필수 | Montmartre | chapters/paris/places.html | Montmartre · South Pigalle | Montmartre |
| `montorgueil` | Montorgueil | spot | 우선 추천 | — | chapters/paris/places.html | Montorgueil | Rue Montorgueil |
| `musee-carnavalet` | Musée Carnavalet | spot | 필수 | Carnavalet | chapters/paris/places.html | Musée Carnavalet | Musée Carnavalet |
| `musee-d-art-moderne-de-paris` | Musée d'Art Moderne de Paris | spot | 필수 | MAM | chapters/paris/places.html | Musée d'Art Moderne de Paris | Musée d'Art Moderne de Paris |
| `musee-d-orsay` | Musée d'Orsay | spot | 필수 | Orsay | chapters/paris/places.html | Mary Cassatt. L'indépendante — Musée d'Orsay | Musée d'Orsay |
| `musee-de-l-orangerie` | Musée de l'Orangerie | spot | 필수 | Orangerie | chapters/paris/places.html | Musée de l'Orangerie | Musée de l'Orangerie |
| `musee-du-louvre` | Musée du Louvre | spot | 필수 | Louvre | chapters/paris/places.html | Musée du Louvre | Louvre |
| `musee-du-luxembourg` | Musée du Luxembourg | spot | 필수 | Luxembourg Museum | chapters/paris/places.html | Musée du Luxembourg | Musée du Luxembourg |
| `musee-guimet` | Musée Guimet | spot | 필수 | Guimet | chapters/paris/places.html | Musée Guimet | Guimet Museum |
| `musee-gustave-moreau` | Musée Gustave Moreau | spot | 필수 | Gustave Moreau | chapters/paris/places.html | Musée Gustave Moreau | Musée Gustave Moreau |
| `musee-jacquemart-andre` | Musée Jacquemart-André | spot | 필수 | Jacquemart-André | chapters/paris/places.html | Musée Jacquemart-André | Musée Jacquemart-André |
| `musee-marmottan-monet` | Musée Marmottan Monet | spot | 필수 | Marmottan Monet | chapters/paris/places.html | Musée Marmottan Monet | Musée Marmottan Monet |
| `musee-picasso-paris` | Musée Picasso Paris | spot | 필수 | Picasso | chapters/paris/places.html | Musée Picasso Paris | Musée Picasso |
| `musee-rodin` | Musée Rodin | spot | 필수 | Rodin | chapters/paris/places.html | Musée Rodin | Musée Rodin |
| `notre-dame-de-paris` | Notre-Dame de Paris | spot | 필수 | Notre-Dame | chapters/paris/places.html | Notre-Dame de Paris | Notre-Dame de Paris |
| `petit-palais` | Petit Palais | spot | 필수 | Petit Palais | chapters/paris/places.html | Petit Palais | Petit Palais |
| `versailles` | Versailles | spot | 필수 | Versailles | chapters/paris/places.html | Versailles — Day 36 A안 | Palace of Versailles |
| `boulangerie-pichard` | Boulangerie Pichard | spot | 필수 | Boulangerie Pichard | chapters/paris/places.html | Boulangerie Pichard | — |
| `marche-convention` | Marché Convention | spot | 필수 | Marché Convention | chapters/paris/places.html | Marché Convention | — |
| `cafe-du-commerce` | Café du Commerce | spot | 필수 | Café du Commerce | chapters/paris/places.html | Café du Commerce | — |
| `le-grand-pan` | Le Grand Pan | spot | 필수 | Le Grand Pan | chapters/paris/places.html | Le Grand Pan | — |
| `bouillon-chartier-montparnasse` | Bouillon Chartier Montparnasse | spot | 필수 | Bouillon Chartier Montparnasse | chapters/paris/places.html | Bouillon Chartier Montparnasse | — |

---

**spot 94 · node 3 · 등급 미정 2(그중 원고 충돌 0)**

`*` 는 등급을 본문 헤딩이 아니라 추천등급 표에서 가져왔다는 표시다.

## 판단이 들어간 곳

기계로 못 가른 것과 그 근거다.

- **Collioure** — 요약표는 '우선 추천', 상세표(장소|등급)는 '필수'다. 상세표가 더 구체적이고 본문이 Day 5 의 축으로 다룬다.
- **Rotonde · Bellecour** — 등급 미정으로 둔다. 원고가 `Presqu’île·Bellecour·Jacobins`
  라는 권역에만 등급을 매겼고 광장 단독 등급이 아니다. Rotonde 는 근거가 없다.
- **역·공항 3곳** — `node` 로 두고 장소 페이지를 만들지 않는다. 지도와 일정에서만 참조한다.
- **`15구 생활일` · `월요일 모듈`** — 등급이 붙어 있지만 하루의 성격이지 갈 곳이 아니다. 뺐다.
- **전시 헤딩 2건** — 전시는 시한이 있고 장소는 남는다. Grand Palais · Musée d’Orsay 로 접었다.
- **`Rocher des Doms · Pont Saint-Bénézet`** — 헤딩 하나에 장소가 둘이라 갈랐다.
- **Lourmarin** — aix(경유)·luberon(정본) 두 행이던 것을 luberon 한 행으로
  합쳤다(2026-08-03). 같은 마을에 페이지가 두 장 생기던 문제. 옛 주소
  `places/lourmarin-2.html` 은 빌드가 리다이렉트로 남긴다. 핀은 Aix 전환일
  지도에 있고, Google Maps 링크는 이름 대조로 이어진다.
