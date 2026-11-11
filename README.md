# coffeenara.github.io

커피나라(Coffee Nara) 카페 원두 납품 사이트. GitHub Pages로 배포합니다.

- 문구와 사실: `_src/facts.py` (가격, 지역, 블렌드, FAQ, 카카오 오픈채팅 주소 `KAKAO_URL`)
- 페이지 본문: `_src/pages.py`
- 빌드: `python _src/build.py` → 루트의 HTML, `sitemap.xml`, `robots.txt`, `llms.txt`를 다시 만듭니다.
- 디자인: `assets/style.css`
