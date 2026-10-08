# NOTES — di-lab.io 고도화 (feat/enrich-2026-10, 2026-10-08)

목표: 글자 위주로 휑한 인상을 장식이 아니라 증거(결과물·숫자·답변)로 채운다. 7월 에디토리얼 톤 유지.

## 변경 요약

| 위치 | 변경 |
|---|---|
| 홈 | hero 아래 신뢰 스트립(번호 없음) → Why 01 → Process 02 → Services 03 → **Deliverables 04** → Selected Work 05(번호만 변경) → **FAQ 06** → closing CTA |
| 홈 스트립 | `50+ 분석 프로젝트 수행 / 3일 이내 영업일 기준 회신 / 4종 공공조달 인증 보유 / R · Python · SAS`. 값은 `hugo.toml` `[params.stats]`·`[params.trust]` 에서 렌더. 모바일 2×2, 데스크톱 1행 |
| 홈 Deliverables | 샘플 3장(01 데이터 분석·02 AI/ML·05 통계 조사) + "서비스별 산출물 보기". services front matter `sample.featured` 로 선택 |
| services | 각 서비스 아코디언에 `샘플` 필드로 해당 그림 1장. 그림 클릭 시 원본 SVG(새 창) |
| 샘플 그림 | `static/images/samples/sample-01~06.svg`, 합성 데이터(고정 표·seed 42), 960×640, 장당 80KB 미만. 생성 스크립트 `tools/samples/make_samples.py`(재실행 시 바이트 동일) |
| FAQ | `data/faq.yaml` 8문항. 홈은 앞 4문항+전체 보기, contact 는 전체 + FAQPage JSON-LD(사이트에서 한 곳만) |
| projects | 수행 사례 8건을 2열 카드 그리드(`.work-grid/.work-card`), 비링크라 hover 없음. 홈 Selected Work 는 변경 없음 |
| CSS | `main.css` 끝에 추가만. `:root` 변경 0, 기존 규칙 수정 0 |
| repo | `.gitignore` 에 `FAQ_REVIEW.md`, `refs/`, `tools/samples/.cache/`, `__pycache__/` 추가 |

## 설계 결정
- 스트립은 밝은 배경. hero 가 94vh 라 다크 연장 시 첫 화면이 전부 어두워지고 헤더 다크 전환 대상 추가도 필요해짐.
- 샘플 그림 텍스트는 글리프 외곽선(path)으로 내장. `<img>` SVG 는 웹폰트를 못 쓰므로. Pretendard 가변 서브셋을 굵기별 정적 TTF 로 병합해 사용(캐시는 커밋 안 함).
- 그림당 액센트는 1개 요소만. 나머지는 ink·muted·dark-muted·dark-sub 명도 차.
- FAQ 는 `.svc-row` 를 공유하지 않고 같은 문법의 `.faq-row` 를 추가. 공유하면 기존 규칙 수정이 됨.
- 샘플 캡션의 "샘플 · 합성 데이터" 는 템플릿 상수(그림 내부에도 고정 표기).

## 검증
- `hugo --gc --minify` 에러·경고 0. 페이즈별 커밋 각각 단독 빌드도 경고 0.
- Playwright 1440·380: 홈 섹션 순서·번호, 스트립 값, 샘플 img 의 width·height·alt·lazy·로드, 캡션 고정표기, 가로 넘침 0, FAQ summary Enter/Space 토글과 포커스 표시 통과.
- CLS: 새 섹션 기여 0. 모바일 홈 0.013 은 hero 텍스트 폰트 교체에서 발생하는 기존 현상.
- 대비: 의미 텍스트는 muted(배경 대비 7.0:1) 이상. faint(4.47:1)는 aria-hidden 번호에만.
- 식별정보·내부경로·금지어 대조(diff·커밋 메시지·추적 파일·빌드 결과물): 이번 브랜치 신규 노출 0. 내부 링크 깨짐 0.
- 시각 비평 10건 중 7건 반영, diff 리뷰 5건 중 4건 반영(샘플 색 지적은 두 색 모두 :root 토큰이라 미반영).
- 전송량(1440, 풀 스크롤 후, 비압축 응답 본문 합): 홈 +226KB(목표 +400KB 이내), services +72KB, contact +12KB, projects +5KB.

## 남은 결정 사항
1. 로컬 `FAQ_REVIEW.md` — 수정 횟수·결제·NDA·세금계산서·데이터 파기·비용·방문·저작권 정책 확정 후 FAQ 추가 여부.
2. "공공조달 인증 4종" — about 인증 목록은 3종+나라장터 등록. 창업기업 확인서를 about 에 올릴지, 라벨을 "인증·등록 4종" 으로 바꿀지.
3. 공개 프로젝트 "호흡기 질환 발생 요인 분석" stack 의 공공 데이터 출처 약칭 — 기존 문구(이번 변경 아님). 일반화할지.
4. 홈 Why 03 "50건 이상의 분석" 과 스트립 "50+" 가 한 화면 안에 중복 — Why 03 소제목을 방법론 중심으로 바꿀지(카피 범위 밖이라 보류).
5. 홈 Selected Work 의 비링크 `div.work-row` hover — projects 는 카드로 해소, 홈은 범위 밖이라 유지.
6. FAQ 답변 속 기간·회신·인증 수는 문장이라 params 와 자동 연동되지 않음(yaml 상단 주석으로 연동 지점 명시).

## 2차 — 홈 상단부 밀도 보강

| 위치 | 변경 |
|---|---|
| 인증 표기 | 홈 Why 02 와 about 인증 목록에 "창업기업 확인" 추가. about 은 인증 4종 + 나라장터 등록 5행. Why 02 의 인증 수는 `params.trust.certs_count` 로 렌더 |
| Process 02 | 각 단계 오른쪽에 "받는 것" 열(데스크톱 3열, 모바일 적층). 하단에 전체 기간 안내 — services `duration` 문자열에서 최소·최대 주를 계산(현재 2~10주) |
| Services 03 | services front matter `summary` 신설. 홈 카드에 한 줄 설명 + 표준 기간, services 아코디언 제목 아래 한 줄(펼치면 숨김) |
| Deliverables 04 | 큰 1장(좌, `sample.lead` = 통계 조사 분석) + 작은 2장(우, 세로 적층), 13:5 비율. 모바일은 큰 자리 샘플이 먼저 |
| Why 03 | 제목을 "검증된 방법론으로, 엄밀하게 분석합니다" 로 교체(건수는 스트립·about 에서 노출) |
| Selected Work 05 | 비링크 `div.work-row` hover 제거. 링크 행 hover 와 하단선은 유지 |
| services | 템플릿이 읽지 않던 `subheading` 삭제 |
| 앵커 | `/services/#service-0N` 으로 들어오면 해당 아코디언을 펼치고 고정 헤더 높이만큼 여백(`scroll-margin-top`). 1차 이전부터 접힌 채 헤더에 가려지던 문제 |

### 검증
- `hugo --gc --minify` 에러·경고 0. 2차 페이즈 커밋 각각 단독 빌드 경고 0.
- Playwright 1440·380: 기존 기능 검사 전부 통과, 홈 카드 앵커 6개 일치, 앵커 진입 시 아코디언 펼침·헤더 아래 위치 확인. Deliverables 좌우 하단 차 3px, Services 기간 줄·아코디언 기호 정렬 확인.
- hero 영상: 일반 설정에서 재생 확인. reduced-motion 에서는 기존 CSS 가 영상 요소를 숨겨 poster 도 보이지 않고 단색 네이비로 표시됨(기존 동작, 이번 범위 밖).
- 시각 비평 7건 중 6건 반영(받는 것 라벨 반복은 모바일 맥락 유지를 위해 유지). diff 리뷰 5건 중 4건 반영.
- 노출 대조(diff·커밋 메시지·추적 파일·빌드): 2차 신규 0건, 금지어 0, 내부 링크·앵커 깨짐 0.
- 홈 전송량 1차 대비 +5.6KB.

### 남은 결정 사항(2차)
1. reduced-motion 사용자에게 hero poster 를 보여줄지(현재 단색). hero 는 이번 범위 밖.
2. Process 하단의 "소프트웨어 개발은 규모에 따라 별도 협의" 는 고정 문구 — 서비스 구성 변경 시 함께 수정.
3. services front matter 의 `heading`·`cta` 도 템플릿이 읽지 않는 필드 — 삭제 여부.

---

# (이전) NOTES — di-lab.io 콘텐츠 현행화 (content/2026-10)

## 변경 요약

| 페이지 | 위치 | 전 | 후 |
|---|---|---|---|
| 전체 | `hugo.toml` | (없음) | `[params.stats] projects_count = 50` 신설. 실적 숫자 단일 소스 |
| 홈 | Why 01 제목 | 수집부터 보고서까지, 한 팀이 끝냅니다 | 수집부터 보고서까지, 담당자가 바뀌지 않습니다 |
| 홈 | Why 03 제목 | 구 실적 숫자 하드코딩 | `{{ .Site.Params.stats.projects_count }}`건 이상의 분석 |
| 홈 | Selected Work | 공개 프로젝트 featured 3건 | 수행 사례 2건(`div.work-row`, 링크 없음) + 공개 프로젝트 1건(기존 `a.work-row` 그대로), 번호 01·02·03 연속 |
| about | 대표 소개 text | 구 실적 숫자 하드코딩 | front matter `{count}` 자리표시 → 템플릿 `replace` 로 파라미터 렌더 |
| about | 통계 블록 | `track.count` 하드코딩 + "+" | `track.count` 삭제, 템플릿이 `projects_count` 직접 렌더 ("50+") |
| services | 04 소프트웨어 개발 진행 방식 | 파이프라인·대시보드 설계(Python·R, Shiny·Streamlit) … 분석팀이 직접 개발 | 파이프라인·대시보드(Shiny·Streamlit)·웹 애플리케이션(FastAPI·Next.js)·업무 자동화 스크립트(Python) 설계 … 분석을 맡은 담당자가 직접 개발 |
| services | front matter `subheading` | 구 실적 숫자 하드코딩 | "{count}건 이상의 …" (※ 템플릿에서 미렌더되는 죽은 필드, 아래 결정 사항) |
| projects | 리드 | 공공·보건·산업 영역에서 수행한 프로젝트 중 일부입니다. 전체 코드는 GitHub에서… | 의뢰받아 수행한 프로젝트는 익명 처리한 사례로, 직접 개발한 분석 코드는 공개 프로젝트로 정리했습니다. 공개 프로젝트의 전체 코드는 GitHub에서… |
| projects | 본문 | 공개 프로젝트 5건 단일 목록 | 01 수행 사례 8건(익명, 연도 표기, 링크 없음) → 02 공개 프로젝트 5건(연도 없음). 섹션 헤더는 about 페이지 패턴 재사용 |
| contact | 리드 | 과제 개요와 데이터 상황을 이메일로 보내주세요. | 과제 개요와 데이터 상황을 아래 폼으로 보내주세요. (이메일 직접 발송 안내 `mail-direct` 유지) |
| repo | `.gitignore` | — | `PUBLISH_REVIEW.md`, `.serena/` 추가 |

## 실적 집계 근거 (R1)
내부 완료 기록 합계 52건 → 10단위 내림 → `projects_count = 50`. 세부 집계와 소스는 로컬 PUBLISH_REVIEW.md 에만 기록.

## "팀" 표현 점검 (R3)

| 위치 | 문구 | 처리 |
|---|---|---|
| 홈 Why 01 | 한 팀이 끝냅니다 | **수정** → 담당자가 바뀌지 않습니다 |
| services 04 how | 분석팀이 직접 개발하므로 | **수정** → 분석을 맡은 담당자가 직접 개발하므로 |
| services 01·02·04·06 "이런 분께" | …필요한 팀 / …자동화하려는 팀 / …자동화해야 하는 팀 / …통합해야 하는 팀 | 유지 (클라이언트 측 팀 지칭) |
| 전체 | 저희·우리·직원·인력 | 해당 없음 (grep 0) |

## 검증 (R4)
- `hugo --gc --minify` 에러·경고 0, 10 pages.
- 빌드 결과물·diff·추적 파일·커밋 메시지에 대해 식별 토큰(클라이언트명·개인명·지역명·주제어·구 실적 숫자) 대조 → 0건. 서브에이전트 1회 + 메인 재검사 1회.
- 내부 링크 전부 public/ 내 실제 파일로 해석됨, 깨짐 0. 홈·about·services·projects·contact·privacy·404 렌더 확인.
- 모바일 380px: 새 사례 행은 기존 `.work-row`(flex-wrap, body `min-width:250px`) 그대로라 기존 행과 동일하게 줄바꿈. CSS 변경 없음.
- diff 리뷰 1회: 디자인 변경 유입 없음(CSS diff 0, 인라인 스타일은 about 패턴 복제만), 하드코딩 없음, 템플릿 스코프 유효, 시크릿·CNAME·사업자 정보 무변경. FAIL 1건(홈 하단선 누락) → 수정 후 재빌드 확인.

## 실패·접근 변경
- 홈 Selected Work 하단선: 1차로 프로젝트 행을 `div`+내부 `a.go` 로 바꿨으나 리뷰에서 "뒤따르는 `div.reveal`(전체 보기 링크) 때문에 어떤 행도 `last-of-type` 하단선을 받지 못함" 지적 → 프로젝트 행을 원래 `a.work-row` 로 되돌림. 사례 `div` 2개는 뒤의 wrapper div 때문에 하단선 없음, `a` 1개가 `a:last-of-type` 로 하단선 → 선 1겹, CSS 무수정. 템플릿 주석으로 의존 관계 명시.
- `subheading` 은 services 템플릿이 읽지 않는 죽은 front matter. 숫자만 자리표시로 바꾸고 삭제는 하지 않음(요청 범위 밖).
- 후속 점검: 1차 NOTES.md 에 내부 경로·원본 건명이 포함되어 해당 커밋을 soft reset 후 재작성. 공개 프로젝트 연도 표기 제거.

## 남은 결정 사항
1. 로컬 PUBLISH_REVIEW.md 승인 — 사례 8건 중 1건은 폴더 위치로만 완료 판단.
2. 실적 숫자 — 내부 완료 기록을 현행화하면 더 큰 10단위로 올릴 여지 있음. 현재는 보수적 50.
3. 사례 카드의 의뢰인 유형 "학술 연구" 표기 — 신분 미확인. 대안 "연구 의뢰".
4. services `subheading` 죽은 필드 — 삭제 또는 템플릿 렌더 결정.
5. `.work-row` 는 비링크 `div` 에도 hover 효과가 적용됨 — 클릭 가능처럼 보일 수 있음. CSS 변경 금지라 그대로 둠.
