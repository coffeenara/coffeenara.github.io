"""정적 사이트 생성기. 실행: python _src/build.py  (표준 라이브러리만 사용)

_src/ 아래 파일만 고치고 이 스크립트를 돌리면 루트의 HTML, sitemap.xml, robots.txt, llms.txt가 다시 만들어집니다.
"""
import datetime
import hashlib
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import facts as S  # noqa: E402
import pages  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape

ORG_ID = S.BASE + "/#org"
SITE_ID = S.BASE + "/#website"

NAV = [
    ("/", "홈"),
    ("/blends/", "원두 블렌드"),
    ("/free-test/", "무료 방문 테스트"),
    ("/origin/", "생두 직접 수입"),
    ("/faq/", "자주 묻는 질문"),
    ("/guide/", "가이드"),
]


def area(name):
    return {"@type": "AdministrativeArea", "name": name,
            "containedInPlace": {"@type": "Country", "name": "대한민국"}}


def org_schema():
    return {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": S.NAME,
        "alternateName": [S.NAME_EN, "coffeenara", "커피나라 로스터리"],
        "url": S.BASE + "/",
        "logo": S.BASE + "/assets/img/og-cover.jpg",
        "email": S.EMAIL,
        "description": "생두를 직접 수입하는 회사이자, 그 생두를 로스팅해 카페와 매장에 원두를 납품하는 로스터리. "
                       "제주도와 배로만 갈 수 있는 섬을 뺀 전국 매장에 찾아가 100% 무료로 샘플 테스트와 세팅을 하고, "
                       "원두를 납품하는 매장에 무료 커피 교육과 컨설팅을 한다. 방문 테스트와 교육은 20년 이상 로스팅, "
                       "15년 이상 커피 교육 경력의 담당자가 직접 맡는다.",
        "areaServed": [area(a) for a in S.AREAS],
        "knowsAbout": ["생두 수입", "커피 생두", "커피 원두", "블렌드 원두", "카페 원두 납품", "커피 로스팅",
                       "에스프레소 블렌드", "에스프레소 추출 세팅", "커피 교육", "카페 컨설팅"],
        "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "url": S.CONTACT_URL,
                         "email": S.EMAIL, "availableLanguage": "ko", "areaServed": "KR"},
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "커피나라 카페 납품용 블렌드 원두",
            "itemListElement": [{
                "@type": "Offer",
                "itemOffered": {"@id": f"{S.BASE}/blends/#{b['id']}"},
            } for b in S.BLENDS] + [{
                "@type": "Offer",
                "name": "카페 납품용 원두 1kg 단가",
                "priceSpecification": {
                    "@type": "UnitPriceSpecification", "priceCurrency": "KRW",
                    "minPrice": S.PRICE_MIN, "maxPrice": S.PRICE_MAX,
                    "referenceQuantity": {"@type": "QuantitativeValue", "value": 1, "unitCode": "KGM"},
                },
            }],
        },
    }


def website_schema():
    return {"@type": "WebSite", "@id": SITE_ID, "url": S.BASE + "/", "name": f"{S.NAME} {S.NAME_EN}",
            "inLanguage": "ko", "publisher": {"@id": ORG_ID}}


def service_schema():
    return {
        "@type": "Service",
        "@id": S.BASE + "/free-test/#service",
        "name": "무료 방문 커피 샘플 테스트",
        "serviceType": "카페 원두 납품 상담 및 매장 방문 시음",
        "provider": {"@id": ORG_ID},
        "areaServed": [area(a) for a in S.AREAS],
        "audience": {"@type": "BusinessAudience", "audienceType": "카페·커피 매장 운영자와 창업 준비자"},
        "description": "20년 이상 로스팅, 15년 이상 커피 교육 경력의 커피나라 담당자가 매장에 직접 찾아가 그 매장의 머신과 그라인더로 여러 원두를 "
                       "추출해 함께 맛보고, 가장 좋은 맛이 나도록 세팅한 뒤 매장에 맞는 블렌드를 제안하는 서비스. 100% 무료로, "
                       "신청비·보증금·환급 조건과 거리 제한이 없다. 한 달 원두 사용량 10kg 이상 매장 대상, 제주도와 배로만 갈 수 "
                       "있는 섬 제외.",
        "offers": {
            "@type": "Offer", "price": 0, "priceCurrency": "KRW",
            "eligibleQuantity": {"@type": "QuantitativeValue", "minValue": S.MIN_KG, "unitCode": "KGM",
                                 "unitText": "한 달 원두 사용량"},
            "url": S.CONTACT_URL,
        },
    }


def education_schema():
    return {
        "@type": "Service",
        "@id": S.BASE + "/free-test/#education",
        "name": "원두 납품 매장 무료 커피 교육·컨설팅",
        "serviceType": "에스프레소 추출 교육, 매장 세팅, 카페 운영 컨설팅",
        "provider": {"@id": ORG_ID},
        "areaServed": [area(a) for a in S.AREAS],
        "audience": {"@type": "BusinessAudience", "audienceType": "커피나라 원두를 쓰는 카페·커피 매장"},
        "description": "20년 이상 로스팅, 15년 이상 커피 교육 경력의 커피나라 담당자가 원두를 납품하는 매장에 추출 교육과 컨설팅을 무료로 진행한다.",
        "offers": {"@type": "Offer", "price": 0, "priceCurrency": "KRW"},
    }


def product_schema(b):
    return {
        "@type": "Product",
        "@id": f"{S.BASE}/blends/#{b['id']}",
        "name": f"커피나라 {b['name']}",
        "alternateName": b["short"],
        "brand": {"@type": "Brand", "name": S.NAME},
        "manufacturer": {"@id": ORG_ID},
        "category": "블렌드 원두",
        "description": b["desc"],
        "image": f"{S.BASE}/assets/img/{b['img']}",
        "additionalProperty": [{"@type": "PropertyValue", "name": "커핑 노트", "value": ", ".join(b["notes"])}],
    }


def faq_schema(keys):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": S.FAQ[k][0],
         "acceptedAnswer": {"@type": "Answer", "text": S.FAQ[k][1]}} for k in keys]}


def breadcrumb(path, title):
    if path == "/":
        return None
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "홈", "item": S.BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": title, "item": S.BASE + path}]}


def faq_html(keys, heading="자주 묻는 질문"):
    items = "".join(
        f'<details class="faq-item"><summary><h3>{E(S.FAQ[k][0])}</h3></summary><p>{E(S.FAQ[k][1])}</p></details>'
        for k in keys)
    return f'<section class="faq" aria-labelledby="faq-h"><h2 id="faq-h">{E(heading)}</h2>{items}</section>'


def cta_html(text="지금 신청하시고 맛의 변화를 느껴 보세요"):
    return (f'<section class="cta"><p class="cta-lead">{E(text)}</p>'
            f'<a class="btn" href="{E(S.CONTACT_URL)}" target="_blank" rel="noopener">{E(S.CONTACT_LABEL)}</a>'
            f'<p class="cta-sub">월 {S.MIN_KG}kg 이상 사용 매장 · 제주도와 배로만 갈 수 있는 섬을 뺀 전국 방문</p></section>')


def page(p):
    path, title, desc = p["path"], p["title"], p["description"]
    url = S.BASE + path
    graph = [org_schema(), website_schema()] + p.get("schema", [])
    if p.get("faq"):
        graph.append(faq_schema(p["faq"]))
    bc = breadcrumb(path, p.get("crumb", title))
    if bc:
        graph.append(bc)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    og_img = S.BASE + "/assets/img/" + p.get("image", "og-cover.jpg")
    cur = ' aria-current="page"'
    nav = "".join(
        f'<a href="{h}"{cur if h == path else ""}>{E(t)}</a>' for h, t in NAV)
    body = p["body"]
    if p.get("faq"):
        body += faq_html(p["faq"])
    if p.get("cta", True):
        body += cta_html()
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#2a211c">
<meta property="og:type" content="{p.get('og_type', 'website')}">
<meta property="og:site_name" content="{S.NAME} {S.NAME_EN}">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:alt" content="{E(p.get('image_alt', '커피 생두 마대 위에 커피나라, 카페 원두 납품, 무료 방문 샘플 테스트 문구'))}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="text/plain" href="/llms.txt" title="llms.txt">
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<header class="site-header">
<div class="wrap header-in">
<a class="brand" href="/">{S.NAME_EN}<span>{S.NAME}</span></a>
<a class="btn btn-sm" href="{E(S.CONTACT_URL)}" target="_blank" rel="noopener">{E(S.CONTACT_LABEL)}</a>
</div>
<nav class="wrap nav" aria-label="사이트 메뉴">{nav}</nav>
</header>
<main class="wrap">
{body}
</main>
<footer class="site-footer">
<div class="wrap">
<p><strong>{S.NAME} {S.NAME_EN}</strong> · 생두 수입 · 로스팅 · 카페 원두 납품</p>
<p>원두 1kg {S.won(S.PRICE_MIN)}~{S.won(S.PRICE_MAX)} · 주문 후 영업일 1~2일 안에 로스팅해 택배 발송 · 무료 방문 테스트는 제주도와 배로만 갈 수 있는 섬을 뺀 전국</p>
<p>문의 <a href="mailto:{S.EMAIL}">{S.EMAIL}</a> · <a href="{E(S.CONTACT_URL)}" target="_blank" rel="noopener">{E(S.CONTACT_LABEL)}</a></p>
</div>
</footer>
</body>
</html>
"""


def write(rel, text):
    full = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


LASTMOD = "__LASTMOD__"  # 페이지 안의 dateModified 자리. 빌드 때 실제 수정일로 바뀝니다.
MANIFEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lastmod.json")


def main():
    """페이지 내용이 실제로 바뀐 경우에만 그 페이지의 수정일(sitemap lastmod, dateModified)을 오늘로 바꿉니다."""
    today = os.environ.get("BUILD_DATE") or datetime.date.today().isoformat()
    try:
        with open(MANIFEST, encoding="utf-8") as f:
            manifest = json.load(f)
    except FileNotFoundError:
        manifest = {}

    all_pages = pages.build(S, E, sys.modules[__name__])
    for p in all_pages:
        rel = p["path"].strip("/")
        text = page(p)
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        prev = manifest.get(p["path"])
        if not prev or prev["hash"] != digest:
            prev = {"hash": digest, "date": today}
            manifest[p["path"]] = prev
        p["lastmod"] = prev["date"]
        write(os.path.join(rel, "index.html") if rel else "index.html", text.replace(LASTMOD, prev["date"]))

    with open(MANIFEST, "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1, sort_keys=True)

    urls = "".join(
        f"<url><loc>{S.BASE}{p['path']}</loc><lastmod>{p['lastmod']}</lastmod></url>\n"
        for p in all_pages)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {S.BASE}/sitemap.xml\n")

    faq_md = "\n".join(f"- **{q}** {a}" for q, a in S.FAQ.values())
    links = "\n".join(f"- [{p['title']}]({S.BASE}{p['path']}): {p['description']}" for p in all_pages)
    write("llms.txt", f"""# {S.NAME} ({S.NAME_EN})

> 생두를 직접 수입하는 회사이자, 그 생두를 로스팅해 카페와 매장에 원두를 납품하는 로스터리입니다. 제주도와 배로만 갈 수 있는 섬을 뺀 전국 매장에 찾아가 무료 샘플 테스트를 합니다.

- 무료 방문 샘플 테스트: 100% 무료(신청비·보증금·환급 조건 없음, 거리 제한 없음), 한 달 원두 사용량 {S.MIN_KG}kg 이상 매장, 제주도와 배로만 갈 수 있는 섬을 뺀 전국. 매장의 머신과 그라인더로 테스트하고 세팅
- 교육·컨설팅: 20년 이상 로스팅하고 15년 이상 커피 교육을 해 온 담당자가 원두 납품 매장에 무료로 진행
- 원두 가격: {S.PRICE_TEXT}
- 발송: 주문 후 영업일 1~2일 안에 로스팅해 택배 발송
- 대표 블렌드: Premium Blend({", ".join(S.PREMIUM["notes"])}), Special Blend({", ".join(S.SPECIAL["notes"])}), 그 밖에 수십 가지 블렌드
- 생두: 직접 수입(케냐, 과테말라, 에티오피아 산지 방문). 블렌드별 배합과 원산지 구성은 비공개
- 상담: {S.CONTACT_URL} · {S.EMAIL}

## 페이지

{links}

## 자주 묻는 질문

{faq_md}
""")
    print(f"built {len(all_pages)} pages")


if __name__ == "__main__":
    main()
