# Pretendard 가변 woff2 서브셋(static/fonts)을 굵기별 정적 TTF 하나로 합쳐 matplotlib 에 등록하는 도우미
from pathlib import Path

from fontTools.merge import Merger
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "static" / "fonts" / "pretendard"
CACHE = Path(__file__).resolve().parent / ".cache"
WEIGHTS = {400: "Regular", 600: "SemiBold", 700: "Bold", 800: "ExtraBold"}
FAMILY = "Pretendard DIL"


def _build(weight: int) -> Path:
    out = CACHE / f"pretendard-{weight}.ttf"
    if out.exists():
        return out
    CACHE.mkdir(exist_ok=True)
    parts = []
    for i, src in enumerate(sorted(SRC.glob("*.woff2"))):
        f = TTFont(src)
        f.flavor = None
        instancer.instantiateVariableFont(f, {"wght": weight}, inplace=True)
        for t in ("GSUB", "GPOS", "GDEF", "STAT"):  # 병합 충돌 방지 — 도표 텍스트엔 불필요
            if t in f:
                del f[t]
        p = CACHE / f"part-{weight}-{i}.ttf"
        f.save(p)
        parts.append(str(p))
    merged = Merger().merge(parts)
    for rec in merged["name"].names:
        if rec.nameID in (1, 16):
            rec.string = FAMILY
        elif rec.nameID in (2, 17):
            rec.string = WEIGHTS[weight]
        elif rec.nameID in (4, 6):
            rec.string = f"{FAMILY} {WEIGHTS[weight]}".replace(" ", "" if rec.nameID == 6 else " ")
    merged["OS/2"].usWeightClass = weight
    merged.save(out)
    for p in parts:
        Path(p).unlink()
    return out


def register() -> str:
    """굵기별 TTF 를 만들고(캐시) matplotlib 에 등록한 뒤 패밀리 이름을 돌려준다."""
    for w in WEIGHTS:
        font_manager.fontManager.addfont(str(_build(w)))
    return FAMILY
