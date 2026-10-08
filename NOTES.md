# NOTES — di-lab.io 콘텐츠 현행화 (content/2026-10, 2026-10-08)

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
