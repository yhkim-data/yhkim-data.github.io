# DI Lab 홈페이지 프로젝트

## 개요
- DI Lab = Data Insight Laboratory (Intelligence 아님!)
- GitHub Pages 배포: yhkim-data.github.io
- 커스텀 도메인: di-lab.io
- 대표: YH.Kim
- 이메일: yhkim@di-lab.io

## 기술 스택
- Hugo Extended (v0.160.1) + GitHub Pages
- 커스텀 도메인: di-lab.io
- 테마 없이 커스텀 레이아웃 (layouts/)
- CSS: assets/css/main.css
- 정적 파일: static/images/
- 한글 폰트: Noto Sans KR (Google Fonts CDN)
- 아이콘: Font Awesome CDN 또는 shields.io

## 파일 구조
yhkim-data.github.io/
├── .github/workflows/ ← GitHub Actions (Hugo 빌드·배포)
├── .gitignore
├── CLAUDE.md
├── CNAME              ← 절대 수정/삭제 금지!
├── hugo.toml          ← Hugo 설정
├── layouts/           ← 커스텀 레이아웃
├── assets/css/        ← CSS
├── content/           ← 콘텐츠 (Markdown)
├── static/images/     ← 정적 파일 (로고 등)
└── archetypes/        ← Hugo 아키타입

## 빌드/배포
- 빌드: hugo --gc --minify
- 로컬 프리뷰: hugo server
- 배포: GitHub Pages (main 브랜치, GitHub Actions)
- CNAME 파일 절대 수정/삭제 금지

## 디자인 규칙
- 메인 컬러: #1E60C9 (파랑), 다크: #174EA3, 라이트: #EBF1FB
- 포인트 컬러: #10B981 (초록), 다크: #0D9668
- 배경: 흰색(#fff) / 연회색(#f7fafc) 번갈아
- 폰트: Noto Sans KR
- 본문: 16px, 제목: 32px, 소제목: 24px
- 섹션 간 여백: 80px

## DI Lab 정보 (홈페이지 내용용)
- 서비스: 데이터 분석, AI/ML 모델링, 통계 조사분석, 데이터 기반 컨설팅
- 기술스택: R, Python, SAS, SQL, scikit-learn, TensorFlow
- 인증(증명서 보유): 여성기업, 중소기업, SW사업자, 창업기업 확인서
- 청년창업기업: 해당되나 증명서 없음
- 나라장터: 등록 (인증 아님)
- 차별점: 석사급 분석 전문성, 원스톱 서비스, 공공조달 인증 완비

## Git 규칙
- CNAME 파일 절대 삭제 금지
- push 전 반드시 로컬 확인
- 커밋 메시지 한국어

## 과거 실수 기록
- (작업하면서 추가)
