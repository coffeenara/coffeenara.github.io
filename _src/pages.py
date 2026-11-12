"""페이지별 본문. build(S, E, X)가 페이지 목록을 돌려줍니다."""


def fig(E, img, alt, cap, cls=""):
    return (f'<figure class="{cls}"><img src="/assets/img/{img}" alt="{E(alt)}" loading="lazy">'
            f'<figcaption>{E(cap)}</figcaption></figure>')


def notes(E, b):
    return "".join(f"<li>{E(n)}</li>" for n in b["notes"])


def blend_card(S, E, b, link=True):
    more = f'<a class="more" href="/blends/#{b["id"]}">블렌드 자세히 보기</a>' if link else ""
    return f"""<article class="blend" id="{b['id']}">
<img src="/assets/img/{b['img']}" alt="{E(b['name'])} 카드. 생두 마대 사진 위에 커핑 노트 {E(', '.join(b['notes']))}와 블렌드 설명" loading="lazy">
<div class="blend-body">
<h3>{E(b['name'])} <small>{E(b['short'])}</small></h3>
<p class="label">커핑 노트</p>
<ul class="chips">{notes(E, b)}</ul>
<p>{E(b['desc'])}</p>
{more}
</div>
</article>"""


def facts_strip(S, E):
    return f"""<dl class="facts">
<div><dt>방문 샘플 테스트·세팅</dt><dd>100% 무료</dd></div>
<div><dt>신청 조건</dt><dd>월 {S.MIN_KG}kg 이상 사용</dd></div>
<div><dt>원두 가격</dt><dd>1kg {S.won(S.PRICE_MIN)}~{S.won(S.PRICE_MAX)}</dd></div>
<div><dt>발송</dt><dd>주문 후 영업일 1~2일 안에 로스팅해 택배</dd></div>
</dl>"""


STEPS = [
    ("상담 신청", "카카오톡으로 매장 지역과 한 달 원두 사용량을 알려 주시면 방문 일정을 잡습니다."),
    ("방문 테스트", "매장의 머신과 그라인더로 여러 원두를 추출해 함께 맛보고, 가장 좋은 맛이 나도록 세팅합니다."),
    ("맞춤 제안", "매장의 메뉴와 원하는 맛, 목표 단가에 맞는 블렌드를 추천하고, 교육과 컨설팅도 무료로 해 드립니다."),
]


def steps(E):
    return '<ol class="steps">' + "".join(
        f"<li><strong>{E(t)}</strong><span>{E(d)}</span></li>" for t, d in STEPS) + "</ol>"


ORIGIN = {
    "kenya": ("케냐", "2024년 2월", "케냐 중부의 가공소와 나이로비의 수출 창고, 커핑실을 찾았습니다.", [
        ("kenya-washing-channel.jpg", "경사진 수로를 따라 흘러가는 파치먼트 생두와 가공소 건물",
         "케냐 중부의 가공소. 수로를 따라 파치먼트가 흘러갑니다."),
        ("kenya-drying-beds.jpg", "아프리칸 베드 위에 펼쳐 말리는 파치먼트를 살펴보는 사람들",
         "아프리칸 베드에서 말리는 파치먼트를 직접 확인합니다."),
        ("kenya-coffee-cherries.jpg", "커피나무 가지에 달린 익기 전 초록색 커피 체리",
         "익어 가는 커피 체리."),
        ("kenya-export-warehouse.jpg", "나이로비 수출 창고에서 PRODUCE OF KENYA가 찍힌 생두 마대를 확인하는 사람들",
         "나이로비의 수출 창고. 케냐산 생두 마대를 확인합니다."),
        ("kenya-cupping-lab.jpg", "커핑실 테이블에 늘어선 생두 샘플과 커핑 준비",
         "커핑실에서 샘플을 맛보고 고릅니다."),
    ]),
    "guatemala": ("과테말라", "2017년 2월", "과테말라의 농장과 건조장, 수출용 생두 창고를 찾았습니다.", [
        ("guatemala-patio-drying.jpg", "넓은 파티오에서 갈퀴로 파치먼트를 고르게 펴 말리는 작업자",
         "파티오에서 파치먼트를 고르게 펴 말립니다."),
        ("guatemala-sacramento-farm.jpg", "커피나무 사이에 세워진 Sacramento 농장 구역 표지판",
         "농장 구역 표지판(Sacramento)."),
        ("guatemala-green-beans.jpg", "손바닥 위에 올린 파치먼트 상태의 커피콩",
         "손에 올려 상태를 확인합니다."),
        ("guatemala-lot-sacks.jpg", "로트 정보가 적힌 표가 붙은 생두 마대 더미",
         "로트 정보가 붙은 생두 마대."),
        ("guatemala-hand-sorting.jpg", "작업대 위 생두에서 결점두를 손으로 골라내는 작업자",
         "결점두를 손으로 골라내는 핸드 소팅."),
    ]),
    "ethiopia": ("에티오피아", "2020년 1월", "에티오피아 남부 산지의 건조장을 찾았습니다.", [
        ("ethiopia-raised-beds.jpg", "아프리칸 베드 위에서 커피 체리를 말리며 고르는 사람들",
         "아프리칸 베드에서 체리째 말리는 내추럴 가공."),
        ("ethiopia-natural-drying.jpg", "산비탈 건조장에 넓게 펼쳐 말리는 붉은 커피 체리",
         "산비탈 건조장에서 말라 가는 커피 체리."),
        ("ethiopia-cherry-sorting.jpg", "건조대 위에서 손으로 체리를 고르는 작업자들",
         "건조대 위에서 체리를 고릅니다."),
        ("ethiopia-dried-cherries.jpg", "자루에 담긴 다 마른 커피 체리를 보여 주는 생산자",
         "다 마른 커피 체리."),
    ]),
}


def origin_section(E, key, full=True):
    name, when, lead, photos = ORIGIN[key]
    shown = photos if full else photos[:1]
    figs = "".join(fig(E, i, a, c) for i, a, c in shown)
    return f"""<section class="origin" id="{key}">
<h2>{E(name)} <small>{E(when)} 방문</small></h2>
<p>{E(lead)}</p>
<div class="gallery">{figs}</div>
</section>"""


def build(S, E, X):
    pages = []

    # ── 홈 ───────────────────────────────────────────────
    home = f"""<section class="hero">
<div class="hero-text">
<p class="eyebrow">Coffee Nara · 커피나라</p>
<h1>매장에서 직접 맛보고 고르는<br>카페 원두</h1>
<p class="lead">커피나라는 생두를 직접 수입하고, 그 생두를 로스팅해 카페에 원두를 납품합니다. 매장에 찾아가 샘플 테스트를 100% 무료로 해 드립니다.
신청비도, 환급 조건도 없습니다. 월 {S.MIN_KG}kg 이상만 사용하셔도 방문합니다. 원두의 맛과 단가, 두 가지 모두 만족을 약속드립니다.</p>
<a class="btn" href="{E(S.CONTACT_URL)}" target="_blank" rel="noopener">{E(S.CONTACT_LABEL)}</a>
</div>
<img class="hero-img" src="/assets/img/roaster.webp" alt="로스터 냉각판에서 막 볶은 원두가 돌며 식는 모습(움직이는 이미지)" width="480" height="254" fetchpriority="high">
</section>
{facts_strip(S, E)}

<section class="split">
{fig(E, "hand-drip.jpg", "드리퍼에 뜨거운 물을 부어 원두를 추출하는 핸드드립", "")}
<div>
<h2>맛있는 커피는 좋은 원두에서 시작합니다</h2>
<p>로스팅은 농부의 땀과 손길로 태어난 생두 안에 갖춰진 수천 가지 향미를 커피 한 잔으로 이야기하는 과정이라고 생각합니다.</p>
<p>다양한 시그니처 블렌드로, 맛이라면 맛, 가격이라면 가격, 원하시는 쪽에 맞춰 드립니다.</p>
<p class="pull">매일 수백, 수천 잔을 추출해도 고객에게는 단 한 잔의 커피입니다.</p>
<p>모든 커피가 맛있을 수 있도록, 좋은 커피 동반자로 같이 걸어가겠습니다.</p>
</div>
</section>

<section>
<h2>무료 방문 샘플 테스트는 세 단계로 진행됩니다</h2>
<p>방문 테스트는 20년 이상 로스팅하고 15년 이상 커피 교육을 해 온 담당자가 직접 진행합니다.</p>
{steps(E)}
<div class="gallery two">
{fig(E, "espresso-extraction.jpg", "방문 테스트 중 매장의 에스프레소 머신에서 두 잔으로 추출되는 에스프레소", "실제 매장 방문 테스트. 그 매장의 머신으로 추출합니다.")}
{fig(E, "store-test-espresso.jpg", "방문 테스트 중 매장 머신의 포터필터에서 샷 잔으로 떨어지는 에스프레소", "다른 매장의 방문 테스트.")}
</div>
<p><a class="more" href="/free-test/">방문 테스트 조건과 지역 보기</a></p>
</section>

<section>
<h2>대표 블렌드 두 가지, 그리고 수십 가지 맞춤 블렌드</h2>
<div class="blends">{''.join(blend_card(S, E, b) for b in S.BLENDS)}</div>
</section>

<section class="split">
{fig(E, "kenya-drying-beds.jpg", "케냐 가공소의 아프리칸 베드 위 파치먼트를 살펴보는 사람들", "케냐 중부 가공소, 2024년 2월")}
<div>
<h2>생두는 직접 수입합니다</h2>
<p>커피나라는 생두 수입 회사입니다. 케냐, 과테말라, 에티오피아의 농장과 가공소, 수출 창고를 직접 찾아가 생두를 보고 커핑합니다.
블렌드별 배합 비율과 원산지 구성은 커피나라의 레시피라 공개하지 않습니다.</p>
<a class="more" href="/origin/">산지 사진 보기</a>
</div>
</section>
"""
    pages.append(dict(
        path="/",
        title="커피나라 Coffee Nara | 생두 수입 · 카페 원두 납품 · 무료 방문 샘플 테스트",
        description=f"커피나라는 생두를 직접 수입해 로스팅하고 카페에 원두를 납품하는 회사입니다. 월 {S.MIN_KG}kg 이상 "
                    f"매장에 찾아가 무료로 샘플 테스트를 합니다. 원두 {S.PRICE_TEXT}.",
        body=home,
        faq=["about", "visit", "free_cost", "min", "price", "ship", "new_store", "unsatisfied"],
        schema=[{"@type": "WebPage", "@id": S.BASE + "/#webpage", "url": S.BASE + "/",
                 "name": "커피나라 | 카페 원두 납품 · 무료 방문 샘플 테스트", "inLanguage": "ko",
                 "about": {"@id": S.BASE + "/#org"}, "isPartOf": {"@id": S.BASE + "/#website"},
                 "dateModified": X.LASTMOD}],
    ))

    # ── 블렌드 ───────────────────────────────────────────
    rows = "".join(
        f"<tr><th scope=\"row\">{E(b['name'])}<br><small>{E(b['short'])}</small></th>"
        f"<td>{E(', '.join(b['notes']))}</td><td>{E(b['desc'])}</td></tr>" for b in S.BLENDS)
    blends = f"""<p class="eyebrow">원두 블렌드</p>
<h1>커피나라 원두 블렌드: Premium Blend와 Special Blend</h1>
<p class="lead">커피나라의 대표 블렌드는 두 가지입니다. 이 밖에도 수십 가지 블렌드를 갖추고 있어, 매장의 메뉴와 원하는 맛, 단가에 맞춰 세팅해 드립니다.</p>
<div class="table-wrap"><table>
<caption>커피나라 대표 블렌드 비교</caption>
<thead><tr><th scope="col">블렌드</th><th scope="col">커핑 노트</th><th scope="col">특징</th></tr></thead>
<tbody>{rows}</tbody>
</table></div>
<div class="blends">{''.join(blend_card(S, E, b, link=False) for b in S.BLENDS)}</div>

<section>
<h2>가격과 발송</h2>
{facts_strip(S, E)}
<p>원두 가격은 {S.PRICE_TEXT}이며 블렌드에 따라 다릅니다. 주문을 받은 뒤 영업일 기준 1~2일 안에 로스팅해 택배로 보냅니다.</p>
</section>

<section class="split">
{fig(E, "coffee-cherries-sorting.jpg", "건조대 가득 펼쳐진 붉은 커피 체리를 손으로 고르는 두 사람", "건조대에서 커피 체리를 고르는 모습.")}
<div>
<h2>배합은 공개하지 않습니다</h2>
<p>커핑 노트와 맛의 방향은 위에 적은 그대로입니다. 블렌드마다 어떤 생두를 어떤 비율로 섞는지는 커피나라의 레시피라 공개하지 않습니다.
매장에 맞는 블렌드는 <a href="/free-test/">무료 방문 테스트</a>에서 직접 맛보고 고르실 수 있습니다.</p>
</div>
</section>
"""
    pages.append(dict(
        path="/blends/", crumb="원두 블렌드",
        title="커피나라 원두 블렌드 | Premium Blend · Special Blend 커핑 노트",
        description="커피나라 대표 블렌드 Premium Blend(다크 초콜릿, 플로랄, 오렌지, 견과류)와 Special Blend(아몬드, "
                    f"오렌지, 바나나, 바닐라, 깔끔한 산미). 원두 {S.PRICE_TEXT}, 수십 가지 블렌드 맞춤 세팅.",
        body=blends,
        faq=["blends", "custom", "price", "ship", "origin"],
        schema=[{"@type": "CollectionPage", "@id": S.BASE + "/blends/#webpage", "url": S.BASE + "/blends/",
                 "name": "커피나라 원두 블렌드", "inLanguage": "ko", "isPartOf": {"@id": S.BASE + "/#website"},
                 "hasPart": [{"@id": f"{S.BASE}/blends/#{b['id']}"} for b in S.BLENDS]}]
        + [X.product_schema(b) for b in S.BLENDS],
        image="premium-blend-card.jpg",
        image_alt="Premium Blend 카드. 과테말라 생두 마대 사진 위에 커핑 노트와 블렌드 설명",
    ))

    # ── 무료 방문 테스트 ─────────────────────────────────
    region_rows = "".join(
        f"<tr><th scope=\"row\">{E(g)}</th><td>{E(', '.join(lst))}</td><td>방문 가능</td></tr>"
        for g, lst in S.REGIONS)
    free = f"""<p class="eyebrow">무료 방문 샘플 테스트</p>
<h1>무료 방문 커피 샘플 테스트</h1>
<p class="lead">새 원두를 고를 때 가장 확실한 방법은 내 매장의 머신과 그라인더로 직접 내려 보는 것입니다.
커피나라가 매장에 찾아가 여러 원두를 추출해 드리고, 함께 맛본 뒤 그 매장에서 가장 좋은 맛이 나도록 세팅하고 블렌드를 제안합니다.
테스트는 100% 무료입니다. 먼저 비용을 내고 나중에 돌려받는 방식이 아니고, 로스터리에서 몇 km 안이라는 거리 제한도 없습니다.</p>

<div class="table-wrap"><table>
<caption>무료 방문 샘플 테스트 조건</caption>
<tbody>
<tr><th scope="row">비용</th><td>100% 무료. 신청비·보증금 없음, 주문량에 따른 환급 조건 없음</td></tr>
<tr><th scope="row">세팅·교육</th><td>매장의 머신과 그라인더에 맞춘 세팅, 20년 이상 로스팅하고 15년 이상 커피 교육을 해 온 담당자의 무료 교육·컨설팅</td></tr>
<tr><th scope="row">대상</th><td>한 달 원두 사용량 {S.MIN_KG}kg 이상인 카페·매장, 오픈을 준비하는 매장</td></tr>
<tr><th scope="row">지역</th><td>제주도와 배로만 갈 수 있는 섬을 뺀 전국</td></tr>
<tr><th scope="row">진행</th><td>상담 신청 → 매장 방문 테스트 → 맞춤 블렌드 제안</td></tr>
<tr><th scope="row">신청</th><td><a href="{E(S.CONTACT_URL)}" target="_blank" rel="noopener">{E(S.CONTACT_LABEL)}</a></td></tr>
</tbody>
</table></div>
<p>원두를 바꾸고 싶은데 단골 반응이 걱정된다면 <a href="/guide/switching-cafe-beans/">카페 원두 바꾸면 손님이 떠날까</a>를 먼저 읽어 보세요.</p>

<section>
<h2>진행 순서</h2>
{steps(E)}
<div class="gallery two">
{fig(E, "store-test-espresso.jpg", "방문 테스트 중 매장 머신의 포터필터에서 샷 잔으로 떨어지는 에스프레소", "실제 매장 방문 테스트. 그 매장의 머신과 그라인더로 추출합니다.")}
</div>
</section>

<section class="split">
{fig(E, "espresso-extraction.jpg", "방문 테스트 중 매장의 에스프레소 머신에서 두 잔으로 추출되는 에스프레소", "실제 매장 방문 테스트.")}
<div>
<h2>새로 카페를 여는 분도 신청할 수 있습니다</h2>
<p>오픈을 준비하는 단계라면 예상 사용량과 원하는 맛, 목표 단가를 알려 주세요. 테스트는 매장의 커피 머신으로 하므로, 머신이 설치된 뒤 일정을 잡아 찾아갑니다. 메뉴 구성에 맞는 블렌드를 함께 고릅니다.</p>
<p>한 달 {S.MIN_KG}kg은 에스프레소 더블샷에 원두 18~20g을 쓸 때 약 500~550잔, 하루 평균 17~18잔입니다.
사용량 계산은 <a href="/guide/choose-bean-supplier/">카페 원두 납품 업체 고르는 법</a>에 정리해 두었습니다.</p>
</div>
</section>

<section>
<h2>제주도와 배로만 갈 수 있는 섬을 뺀 전국에 방문합니다</h2>
<p>서울이나 부산 같은 대도시뿐 아니라 담양, 순천, 경주, 강릉, 공주 같은 시·군 지역에도 방문합니다. 거제도나 강화도처럼 다리로 이어져 차로 갈 수 있는 섬도 방문합니다.</p>
<div class="table-wrap"><table>
<caption>방문 가능 지역</caption>
<thead><tr><th scope="col">권역</th><th scope="col">시·도</th><th scope="col">방문 테스트</th></tr></thead>
<tbody>{region_rows}
<tr><th scope="row">다리로 이어진 섬</th><td>거제도, 강화도, 진도, 남해, 완도 등 차로 갈 수 있는 섬</td><td>방문 가능</td></tr>
<tr><th scope="row">제주·섬</th><td>제주특별자치도, 배로만 갈 수 있는 섬</td><td>방문 불가</td></tr>
</tbody>
</table></div>
</section>
"""
    pages.append(dict(
        path="/free-test/", crumb="무료 방문 테스트",
        title="무료 방문 커피 샘플 테스트 | 전국 카페 방문(제주·배편 섬 제외) · 커피나라",
        description=f"커피나라가 카페에 직접 찾아가 원두를 추출해 함께 맛보고 블렌드를 제안합니다. 무료, 월 {S.MIN_KG}kg 이상 "
                    "사용 매장, 서울·부산·대구·광주·대전 등 제주도와 배로만 갈 수 있는 섬을 뺀 전국, 오픈 준비 매장도 신청 가능.",
        body=free,
        faq=["visit", "free_cost", "education", "store_diff", "region", "region_small", "bridge", "new_store", "min",
             "unsatisfied", "contact"],
        schema=[X.service_schema(), X.education_schema()],
        image="espresso-extraction.jpg",
        image_alt="방문 테스트 중 매장의 에스프레소 머신에서 두 잔으로 추출되는 에스프레소",
    ))

    # ── 생두 직접 수입 ───────────────────────────────────
    origin = f"""<p class="eyebrow">생두 직접 수입</p>
<h1>생두 직접 수입: 케냐·과테말라·에티오피아 산지에서</h1>
<p class="lead">커피나라는 생두를 직접 수입하는 회사입니다. 산지의 농장과 가공소, 수출 창고를 직접 찾아가 생두가 어떻게 길러지고 가공되는지 보고,
커핑으로 맛을 확인한 뒤 들여옵니다. 아래는 산지에서 직접 찍은 사진입니다.</p>
<div class="table-wrap"><table>
<caption>커피나라 산지 방문 기록</caption>
<thead><tr><th scope="col">나라</th><th scope="col">방문</th><th scope="col">본 곳</th></tr></thead>
<tbody>
<tr><th scope="row">과테말라</th><td>2017년 2월</td><td>농장, 파티오 건조장, 수출용 생두 창고</td></tr>
<tr><th scope="row">에티오피아</th><td>2020년 1월</td><td>남부 산지 건조장(내추럴 가공)</td></tr>
<tr><th scope="row">케냐</th><td>2024년 2월</td><td>중부 가공소, 나이로비 수출 창고와 커핑실</td></tr>
</tbody>
</table></div>
{origin_section(E, "kenya")}
{origin_section(E, "guatemala")}
{origin_section(E, "ethiopia")}
<p class="note">블렌드마다 어느 산지의 생두를 얼마나 쓰는지는 공개하지 않습니다.</p>
"""
    pages.append(dict(
        path="/origin/", crumb="생두 직접 수입",
        title="생두 직접 수입 | 케냐·과테말라·에티오피아 산지 방문 · 커피나라",
        description="커피나라는 생두를 직접 수입합니다. 케냐(2024), 과테말라(2017), 에티오피아(2020)의 농장, 가공소, "
                    "수출 창고를 찾아가 생두를 보고 커핑한 기록과 사진.",
        body=origin,
        faq=["origin", "about", "blends"],
        schema=[{"@type": "WebPage", "@id": S.BASE + "/origin/#webpage", "url": S.BASE + "/origin/",
                 "name": "커피나라 생두 직접 수입", "inLanguage": "ko", "about": {"@id": S.BASE + "/#org"},
                 "primaryImageOfPage": S.BASE + "/assets/img/kenya-drying-beds.jpg"}],
        image="kenya-drying-beds.jpg",
        image_alt="케냐 가공소의 아프리칸 베드 위 파치먼트를 살펴보는 사람들",
    ))

    # ── FAQ ──────────────────────────────────────────────
    pages.append(dict(
        path="/faq/", crumb="자주 묻는 질문",
        title="자주 묻는 질문 | 카페 원두 납품 · 방문 테스트 · 가격 · 발송 · 커피나라",
        description=f"커피나라 원두 납품과 무료 방문 샘플 테스트에 관한 질문과 답. 신청 조건(월 {S.MIN_KG}kg), 방문 지역(제주도와 배로만 갈 수 있는 섬을 뺀 "
                    f"전국), 원두 가격({S.PRICE_TEXT}), 발송(주문 후 영업일 1~2일), 블렌드.",
        body="""<p class="eyebrow">자주 묻는 질문</p>
<h1>커피나라 자주 묻는 질문</h1>
<p class="lead">원두 납품, 무료 방문 샘플 테스트, 가격과 발송에 관해 많이 받는 질문을 모았습니다.</p>""",
        faq=list(S.FAQ.keys()),
    ))

    # ── 가이드 ───────────────────────────────────────────
    def cup(price, g):
        return round(price / (1000 / g), -1)

    cost_rows = "".join(
        f"<tr><th scope=\"row\">{S.won(p)}</th><td>약 {int(cup(p, 18)):,}원</td><td>약 {int(cup(p, 20)):,}원</td></tr>"
        for p in (20000, 30000, 45000))
    guide = f"""<p class="eyebrow">가이드 · 카페 운영</p>
<h1>카페 원두 납품 업체 고를 때 확인할 다섯 가지</h1>
<p class="meta">커피나라 · 2026-11-12</p>
<p class="lead">카페를 새로 열거나 원두를 바꾸려고 할 때, 업체 홈페이지의 커핑 노트만으로는 결정하기 어렵습니다.
사용량, 잔당 원가, 매장에서의 맛, 로스팅에서 받기까지의 기간, 블렌드 선택지를 차례로 확인하면 비교가 쉬워집니다.</p>

<h2>한 달 사용량부터 계산합니다</h2>
<p>에스프레소 더블샷 한 잔에 원두 18~20g을 쓰면 1kg으로 약 50~55잔이 나옵니다. 한 달 10kg이면 약 500~550잔, 30일로 나누면 하루 17~18잔입니다.
많은 납품 업체가 월 사용량을 기준으로 조건을 정하기 때문에, 이 숫자를 먼저 알아 두면 상담이 빨라집니다.</p>

<h2>1kg 단가를 잔당 원두 원가로 바꿔 봅니다</h2>
<p>1kg 단가가 같아도 한 잔에 쓰는 양에 따라 원가가 달라집니다. 메뉴 가격을 정할 때는 잔당 원가로 보는 편이 정확합니다.</p>
<div class="table-wrap"><table>
<caption>1kg 단가별 잔당 원두 원가(10원 단위 반올림)</caption>
<thead><tr><th scope="col">1kg 단가</th><th scope="col">한 잔 18g</th><th scope="col">한 잔 20g</th></tr></thead>
<tbody>{cost_rows}</tbody>
</table></div>
<p>커피나라 원두는 {S.PRICE_TEXT}이므로 잔당 원두 원가는 약 360원에서 900원 사이입니다.</p>

<h2>내 매장 장비로 맛봅니다</h2>
<p>같은 원두라도 머신, 그라인더, 물, 추출 레시피에 따라 맛이 달라집니다. 샘플을 받아 다른 곳에서 마셔 보는 것보다
실제로 쓸 매장 장비로 내려 보는 것이 가장 확실합니다. 커피나라는 이 때문에 <a href="/free-test/">매장 방문 샘플 테스트</a>를 무료로 합니다.</p>
{fig(E, "store-test-espresso.jpg", "방문 테스트 중 매장 머신의 포터필터에서 샷 잔으로 떨어지는 에스프레소", "커피나라의 매장 방문 테스트. 그 매장의 머신으로 추출합니다.")}

<h2>로스팅에서 받기까지 며칠 걸리는지 묻습니다</h2>
<p>주문을 받고 볶는지, 볶아 둔 원두를 보내는지, 받기까지 며칠이 걸리는지 확인합니다.
커피나라는 주문 후 영업일 기준 1~2일 안에 로스팅해 택배로 보냅니다.</p>

<h2>블렌드 선택지와 생두 출처를 봅니다</h2>
<p>대표 블렌드 한두 가지만 있는 곳보다 선택지가 많은 곳이 메뉴와 단가에 맞추기 쉽습니다.
생두를 어떻게 들여오는지도 맛의 일관성과 관련이 있습니다. 커피나라는 대표 블렌드 두 가지(<a href="/blends/">Premium Blend, Special Blend</a>) 외에
수십 가지 블렌드를 갖추고 있고, 생두를 <a href="/origin/">직접 수입</a>합니다.</p>

<div class="table-wrap"><table>
<caption>확인할 항목과 커피나라의 답</caption>
<thead><tr><th scope="col">확인할 것</th><th scope="col">커피나라</th></tr></thead>
<tbody>
<tr><th scope="row">신청 조건</th><td>한 달 원두 사용량 {S.MIN_KG}kg 이상</td></tr>
<tr><th scope="row">1kg 단가</th><td>{S.won(S.PRICE_MIN)}~{S.won(S.PRICE_MAX)}</td></tr>
<tr><th scope="row">매장 테스트</th><td>100% 무료 방문 샘플 테스트와 세팅(신청비·환급 조건 없음), 제주도와 배로만 갈 수 있는 섬을 뺀 전국</td></tr>
<tr><th scope="row">교육·컨설팅</th><td>원두 납품 매장에 무료(20년 이상 로스팅, 15년 이상 커피 교육 경력 담당자)</td></tr>
<tr><th scope="row">로스팅·발송</th><td>주문 후 영업일 1~2일 안에 로스팅해 택배</td></tr>
<tr><th scope="row">블렌드</th><td>대표 블렌드 2가지와 수십 가지 맞춤 블렌드</td></tr>
<tr><th scope="row">생두</th><td>직접 수입(케냐, 과테말라, 에티오피아 산지 방문)</td></tr>
</tbody>
</table></div>
<p>업체를 정한 뒤 원두를 실제로 바꿀 때의 걱정(단골 반응, 세팅)은 <a href="/guide/switching-cafe-beans/">카페 원두 바꾸면 손님이 떠날까</a>에 정리했습니다.</p>
"""
    gpath = "/guide/choose-bean-supplier/"
    pages.append(dict(
        path=gpath, crumb="카페 원두 납품 업체 고르는 법",
        title="카페 원두 납품 업체 고를 때 확인할 다섯 가지 | 사용량·잔당 원가·발송 · 커피나라",
        description="카페 원두 납품 업체를 고를 때 확인할 것: 한 달 사용량(1kg ≈ 50~55잔), 1kg 단가를 잔당 원가로 환산한 표, "
                    "매장 장비로 맛보기, 로스팅에서 받기까지의 기간, 블렌드 선택지와 생두 출처.",
        body=guide,
        og_type="article",
        schema=[{"@type": "Article", "@id": S.BASE + gpath + "#article",
                 "headline": "카페 원두 납품 업체 고를 때 확인할 다섯 가지", "inLanguage": "ko",
                 "datePublished": "2026-11-12", "dateModified": X.LASTMOD,
                 "author": {"@id": S.BASE + "/#org"}, "publisher": {"@id": S.BASE + "/#org"},
                 "mainEntityOfPage": S.BASE + gpath, "image": S.BASE + "/assets/img/og-cover.jpg",
                 "about": ["카페 원두 납품", "카페 창업", "원두 단가", "잔당 원가"]}],
    ))

    # ── 가이드: 원두 바꿀 때 ─────────────────────────────
    sdate = "2026-11-12"
    switch = f"""<p class="eyebrow">가이드 · 카페 운영</p>
<h1>카페 원두 바꾸면 손님이 떠날까? 원두 교체 전에 알아 둘 것</h1>
<p class="meta">커피나라 · {sdate}</p>
<p class="lead">지금 쓰는 원두가 마음에 들지 않는데도 쉽게 바꾸지 못하는 이유는 대개 하나입니다. 단골이 맛이 달라졌다며 떠날까 봐서입니다.
커피나라가 매장을 찾아다니며 원두를 바꿔 드린 경험으로 보면, 손님을 떠나게 하는 것은 원두를 바꾸는 일 자체가 아니라 어떤 원두로, 어떻게 바꾸느냐입니다.</p>

<div class="table-wrap"><table>
<caption>원두를 바꾸기 전에 많이 하는 걱정과 커피나라가 현장에서 본 것</caption>
<thead><tr><th scope="col">걱정</th><th scope="col">현장에서 본 것</th><th scope="col">이렇게 하면 됩니다</th></tr></thead>
<tbody>
<tr><th scope="row">단골이 싫어할까</th><td>지금보다 좋은 원두로 바꾼 매장의 손님 반응은 대부분 호의적이었습니다</td><td>맛이 좋아지는 쪽으로 바꿉니다</td></tr>
<tr><th scope="row">원가를 낮추고 싶다</th><td>싼 원두로 바꾼 뒤 손님이 크게 줄어든 매장을 직접 봤습니다</td><td>원두 등급을 낮추지 말고, 단가가 맞는 블렌드를 고릅니다</td></tr>
<tr><th scope="row">샘플은 맛있었는데</th><td>같은 원두도 매장마다 맛이 조금씩 다르게 나옵니다</td><td>내 매장의 머신과 그라인더로 맛봅니다</td></tr>
<tr><th scope="row">세팅을 다시 잡아야 한다</th><td>원두가 바뀌면 분쇄도와 원두 양을 다시 맞춰야 합니다</td><td>한 번에 한 가지씩 조정합니다</td></tr>
<tr><th scope="row">테스트 비용</th><td>무료 테스트라도 선결제 후 환급, 거리 제한 같은 조건이 붙는 곳이 있습니다</td><td>조건을 미리 묻습니다. 커피나라는 100% 무료입니다</td></tr>
</tbody>
</table></div>

<p class="pull">손님이 떠나는 건 원두를 바꿔서가 아니라, 더 나쁜 원두로 바꿔서입니다.</p>

<h2>더 좋은 원두로 바꿨을 때 손님 반응은 대부분 호의적이었습니다</h2>
<p>사장님들이 원두 교체를 앞두고 가장 많이 걱정하는 것이 손님 반응입니다. 커피나라가 지금보다 좋은 원두로 바꿔 드린 매장에서 손님 반응은 거의 대부분 호의적이었습니다.
맛이 달라진 것을 알아채는 손님은 좋아진 맛도 알아봅니다.</p>
<p>커피나라는 원두만 바꿔 드리고 끝내지 않습니다. 20년 이상 로스팅하고 15년 이상 커피 교육을 해 온 담당자가 원두를 쓰는 매장에 추출 교육과 컨설팅을 무료로 해 드려,
바꾼 원두의 맛이 매장에서 꾸준히 나오도록 돕습니다.</p>

<h2>원가 때문에 싼 원두로 바꾼 매장은 손님을 잃었습니다</h2>
<p>커피나라가 예전에 원두를 납품하던 곳 중에 손님이 줄을 서던 카페가 있었습니다. 가게를 넘겨받은 새 사장님이 원가를 낮추려고 저가 원두로 바꿨고,
지금은 문을 닫을 걱정을 할 만큼 손님이 줄었습니다. 이야기로도 들었고, 직접 보기도 했습니다.</p>
<p>원두값을 줄이고 싶다면 원두의 질을 낮추기보다, 단가가 맞는 블렌드를 고르는 쪽이 안전합니다. 커피나라 원두는 {S.PRICE_TEXT}이고,
<a href="/blends/">대표 블렌드</a> 외에도 수십 가지 블렌드가 있어 목표 단가에 맞춰 고를 수 있습니다. 잔당 원두 원가는
<a href="/guide/choose-bean-supplier/">카페 원두 납품 업체 고르는 법</a>의 표로 계산해 볼 수 있습니다.</p>

<h2>같은 원두도 매장마다 맛이 다르게 나옵니다</h2>
<p>로스터리에서 마셨을 때 좋았던 원두가 내 매장에서는 다르게 느껴지는 경우가 있습니다. 같은 원두라도 매장의 물, 머신, 그라인더, 추출 방식에 따라 맛이 조금씩 달라지기 때문입니다.
커피나라가 샘플을 보내지 않고 매장에 직접 찾아가는 이유가 이것입니다. 그 매장에서 낼 수 있는 가장 좋은 맛을 찾아 세팅합니다.</p>
{fig(E, "espresso-extraction.jpg", "방문 테스트 중 매장의 에스프레소 머신에서 두 잔으로 추출되는 에스프레소", "실제 매장 방문 테스트. 그 매장의 머신으로 추출합니다.")}

<h2>원두를 바꾸면 세팅을 다시 잡아야 합니다</h2>
<p>원두마다 밀도와 로스팅 정도가 달라서, 이전 원두에 맞춰 둔 분쇄도 그대로는 추출 속도와 맛이 달라집니다. 원두를 바꾸면 이렇게 다시 맞춥니다.</p>
<ul>
<li>신맛이 강하고 추출이 빨리 끝나면 분쇄도를 더 곱게 합니다.</li>
<li>쓴맛이 강하고 추출이 느리면 분쇄도를 더 굵게 합니다.</li>
<li>분쇄도, 원두 양(도징), 추출량 가운데 한 번에 한 가지만 바꿔 가며 맛을 봅니다.</li>
<li>그라인더 안에 남아 있던 이전 원두가 처음 몇 잔에 섞여 나오므로, 처음 몇 샷으로는 맛을 판단하지 않습니다.</li>
</ul>
<p>커피나라는 방문 테스트 때 이 세팅을 매장에서 직접 잡아 드립니다. 바쁜 시간에도 매장 직원이 쉽고 제대로 같은 맛을 낼 수 있게 만드는 것이 목표입니다.</p>
{fig(E, "store-test-espresso.jpg", "방문 테스트 중 매장 머신의 포터필터에서 샷 잔으로 떨어지는 에스프레소", "다른 매장의 방문 테스트. 매장마다 세팅이 다릅니다.")}

<h2>대용량 주문 전에 매장에서 먼저 맛봅니다</h2>
<p>커핑 노트와 상세페이지만 보고 대용량을 먼저 주문하면, 매장에서 기대한 맛이 나지 않았을 때 되돌리기 어렵습니다. 내 매장 장비로 먼저 맛보고 정하는 것이 순서입니다.</p>
<p>무료 테스트를 내건 곳이라도 조건은 확인하세요. 먼저 비용을 내고 일정량을 주문하면 돌려받는 방식이나, 로스터리에서 몇 km 안의 매장만 방문하는 곳도 있습니다.
커피나라 <a href="/free-test/">방문 샘플 테스트</a>는 100% 무료입니다. 신청비와 보증금이 없고, 환급 조건도 없으며, 제주도와 배로만 갈 수 있는 섬을 뺀 전국에 찾아갑니다.
한 달 원두 사용량이 {S.MIN_KG}kg 이상이면 신청할 수 있고, 테스트 뒤 거래하지 않아도 손해 볼 것이 없습니다.</p>
"""
    spath = "/guide/switching-cafe-beans/"
    pages.append(dict(
        path=spath, crumb="카페 원두 바꿀 때",
        title="카페 원두 바꾸면 손님이 떠날까? 원두 교체 전에 알아 둘 것 · 커피나라",
        description="카페 원두를 바꿀 때의 걱정과 현장 경험: 좋은 원두로 바꾼 매장의 손님 반응은 대부분 호의적, 원가 때문에 싼 원두로 "
                    "바꾼 매장은 손님을 잃음. 매장마다 다른 맛, 분쇄도·도징 다시 잡기, 무료 테스트 조건 확인.",
        body=switch,
        updated=sdate,
        og_type="article",
        image="espresso-extraction.jpg",
        image_alt="방문 테스트 중 매장의 에스프레소 머신에서 두 잔으로 추출되는 에스프레소",
        faq=["switch_reaction", "switch_setting", "store_diff", "free_cost", "education"],
        schema=[{"@type": "Article", "@id": S.BASE + spath + "#article",
                 "headline": "카페 원두 바꾸면 손님이 떠날까? 원두 교체 전에 알아 둘 것", "inLanguage": "ko",
                 "datePublished": sdate, "dateModified": X.LASTMOD,
                 "author": {"@id": S.BASE + "/#org"}, "publisher": {"@id": S.BASE + "/#org"},
                 "mainEntityOfPage": S.BASE + spath, "image": S.BASE + "/assets/img/espresso-extraction.jpg",
                 "about": ["카페 원두 교체", "원두 납품 업체 변경", "에스프레소 세팅", "분쇄도", "카페 운영"]}],
    ))

    # ── 가이드 목록 ──────────────────────────────────────
    guides = [p for p in pages if p["path"].startswith("/guide/")]
    items = "".join(
        f'<li><a href="{g["path"]}"><strong>{E(g["title"].split(" | ")[0].split(" · 커피나라")[0])}</strong></a>'
        f'<span>{E(g["description"])}</span></li>' for g in reversed(guides))
    pages.append(dict(
        path="/guide/", crumb="가이드",
        title="카페 운영 가이드 | 원두 납품 업체 고르기 · 원두 바꿀 때 · 커피나라",
        description="카페 사장님과 창업 준비자를 위한 커피나라 가이드. 원두 납품 업체 고르는 법, 잔당 원가 계산, 원두를 바꿀 때 "
                    "손님 반응과 세팅.",
        body=f"""<p class="eyebrow">가이드</p>
<h1>카페 운영 가이드</h1>
<p class="lead">카페를 열거나 원두를 바꾸려는 분들이 자주 묻는 것을, 커피나라가 매장을 찾아다니며 본 것과 함께 정리합니다.</p>
<ul class="guide-list">{items}</ul>""",
        schema=[{"@type": "CollectionPage", "@id": S.BASE + "/guide/#webpage", "url": S.BASE + "/guide/",
                 "name": "커피나라 카페 운영 가이드", "inLanguage": "ko", "isPartOf": {"@id": S.BASE + "/#website"},
                 "mainEntity": {"@type": "ItemList", "itemListElement": [
                     {"@type": "ListItem", "position": i + 1, "url": S.BASE + g["path"]}
                     for i, g in enumerate(reversed(guides))]}}],
    ))

    return pages
