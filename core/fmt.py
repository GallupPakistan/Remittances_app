"""Number / date formatting helpers (match the HTML dashboard)."""
import math

MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def money(v: float) -> str:
    if v >= 1000:
        return f"${v / 1000:.2f}bn"
    return f"${v:.0f}m" if v >= 100 else f"${v:.1f}m"


def num(v: float) -> str:
    if v < 100:
        s = f"{v:,.1f}"
        return s[:-2] if s.endswith(".0") else s
    return f"{v:,.0f}"


def pct(x: float) -> str:
    if 0 < x < 0.001:
        return "<0.1%"
    return f"{x * 100:.1f}%"


def spct(x: float) -> str:
    return ("+" if x >= 0 else "−") + f"{abs(x) * 100:.1f}%"


def mname(ym: str) -> str:
    return f"{MON[int(ym[5:7]) - 1]} {ym[:4]}"


def dfmt(date: str) -> str:
    return f"{int(date[8:])} {MON[int(date[5:7]) - 1]} {date[:4]}"


def nice_ticks(vmax: float, n: int = 5):
    if not vmax > 0:
        vmax = 1
    raw = vmax / n
    p = 10 ** math.floor(math.log10(raw))
    f = raw / p
    step = (1 if f <= 1 else 2 if f <= 2 else 2.5 if f <= 2.5 else 5 if f <= 5 else 10) * p
    top = math.ceil(vmax / step - 1e-9) * step
    ticks, v = [], 0.0
    while v <= top + step / 1e6:
        ticks.append(round(v, 6))
        v += step
    return ticks, top


def money_axis(top: float):
    if top >= 2000:
        return lambda v: "$" + f"{v / 1000:.2f}".rstrip("0").rstrip(".") + "bn"
    return lambda v: f"${v:g}m"
