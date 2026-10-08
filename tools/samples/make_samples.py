# 서비스별 산출물 샘플 그림 6종(합성 데이터)을 SVG로 생성하는 스크립트 — static/images/samples/
"""
실행:  python tools/samples/make_samples.py
- 모든 수치는 합성값이다(고정 표 또는 seed 42 난수). 실제 프로젝트 데이터와 무관하다.
- 캔버스 960×640 px. 모든 좌표는 캔버스 px(좌상단 원점)이며 글자 크기 px → pt 는 ×0.72.
- 색은 사이트 :root 토큰만 사용한다.
"""
import re
from math import erf, sqrt
from pathlib import Path
from statistics import NormalDist

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.font_manager import FontProperties  # noqa: E402
from matplotlib.patches import Polygon, Rectangle  # noqa: E402
from matplotlib.textpath import TextPath  # noqa: E402

import _font  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "static" / "images" / "samples"
FAM = _font.register()
SEED = 42

INK, MUTED, DMUTED, DSUB = "#0B0F1A", "#475569", "#8A94A6", "#C7D0DE"
LINE, BG, BODY, FAINT = "#D3D7DE", "#F5F6F8", "#1F2937", "#6B7280"
ACCENT, ACCENT_T, WHITE = "#DB3B17", "#C13210", "#FFFFFF"
PX = 0.72  # px → pt

plt.rcParams.update({"svg.fonttype": "path", "svg.hashsalt": "dilab", "font.family": FAM})


class Canvas:
    """960×640 px 캔버스 위에 px 좌표로 그리는 얇은 래퍼."""

    def __init__(self):
        self.fig = plt.figure(figsize=(9.6, 6.4), dpi=100)
        self.fig.patch.set_facecolor(WHITE)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, 960)
        self.ax.set_ylim(640, 0)
        self.ax.axis("off")

    def text(self, x, y, s, size=15, w=400, c=MUTED, ha="left", va="baseline", **kw):
        return self.ax.text(x, y, s, fontsize=size * PX, fontweight=w, color=c, ha=ha, va=va, **kw)

    def width(self, t):
        """텍스트 폭(px). 글리프 외곽선으로 직접 계산해 백엔드 dpi 와 무관하다."""
        prop = FontProperties(family=FAM, weight=t.get_fontweight())
        return TextPath((0, 0), t.get_text(), size=t.get_fontsize() / PX, prop=prop).get_extents().width

    def line(self, x1, y1, x2, y2, c=LINE, lw=1, cap="butt"):
        self.ax.plot([x1, x2], [y1, y2], color=c, lw=lw * PX, solid_capstyle=cap)

    def path(self, xs, ys, c=INK, lw=2):
        self.ax.plot(xs, ys, color=c, lw=lw * PX, solid_capstyle="round", solid_joinstyle="round")

    def rect(self, x, y, w, h, fc=WHITE, ec="none", lw=1):
        self.ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, lw=lw * PX))

    def dot(self, x, y, d=12, c=INK, marker="o"):
        self.ax.plot([x], [y], marker=marker, ms=d * PX, mfc=c, mec=WHITE, mew=2 * PX, ls="none")

    def frame(self, no, title, notes):
        """공통 문서 헤더·샘플 태그·푸터."""
        self.line(48, 40, 912, 40, INK, 2)
        self.text(48, 76, no, 15, 600, FAINT)
        self.text(140, 76, title, 22, 700, INK)
        tag = self.text(902, 74, "샘플 · 합성 데이터", 15, 600, MUTED, ha="right")
        tw = self.width(tag)
        self.rect(902 - tw - 10, 56, tw + 20, 26, BG, LINE, 1)
        tag.set_zorder(5)
        self.line(48, 92, 912, 92)
        self.line(48, 568, 912, 568)
        for i, s in enumerate(notes):
            self.text(48, 592 + 20 * i, s, 15, 400, MUTED)
        self.text(912, 592, f"자료: 합성 데이터(seed {SEED})", 15, 400, FAINT, ha="right")

    def save(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        self.fig.savefig(OUT / name, metadata={"Date": None}, facecolor=WHITE)
        plt.close(self.fig)
        minify(OUT / name)


_NUM = re.compile(r"-?\d+(?:\.\d+)?(?:e-?\d+)?")
GLYPH_K = 16  # 글리프 좌표를 1/16 로 줄이고 텍스트 그룹 scale 을 16배로 보정(오차 < 0.06px)


def _num(v: float) -> str:
    v = round(v, 2)
    if v == int(v):
        return str(int(v))
    t = f"{abs(v):.2f}".rstrip("0").lstrip("0")
    return ("-" if v < 0 else "") + t


def _compact_d(d: str, k: float = 1.0) -> str:
    """경로 d 를 상대 좌표·최소 공백으로 다시 쓴다. k 로 나눈 뒤 절대좌표 기준으로 반올림."""
    nd = 0 if k > 1 else 2
    out, cx, cy, sx, sy = [], 0.0, 0.0, 0.0, 0.0
    for cmd, args in re.findall(r"([MLQCZz])([^MLQCZz]*)", d):
        if cmd in "Zz":
            out.append("z")
            cx, cy = sx, sy
            continue
        nums = [round(float(n) / k, nd) for n in _NUM.findall(args)]
        txt = ""
        for i, v in enumerate(nums):
            sv = _num(v - (cx if i % 2 == 0 else cy))
            txt += sv if (sv.startswith("-") or not txt) else " " + sv
        cx, cy = nums[-2], nums[-1]
        if cmd == "M":
            sx, sy = cx, cy
        out.append(cmd.lower() + txt)
    return "".join(out)


def minify(path: Path):
    """SVG 용량 절감: 주석·공백 제거, 경로 상대좌표화, 글리프 좌표 축소. 렌더 결과는 동일."""
    s = path.read_text(encoding="utf-8")
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r'(<path id="PretendardDIL[^"]*" d=")([^"]*)"',
               lambda m: m.group(1) + _compact_d(m.group(2), GLYPH_K) + '"', s)
    s = re.sub(r'( d=")([^"]*)"',
               lambda m: m.group(1) + (_compact_d(m.group(2)) if m.group(2)[:1] == "M" else m.group(2)) + '"', s)
    s = re.sub(r"scale\(([\d.]+) -\1\)", lambda m: "scale({0:.6g} -{0:.6g})".format(float(m.group(1)) * GLYPH_K), s)
    s = re.sub(r'(<use xlink:href="#PretendardDIL[^"]*" transform="translate\()([-\d.e]+) ([-\d.e]+)\)',
               lambda m: f"{m.group(1)}{_num(float(m.group(2)) / GLYPH_K)} {_num(float(m.group(3)) / GLYPH_K)})", s)
    s = re.sub(r">\s+<", "><", s)
    path.write_text(s, encoding="utf-8")


def fmt(v, nd=2):
    return f"{v:.{nd}f}".replace("-", "\u2013")


# ── 1. 데이터 분석: 하위집단 forest plot ───────────────────────────────
def sample_01():
    c = Canvas()
    c.frame("그림 2-1", "하위집단별 참여 효과(표준화 효과크기)",
            ["주. 양의 값은 참여군 우세. 4회 이상 참여에서만 효과가 뚜렷하며 1–3회는 유의하지 않음."])
    rows = [  # 집단, n, g, 하한, 상한 (합성 고정값)
        ("20–39세", 410, 0.44, 0.28, 0.60),
        ("40–59세", 480, 0.36, 0.21, 0.51),
        ("60세 이상", 310, 0.31, 0.12, 0.50),
        ("참여 1–3회", 520, 0.12, -0.05, 0.29),
        ("참여 4회 이상", 680, 0.55, 0.42, 0.68),
        ("전체", 1200, 0.38, 0.29, 0.47),
    ]
    ys = [178, 236, 294, 352, 410, 486]
    X = lambda g: 340 + (g + 0.2) / 1.0 * 440  # noqa: E731
    for lab, x, ha in (("집단", 48, "left"), ("n", 300, "right"), ("g", 912, "right")):
        c.text(x, 132, lab, 15, 600, FAINT, ha=ha)
    c.text(560, 132, "Hedges' g (95% CI)", 15, 600, FAINT, ha="center")
    c.line(48, 142, 912, 142)
    for t in (-0.2, 0, 0.2, 0.4, 0.6, 0.8):
        c.line(X(t), 150, X(t), 520, MUTED if t == 0 else LINE, 1)
        c.text(X(t), 544, fmt(t, 1), 15, 400, MUTED, ha="center")
    c.line(48, 448, 912, 448)
    for (lab, n, g, lo, hi), y in zip(rows, ys):
        hot = lo < 0 < hi
        col = ACCENT if hot else INK
        total = lab == "전체"
        c.text(48, y + 5, lab, 16, 700 if total else 400, BODY)
        c.text(300, y + 5, f"{n:,}", 15, 400, MUTED, ha="right")
        c.text(912, y + 5, fmt(g), 16, 600, ACCENT_T if hot else INK, ha="right")
        if total:
            c.ax.add_patch(Polygon([(X(lo), y), (X(g), y - 8), (X(hi), y), (X(g), y + 8)], closed=True, fc=INK, ec="none"))
        else:
            c.line(X(lo), y, X(hi), y, col, 2)
            c.dot(X(g), y, 12, col, marker="s")
    c.save("sample-01.svg")


# ── 2. AI/ML: ROC + 변수 중요도 ─────────────────────────────────────────
def sample_02():
    c = Canvas()
    c.frame("그림 4-3", "이탈 예측 모델 성능과 변수 중요도",
            ["주. 검증 세트(30%) 기준. 변수 중요도는 순열 중요도(AUC 감소량) 상위 6개."])
    nd = NormalDist()
    phi = lambda z: 0.5 * (1 + erf(z / sqrt(2)))  # noqa: E731
    fpr = np.linspace(0.0005, 0.9995, 201)
    x0, y0, s = 124, 516, 370  # 플롯 좌하단, 한 변
    P = lambda f, t: (x0 + s * f, y0 - s * t)  # noqa: E731
    c.text(48, 128, "A. ROC 곡선", 17, 600, INK)
    for v in (0.5,):
        c.line(*P(v, 0), *P(v, 1))
        c.line(*P(0, v), *P(1, v))
    c.line(*P(0, 0), *P(1, 1))
    c.line(*P(0, 0), *P(1, 0))
    for v, lab in ((0, "0"), (0.5, "0.5"), (1, "1.0")):
        c.text(x0 - 10, P(0, v)[1] + 5, lab, 15, 400, MUTED, ha="right")
    c.text(x0, y0 + 24, "0", 15, 400, MUTED, ha="center")
    c.text(x0 + s, y0 + 24, "1.0", 15, 400, MUTED, ha="center")
    c.text(x0 + s / 2, y0 + 24, "위양성률", 15, 600, MUTED, ha="center")
    c.text(62, y0 - s / 2, "진양성률", 15, 600, MUTED, ha="center", va="center", rotation=90)
    curves = {}
    for a, col in ((1.09, DMUTED), (1.60, INK)):  # binormal ROC, b=1
        tpr = np.array([phi(a + nd.inv_cdf(f)) for f in fpr])
        xs, ys = zip(*(P(0, 0), *[P(f, t) for f, t in zip(fpr, tpr)], P(1, 1)))
        c.path(xs, ys, col, 2)
        curves[a] = phi(a / sqrt(2))
    # 범례
    for i, (a, col, name) in enumerate(((1.60, INK, "최종 모델"), (1.09, DMUTED, "기준 모델"))):
        y = 458 + 26 * i
        c.line(318, y - 5, 342, y - 5, col, 2)
        c.text(352, y, name, 15, 400, MUTED)
        c.text(x0 + s - 8, y, f"AUC {curves[a]:.2f}", 15, 600, INK, ha="right")
    # 운영 임계값 점 (강조 1개)
    ft = 0.20
    tt = phi(1.60 + nd.inv_cdf(ft))
    px, py = P(ft, tt)
    ly = P(0, 0.93)[1]  # 곡선 위쪽 빈 영역에 라벨, 점까지 헤어라인 지시선
    c.line(px, ly + 8, px, py - 9)
    c.dot(px, py, 12, ACCENT)
    c.text(x0 + 16, ly, "운영 임계값 0.35", 16, 600, ACCENT_T)
    # 패널 구분선
    c.line(520, 116, 520, 552)
    # B. 변수 중요도
    c.text(548, 128, "B. 변수 중요도(순열, AUC 감소)", 17, 600, INK)
    names = ["최근 접속 간격", "월 이용 횟수", "가입 기간", "문의 건수", "결제 실패 횟수", "요금제 유형"]
    vals = [0.182, 0.141, 0.097, 0.064, 0.041, 0.023]
    bx, scale = 680, 170 / 0.182
    c.line(bx, 160, bx, 520)
    for i, (n, v) in enumerate(zip(names, vals)):
        y = 190 + 60 * i
        c.text(548, y + 5, n, 15, 400, BODY)
        c.rect(bx, y - 10, v * scale, 20, INK)
        c.text(bx + v * scale + 8, y + 5, f"{v:.3f}", 15, 400, MUTED)
    c.save("sample-02.svg")


# ── 3. 컨설팅: 우선순위 매트릭스 ────────────────────────────────────────
def sample_03():
    c = Canvas()
    c.frame("그림 1-2", "분석 과제 우선순위 매트릭스",
            ["주. 기대 효과·난이도는 워크숍 평가 평균(1–10). 좌상단이 우선 추진 영역."])
    x0, x1, y0, y1 = 128, 880, 124, 528
    X = lambda v: x0 + (x1 - x0) * v / 10  # noqa: E731
    Y = lambda v: y1 - (y1 - y0) * v / 10  # noqa: E731
    c.rect(x0, y0, X(5) - x0, Y(5) - y0, BG)
    c.rect(x0, y0, x1 - x0, y1 - y0, "none", LINE, 1)
    c.line(X(5), y0, X(5), y1)
    c.line(x0, Y(5), x1, Y(5))
    c.text(72, (y0 + y1) / 2, "기대 효과", 15, 600, MUTED, ha="center", va="center", rotation=90)
    c.text(116, y0 + 12, "높음", 15, 400, FAINT, ha="right")
    c.text(116, y1, "낮음", 15, 400, FAINT, ha="right")
    c.text((x0 + x1) / 2, 552, "실행 난이도", 15, 600, MUTED, ha="center")
    c.text(x0, 552, "낮음", 15, 400, FAINT)
    c.text(x1, 552, "높음", 15, 400, FAINT, ha="right")
    for s, x, y, ha in (("우선 추진", x0 + 16, y0 + 28, "left"), ("전략 과제", x1 - 16, y0 + 28, "right"),
                        ("여유 시 추진", x0 + 16, y1 - 16, "left"), ("보류", x1 - 16, y1 - 16, "right")):
        c.text(x, y, s, 15, 600, FAINT, ha=ha)
    rng = np.random.default_rng(SEED)
    tasks = [  # 과제, 난이도, 효과, 라벨 방향
        ("리포트 자동화", 2.4, 7.9, "r"), ("품질 모니터링", 3.6, 6.6, "r"), ("이탈 조기경보", 6.8, 8.8, "r"),
        ("수요 예측", 7.9, 7.4, "r"), ("데이터 통합", 8.7, 6.1, "l"), ("설문 재설계", 2.1, 3.2, "r"),
        ("고객 세분화", 4.2, 4.4, "r"), ("가격 실험", 7.3, 2.6, "r"),
    ]
    jit = rng.uniform(-0.3, 0.3, size=(len(tasks), 2))
    for (name, dx, ey, side), (jx, jy) in zip(tasks, jit):
        hot = name == "리포트 자동화"
        x, y = X(dx + jx), Y(ey + jy)
        c.dot(x, y, 22 if hot else 18, ACCENT if hot else INK)
        off = 18 if hot else 16
        c.text(x + off if side == "r" else x - off, y + 6, name, 16, 600 if hot else 400,
               ACCENT_T if hot else BODY, ha="left" if side == "r" else "right")
    c.save("sample-03.svg")


# ── 4. 소프트웨어: 대시보드 목업 ───────────────────────────────────────
def sample_04():
    c = Canvas()
    c.frame("그림 5-1", "운영 대시보드 화면(요약 탭)",
            ["주. 화면 목업. 수치는 합성값이며 실제 운영 데이터가 아님."])
    c.rect(48, 108, 864, 444, BG)
    c.text(64, 138, "운영 현황", 17, 700, INK)
    c.text(896, 138, "최근 12주 · 주간", 15, 400, MUTED, ha="right")
    c.line(64, 150, 896, 150)
    tiles = [("총 처리 건수", "12,480", "+4.2% 전주"), ("평균 처리일", "3.6일", "–0.4일 전주"),
             ("지연 건수", "318", "+12.5% 전주"), ("만족도", "4.3", "+0.1 전주")]
    for i, (lab, val, delta) in enumerate(tiles):
        x = 64 + 212 * i
        hot = lab == "지연 건수"
        c.rect(x, 166, 196, 104, WHITE, LINE, 1)
        if hot:
            c.line(x, 167.5, x + 196, 167.5, ACCENT, 3)
        c.text(x + 16, 192, lab, 15, 400, MUTED)
        c.text(x + 16, 232, val, 32, 800, INK)
        c.text(x + 16, 256, delta, 15, 600, ACCENT_T if hot else MUTED)
    c.rect(64, 286, 832, 250, WHITE, LINE, 1)
    c.text(80, 312, "주간 처리 건수", 15, 600, INK)
    rng = np.random.default_rng(SEED)
    t = np.arange(12)
    v = np.rint(900 + 28 * t + 60 * np.sin(2 * np.pi * t / 6) + rng.normal(0, 35, 12))
    X = lambda i: 128 + (856 - 128) * i / 11  # noqa: E731
    Y = lambda k: 500 - (500 - 336) * (k - 800) / 500  # noqa: E731
    for k in (800, 1000, 1200):
        c.line(128, Y(k), 872, Y(k))
        c.text(116, Y(k) + 5, f"{k:,}", 15, 400, MUTED, ha="right")
    for i, lab in ((0, "1주"), (3, "4주"), (7, "8주"), (11, "12주")):
        c.text(X(i), 524, lab, 15, 400, MUTED, ha="center")
    c.path([X(i) for i in t], [Y(k) for k in v], INK, 2)
    c.dot(X(11), Y(v[-1]), 10, INK)
    c.text(X(11) - 10, Y(v[-1]) - 14, f"{int(v[-1]):,}", 16, 600, INK, ha="right")
    c.save("sample-04.svg")


# ── 5. 통계 조사: 리커트 diverging 누적 막대 + 교차표 ──────────────────
def sample_05():
    c = Canvas()
    c.frame("그림 3-4", "만족도 문항별 응답 분포와 교차표",
            ["주. n=800. 부정=매우 불만족+불만족, 긍정=만족+매우 만족.", "B 는 요금 적정성 문항만 발췌."])
    c.text(48, 128, "A. 문항별 응답 분포(%)", 17, 600, INK)
    cats = [("매우 불만족", MUTED), ("불만족", DSUB), ("보통", WHITE), ("만족", DMUTED), ("매우 만족", INK)]
    # 범례: 오른쪽 끝에서 왼쪽으로 배치
    x = 912
    for name, col in reversed(cats):
        t = c.text(x, 128, name, 15, 400, MUTED, ha="right")
        x -= c.width(t) + 6
        c.rect(x - 12, 117, 12, 12, col, LINE if col == WHITE else "none", 1)
        x -= 12 + 20
    items = [  # 매우불만, 불만, 보통, 만족, 매우만족 (%, 합성 고정값)
        ("응대 친절", [3, 9, 17, 46, 25]), ("처리 속도", [5, 14, 23, 41, 17]), ("정보 명확성", [4, 12, 26, 42, 16]),
        ("요금 적정성", [10, 21, 30, 30, 9]), ("재이용 의향", [4, 10, 20, 44, 22]),
    ]
    cx, k = 480, 4.6
    c.line(cx, 150, cx, 362, MUTED, 1)
    for i, (name, p) in enumerate(items):
        y = 170 + 44 * i
        hot = name == "요금 적정성"
        c.text(48, y + 6, name, 16, 400, BODY)
        if hot:
            c.line(48, y + 14, 120, y + 14, ACCENT, 2)
        left = cx - (p[0] + p[1] + p[2] / 2) * k
        xx = left
        for v, (_, col) in zip(p, cats):
            w = v * k
            c.rect(xx + 1, y - 12, w - 2, 24, col, LINE if col == WHITE else "none", 1)
            xx += w
        neg, pos = p[0] + p[1], p[3] + p[4]
        c.text(left - 8, y + 5, f"{neg}%", 15, 600, ACCENT_T if hot else INK, ha="right")
        c.text(xx + 8, y + 5, f"{pos}%", 15, 600, INK)
    c.line(48, 384, 912, 384)
    c.text(48, 410, "B. 요금 적정성 × 이용 기간(%)", 17, 600, INK)
    c.rect(48, 424, 864, 26, BG)
    cols = [("구분", 48, "left"), ("1년 미만", 560, "right"), ("1–3년", 736, "right"), ("3년 이상", 912, "right")]
    for s, x, ha in cols:
        c.text(x, 442, s, 15, 600, FAINT, ha=ha)
    c.line(48, 450, 912, 450, INK, 1)
    table = [("부정", ["42", "29", "21"]), ("긍정", ["30", "41", "48"]), ("n", ["260", "310", "230"])]
    for r, (lab, vals) in enumerate(table):
        y = 472 + 30 * r
        if r:
            c.line(48, y - 20, 912, y - 20)
        c.text(48, y, lab, 15, 400, BODY)
        for j, v in enumerate(vals):
            c.text(cols[j + 1][1], y, v, 15, 700 if (r == 0 and j == 0) else 400, BODY, ha="right")
    c.save("sample-05.svg")


# ── 6. 데이터 구축: 코드북 + 결측·품질 요약 ────────────────────────────
def sample_06():
    c = Canvas()
    c.frame("표 2-1", "코드북 발췌와 변수별 결측률",
            ["주. 전체 42개 변수 중 5개 발췌."])
    c.rect(48, 116, 864, 30, BG)
    heads = [("변수명", 48, "left"), ("라벨", 190, "left"), ("유형", 360, "left"), ("값 범위", 440, "left"),
             ("결측률", 912, "right")]
    for s, x, ha in heads:
        c.text(x, 136, s, 15, 600, FAINT, ha=ha)
    c.line(48, 146, 912, 146, INK, 1)
    rows = [("resp_id", "응답자 ID", "문자", "고유값", 0.0), ("age", "연령", "정수", "18–89", 1.2),
            ("region", "거주 지역", "범주", "1–17", 0.4), ("income", "월 소득(만원)", "연속", "0–2,000", 18.7),
            ("sat_q4", "만족도 문항 4", "순서", "1–5", 6.1)]
    for i, (var, lab, typ, rng_, miss) in enumerate(rows):
        y = 172 + 40 * i
        hot = var == "income"
        if i:
            c.line(48, y - 26, 912, y - 26)
        c.text(48, y, var, 15, 600, INK)
        c.text(190, y, lab, 15, 400, BODY)
        c.text(360, y, typ, 15, 400, BODY)
        c.text(440, y, rng_, 15, 400, BODY)
        if miss > 0:
            c.rect(660, y - 11, miss / 20 * 180, 12, ACCENT if hot else MUTED)
        c.text(912, y, f"{miss:.1f}%", 15, 600 if hot else 400, ACCENT_T if hot else MUTED, ha="right")
    y_end = 146 + 40 * len(rows)
    c.line(48, y_end, 912, y_end, INK, 1)
    q = y_end + 44  # 품질 요약 블록 기준선
    c.text(48, q, "데이터 품질 요약", 17, 600, INK)
    cells = [("총 레코드", "12,480", 28, 800), ("중복 제거", "36건", 28, 800), ("결측 처리", "다중대체(m=5)", 22, 700)]
    for i, (lab, val, size, w) in enumerate(cells):
        x = 48 + 288 * i
        pad = 0 if i == 0 else 16
        if i:
            c.line(x, q + 20, x, q + 108)
        c.text(x + pad, q + 42, lab, 15, 400, MUTED)
        c.text(x + pad, q + 84, val, size, w, INK)
    c.save("sample-06.svg")


if __name__ == "__main__":
    for fn in (sample_01, sample_02, sample_03, sample_04, sample_05, sample_06):
        fn()
    for p in sorted(OUT.glob("sample-*.svg")):
        print(f"{p.name}\t{p.stat().st_size / 1024:.1f} KB")
