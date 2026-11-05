"""Plotly figures and HTML fragments that reproduce each panel of the HTML dashboard."""
from __future__ import annotations

import math
from datetime import date

import numpy as np
import plotly.graph_objects as go

from . import data as dd
from .fmt import dfmt, mname, money, money_axis, nice_ticks, num, pct, spct
from .style import BAD, DIM, GOLD, GOLD_LIGHT, GOOD, GRID, LINE, MONO, MUTED, NAVY, PAL, REGCOL

ACCENT = GOLD
FIG_CFG = {"displayModeBar": False, "responsive": True}


# ---------------------------------------------------------------- base figure
def base(height=280, top_pad=0, showlegend=False):
    fig = go.Figure()
    fig.update_layout(
        height=height, margin=dict(l=8, r=10, t=8 + top_pad, b=8), paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family=MONO, size=11, color=MUTED), showlegend=showlegend, hovermode="closest",
        hoverlabel=dict(bgcolor=NAVY, font=dict(family=MONO, size=12, color="#fff"), bordercolor=NAVY),
        bargap=0.12,
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor=LINE, tickfont=dict(family=MONO, size=11, color=MUTED))
    fig.update_yaxes(gridcolor=GRID, zeroline=False, linecolor="rgba(0,0,0,0)", tickfont=dict(family=MONO, size=11, color=MUTED))
    return fig


def money_yaxis(fig, vmax, pad_top=1.0, nticks=5):
    ticks, top = nice_ticks(vmax, nticks)
    f = money_axis(top)
    fig.update_yaxes(tickvals=ticks, ticktext=[f(t) for t in ticks], range=[0, top * pad_top])
    return top


def pct_yaxis(fig, vmax, nticks=4, fmt=lambda v: f"{v * 100:g}%"):
    ticks, top = nice_ticks(vmax, nticks)
    fig.update_yaxes(tickvals=ticks, ticktext=[fmt(t) for t in ticks], range=[0, top])
    return top


def nice_range(lo, hi, n=5):
    lo, hi = min(lo, 0), max(hi, 0)
    span = (hi - lo) or 1
    raw = span / n
    p = 10 ** math.floor(math.log10(raw))
    f = raw / p
    step = (1 if f <= 1 else 2 if f <= 2 else 2.5 if f <= 2.5 else 5 if f <= 5 else 10) * p
    a = math.floor(lo / step - 1e-9) * step
    b = math.ceil(hi / step - 1e-9) * step
    ticks, v = [], a
    while v <= b + step / 1e6:
        ticks.append(round(v, 8))
        v += step
    return ticks, a, b


def fmt_pct_axis(v):
    return "0%" if abs(v) < 1e-9 else f"{v * 100:.1f}".rstrip("0").rstrip(".") + "%"


# ---------------------------------------------------------------- tiles
def tiles_html(S, sel):
    s_fy, s_m = dd.series(sel)
    a_fy, a_m = dd.series(dd.ALL)
    i = dd.yi(S["year"])
    v = s_fy[i]
    p = s_fy[i - 1] if i > 0 else None
    tot = a_fy[i]
    reg = dd.sel_region(sel)
    reg_t = dd.series(("region", reg))[0][i] if reg else None
    cards = []

    def mk(lab, val, sub, color, cls=""):
        cards.append(f'<div class="tile" style="--tc:{color}"><div class="lab">{lab}</div>'
                     f'<div class="val {cls}">{val}</div><div class="sub">{sub}</div></div>')

    mk(f"FY{S['year']} received", money(v), dd.sel_name(sel), GOLD_LIGHT)
    cum, cum_all = s_m.sum(), a_m.sum()
    extra = "" if sel[0] == "all" else f" · {pct(cum / cum_all)} of all-time total"
    mk("Total since records began", money(cum), f"{mname(dd.MONTHS[0])} – {mname(dd.MONTHS[-1])}{extra}", "#1f5fd6")
    g = (v / p - 1) if p else None
    mk(f"Change on FY{S['year'] - 1}", spct(g) if p else "—", f"Year before: {money(p)}" if p else "No earlier year",
       GOOD, ("up" if g >= 0 else "down") if p else "")
    mk("Share of all remittances", pct(v / tot) if tot else "—", f"All countries: {money(tot)}", GOLD)
    if sel[0] == "all":
        best = sorted(((r, dd.series(("region", r))[0][i]) for r in dd.REGIONS), key=lambda x: -x[1])[0]
        mk("Largest region", best[0], f"{pct(best[1] / tot)} of the total", "#7c4dff")
    elif sel[0] == "region":
        best = sorted(((c["name"], c["fy"][i]) for c in dd.C if c["region"] == reg), key=lambda x: -x[1])[0]
        mk("Largest country in region", best[0], f"{pct(best[1] / reg_t if reg_t else 0)} of {reg}", "#7c4dff")
    else:
        mk(f"Share of {reg}", pct(v / reg_t) if reg_t else "—", f"{reg}: {money(reg_t)}", "#7c4dff")
    pk = max(dd.FULL, key=lambda y: s_fy[dd.yi(y)])
    mk("Record fiscal year", f"FY{pk}", money(s_fy[dd.yi(pk)]), "#1597b3")
    return '<div class="tiles">' + "".join(cards) + "</div>"


# ---------------------------------------------------------------- annual
def annual_fig(S, sel):
    fy, _ = dd.series(sel)
    years = dd.FULL
    vals = [fy[dd.yi(y)] for y in years]
    fig = base(280)
    yoy = [spct(vals[k] / vals[k - 1] - 1) if k and vals[k - 1] > 0 else "—" for k in range(len(years))]
    fig.add_bar(x=years, y=vals, marker_color=[ACCENT if y == S["year"] else DIM for y in years],
                customdata=np.column_stack([[money(v) for v in vals], yoy]),
                hovertemplate="<b>FY%{x}</b><br>Received: %{customdata[0]}<br>On year before: %{customdata[1]}<extra></extra>")
    money_yaxis(fig, max(vals))
    fig.update_xaxes(tickvals=[y for y in years if y % 5 == 0], range=[years[0] - 0.7, years[-1] + 0.7])
    fig.update_layout(bargap=0.18, clickmode="event+select")
    return fig


def share_fig(S, sel):
    fy, _ = dd.series(sel)
    a_fy, _ = dd.series(dd.ALL)
    years = dd.FULL
    vals = [fy[dd.yi(y)] / a_fy[dd.yi(y)] if a_fy[dd.yi(y)] else 0 for y in years]
    fig = base(260)
    fig.add_scatter(x=years, y=vals, mode="lines", line=dict(color=ACCENT, width=3), fill="tozeroy",
                    fillcolor="rgba(184,134,11,.12)",
                    customdata=np.column_stack([[money(fy[dd.yi(y)]) for y in years], [money(a_fy[dd.yi(y)]) for y in years]]),
                    hovertemplate="<b>FY%{x}</b><br>Share of all remittances: %{y:.1%}<br>Received: %{customdata[0]}"
                                  "<br>All countries: %{customdata[1]}<extra></extra>")
    k0 = years.index(S["year"])
    fig.add_vline(x=S["year"], line=dict(color=MUTED, dash="dash", width=1))
    fig.add_scatter(x=[S["year"]], y=[vals[k0]], mode="markers+text", marker=dict(color=ACCENT, size=10, line=dict(color="#fff", width=2)),
                    text=[f"FY{S['year']} {pct(vals[k0])}"], textposition="top center", textfont=dict(color=NAVY, family=MONO, size=11),
                    hoverinfo="skip")
    pct_yaxis(fig, max(max(vals), 0.01), 5, lambda v: f"{v * 100:.1f}".rstrip("0").rstrip(".") + "%")
    fig.update_xaxes(tickvals=[y for y in years if y % 5 == 0])
    return fig


# ---------------------------------------------------------------- macro
def macro_fig(S, sel, key, solid_end):
    fy, _ = dd.series(sel)
    den = dd.D["macro"][key]
    pts = []
    for y in dd.FULL:
        dv = den[dd.yi(y)]
        if dv:
            pts.append((y, dv, fy[dd.yi(y)], fy[dd.yi(y)] / (dv * 1000)))
    cur = next((p for p in pts if p[0] == S["year"]), None)
    big = f"{pct(cur[3])} in FY{S['year']}" if cur else f"— (not available for FY{S['year']})"
    name = {"exp": "Exports", "ppp": "GDP (PPP)", "gdp": "GDP"}[key]
    fig = base(220)
    solid = [p for p in pts if p[0] <= solid_end]
    dash = [p for p in pts if p[0] >= solid_end]

    def cd(a):
        return np.column_stack([[money(p[2]) for p in a], [f"${p[1]:.{1 if p[1] < 100 else 0}f}bn" for p in a]])

    ht = "<b>FY%{x}</b><br>Share: %{y:.1%}<br>Remittances: %{customdata[0]}<br>" + name + ": %{customdata[1]}<extra></extra>"
    fig.add_scatter(x=[p[0] for p in solid], y=[p[3] for p in solid], mode="lines", line=dict(color=ACCENT, width=3),
                    fill="tozeroy", fillcolor="rgba(184,134,11,.12)", customdata=cd(solid), hovertemplate=ht)
    if len(dash) > 1:
        fig.add_scatter(x=[p[0] for p in dash], y=[p[3] for p in dash], mode="lines", line=dict(color=ACCENT, width=3, dash="dot"),
                        customdata=cd(dash), hovertemplate=ht + "")
    if cur:
        fig.add_scatter(x=[cur[0]], y=[cur[3]], mode="markers", marker=dict(color=ACCENT, size=10, line=dict(color="#fff", width=2)), hoverinfo="skip")
    pct_yaxis(fig, max(p[3] for p in pts) if pts else 0.001, 4, fmt_pct_axis)
    fig.update_xaxes(tickvals=[y for y in (1980, 1990, 2000, 2010, 2020) if y >= pts[0][0]], range=[dd.FY0, dd.LASTFULL + 0.5])
    return fig, big


# ---------------------------------------------------------------- shocks
SH = []
for x in dd.D["shocks"]:
    y, m = int(x["ym"][:4]), int(x["ym"][5:])
    fy = y + 1 if m >= 7 else y
    SH.append({**x, "t": (fy - dd.FY0) + ((m + 5) % 12) / 12 + 0.5 / 12})


def shocks_fig(S, sel, mode):
    fy, _ = dd.series(sel)
    years = dd.FULL
    vals = [fy[dd.yi(y)] for y in years]
    gr = [vals[k] / vals[k - 1] - 1 if k and vals[k - 1] > 0 else None for k in range(len(years))]
    fig = base(360)
    if mode == "level":
        ticks, top = nice_ticks(max(vals + [1]), 5)
        f = money_axis(top)
        lo, hi = 0, top
        tt = [f(t) for t in ticks]
        fig.add_bar(x=years, y=vals, marker_color=[ACCENT if y == S["year"] else DIM for y in years],
                    customdata=np.column_stack([[money(v) for v in vals], [spct(g) if g is not None else "—" for g in gr]]),
                    hovertemplate="<b>FY%{x}</b><br>Received: %{customdata[0]}<br>On year before: %{customdata[1]}<extra></extra>")
    else:
        gg = [g for g in gr if g is not None]
        ticks, lo, hi = nice_range(min(gg + [0]), max(gg + [0.1]), 5)
        tt = [fmt_pct_axis(t) for t in ticks]
        fig.add_bar(x=years, y=[g if g is not None else 0 for g in gr],
                    marker_color=[(GOOD if (g or 0) >= 0 else BAD) for g in gr],
                    opacity=1,
                    customdata=np.column_stack([[money(v) for v in vals], [spct(g) if g is not None else "—" for g in gr]]),
                    hovertemplate="<b>FY%{x}</b><br>Received: %{customdata[0]}<br>On year before: %{customdata[1]}<extra></extra>")
    span = hi - lo
    r_hi = hi + span * 0.34
    row_y = {0: hi + span * 0.27, 1: hi + span * 0.12}
    for x in SH:
        xx = dd.FY0 + x["t"] - 0.5
        yy = row_y[x["n"] % 2]
        fig.add_shape(type="line", x0=xx, x1=xx, y0=yy, y1=lo if mode != "level" else 0,
                      line=dict(color=NAVY, width=1.2, dash="dot"), opacity=0.5, layer="below")
        txt = x["text"] if len(x["text"]) <= 80 else x["text"][:78] + "…"
        fig.add_scatter(x=[xx], y=[yy], mode="markers+text", text=[str(x["n"])],
                        marker=dict(size=21, color=ACCENT, line=dict(color=NAVY, width=1.5)),
                        textfont=dict(color="#fff", family=MONO, size=11), showlegend=False,
                        hovertemplate=f"<b>{mname(x['ym'])} · {x['name']}</b><br>{txt}<extra></extra>")
    fig.update_yaxes(tickvals=ticks, ticktext=tt, range=[lo, r_hi])
    fig.update_xaxes(tickvals=[y for y in years if y % 5 == 0], range=[years[0] - 0.7, years[-1] + 0.7])
    if mode != "level":
        fig.add_hline(y=0, line=dict(color=NAVY, width=1.5))
    fig.update_layout(bargap=0.16)
    return fig


def events_html():
    out = []
    for x in SH:
        out.append(f'<div class="ev"><span class="bd">{x["n"]}</span><div><b>{mname(x["ym"])} · {x["name"]}</b>'
                   f'<span class="tx">{x["text"]}</span></div></div>')
    return '<div class="evlist">' + "".join(out) + "</div>"


# ---------------------------------------------------------------- monthly
def monthly_fig(sel):
    _, m = dd.series(sel)
    n = 60
    a = dd.NM - n
    vals, labs = m[a:], dd.MONTHS[a:]
    x = [f"{l}-15" for l in labs]
    fig = base(280, top_pad=14)
    fig.add_scatter(x=x, y=vals, mode="lines", line=dict(color=ACCENT, width=3, shape="linear"), fill="tozeroy",
                    fillcolor="rgba(184,134,11,.12)",
                    customdata=[[mname(l), money(v)] for l, v in zip(labs, vals)],
                    hovertemplate="<b>%{customdata[0]}</b><br>Received: %{customdata[1]}<extra></extra>")
    pk = int(np.argmax(vals))
    if vals[pk] > 0:
        fig.add_scatter(x=[x[pk]], y=[vals[pk]], mode="markers+text", marker=dict(color=ACCENT, size=9),
                        text=[f"{mname(labs[pk])} {money(vals[pk])}"], textposition="top center",
                        textfont=dict(color=NAVY, family=MONO, size=11), hoverinfo="skip", cliponaxis=False)
    top = money_yaxis(fig, max(vals), 1.08)
    jan = [l for l in labs if l.endswith("-01")][:]
    fig.update_xaxes(tickvals=[f"{l}-01" for l in jan[1:] if True], ticktext=[l[:4] for l in jan[1:]])
    return fig


# ---------------------------------------------------------------- horizontal bars (html)
def hbars_html(items, on_id=None):
    mx = max([x["frac"] for x in items] + [1e-9])
    rows = []
    for it in items:
        rows.append(
            f'<div class="row{" on" if on_id == it["id"] else ""}"><span class="nm">{it["name"]}</span>'
            f'<div class="track"><div class="fill" style="width:{it["frac"] / mx * 100:.1f}%;background:{it["color"]}"></div></div>'
            f'<span class="num"><b>{pct(it["frac"])}</b>&nbsp; {money(it["v"])}</span></div>')
    return '<div class="hb">' + "".join(rows) + "</div>"


def region_bars_html(S, sel):
    i = dd.yi(S["year"])
    tot = dd.series(dd.ALL)[0][i]
    items = [{"id": r, "name": r, "color": REGCOL[r], "v": dd.series(("region", r))[0][i]} for r in dd.REGIONS]
    items.sort(key=lambda x: -x["v"])
    for x in items:
        x["frac"] = x["v"] / tot if tot else 0
    return hbars_html(items, dd.sel_region(sel))


# ---------------------------------------------------------------- stacked
def legend_html(items, active=None):
    return '<div class="leg">' + "".join(
        f'<span style="{"border-color:#0b1f4b;font-weight:800" if active == it["name"] else ""}"><i style="background:{it["color"]}"></i>{it["name"]}</span>'
        for it in items) + "</div>"


def stacked_fig(years, series, percent=False, hl=None, mark=None):
    tot = [sum(s["vals"][k] for s in series) for k in range(len(years))]
    fig = base(300, showlegend=False)
    ymax = 1 if percent else max(tot)
    labels = [f"FY{str(y)[2:]}" for y in years]
    ticks, top = nice_ticks(ymax, 5)
    for s in series:
        share = [s["vals"][k] / tot[k] if tot[k] else 0 for k in range(len(years))]
        y = share if percent else s["vals"]
        axis_frac = share if percent else [(v / top if top else 0) for v in s["vals"]]
        text = [f"{round(sh * 100)}%" if af >= 0.05 else "" for sh, af in zip(share, axis_frac)]
        dim = hl is not None and hl != s["name"]
        fig.add_bar(x=labels, y=y, name=s["name"], marker_color=s["color"], opacity=0.3 if dim else 1,
                    text=text, textposition="inside", insidetextanchor="middle",
                    textfont=dict(color="#fff", family=MONO, size=10),
                    customdata=np.column_stack([[pct(v) for v in share], [money(v) for v in s["vals"]]]),
                    hovertemplate="%{fullData.name}: <b>%{customdata[0]}</b> · %{customdata[1]}<extra></extra>")
    fig.update_layout(barmode="stack", bargap=0.18, hovermode="x unified")
    if percent:
        fig.update_yaxes(tickvals=[0, .2, .4, .6, .8, 1], ticktext=["0%", "20%", "40%", "60%", "80%", "100%"], range=[0, 1])
    else:
        f = money_axis(top)
        fig.update_yaxes(tickvals=ticks, ticktext=[f(t) for t in ticks], range=[0, top])
    if mark and mark in years:
        k = years.index(mark)
        fig.add_vline(x=k - 0.5, line=dict(color=MUTED, dash="dash", width=1))
    return fig


def mix_series(years):
    return [{"name": r, "color": REGCOL[r], "vals": [dd.series(("region", r))[0][dd.yi(y)] for y in years]} for r in dd.REGIONS]


def inside_data(S, sel):
    i = dd.yi(S["year"])
    reg = dd.sel_region(sel) or dd.REGIONS[0]
    cs = [c for c in dd.C if c["region"] == reg]
    reg_t = dd.series(("region", reg))[0][i]
    items = sorted(({"id": c["id"], "name": c["name"], "v": c["fy"][i], "color": REGCOL[reg]} for c in cs if c["fy"][i] > 0),
                   key=lambda x: -x["v"])
    for x in items:
        x["frac"] = x["v"] / reg_t if reg_t else 0
    years = [y for y in dd.FULL if y >= 2011]
    order = sorted(cs, key=lambda c: -c["fy"][i])
    top, rest = order[:7], order[7:]
    sr = [{"name": c["name"], "color": PAL[k], "vals": [c["fy"][dd.yi(y)] for y in years]} for k, c in enumerate(top)]
    if rest:
        sr.append({"name": "Others in region", "color": DIM, "vals": [sum(c["fy"][dd.yi(y)] for c in rest) for y in years]})
    hl = None
    if S["country"] != "all" and S["country"] not in dd.AGG:
        nm = dd.BY_ID[S["country"]]["name"]
        hl = nm if any(s["name"] == nm for s in sr) else None
    return reg, reg_t, items, years, sr, hl


# ---------------------------------------------------------------- eid
def _mi(d):
    return (int(d[:4]) - 1972) * 12 + (int(d[5:7]) - 7)


EIDS = [{"type": e["type"], "date": e["date"], "idx": _mi(e["date"]), "day": int(e["date"][8:])} for e in dd.D["eids"]]
EIDS = [e for e in EIDS if 0 <= e["idx"] < dd.NM]
EIDNAME = {"fitr": "Eid al-Fitr", "adha": "Eid al-Adha"}
EIDCOL = {"fitr": PAL[1], "adha": PAL[2]}
AFF = set()
for _e in EIDS:
    AFF.add(_e["idx"])
    AFF.add(_e["idx"] - 1)


def eid_fig(sel, years):
    _, m = dd.series(sel)
    n = min(dd.NM, years * 12)
    a = dd.NM - n
    vals = m[a:]
    labs = dd.MONTHS[a:]
    x = [f"{l}-15" for l in labs]
    vmax = max(list(vals) + [1])
    ticks, top = nice_ticks(vmax, 5)
    fig = base(310)
    x_lo, x_hi = f"{labs[0]}-01", f"{labs[-1]}-28"
    for r in dd.D["ramadan"]:
        s0 = max(r["start"], x_lo)
        e0 = min(r["end"], x_hi)
        if e0 <= s0:
            continue
        fig.add_vrect(x0=s0, x1=e0, fillcolor=PAL[4], opacity=0.22, line_width=0, layer="below")
    fig.add_scatter(x=x, y=vals, mode="lines", line=dict(color=ACCENT, width=2.5),
                    customdata=[[mname(l), money(v)] for l, v in zip(labs, vals)],
                    hovertemplate="<b>%{customdata[0]}</b><br>Received: %{customdata[1]}<extra></extra>")
    ymark = top * 1.12
    for t in ("fitr", "adha"):
        ev = [e for e in EIDS if e["type"] == t and x_lo <= e["date"] <= x_hi]
        if not ev:
            continue
        for e in ev:
            fig.add_shape(type="line", x0=e["date"], x1=e["date"], y0=0, y1=ymark, line=dict(color=EIDCOL[t], width=2, dash="dot"))
        fig.add_scatter(x=[e["date"] for e in ev], y=[ymark] * len(ev), mode="markers+text", text=["F" if t == "fitr" else "A"] * len(ev),
                        marker=dict(size=20, color=EIDCOL[t], line=dict(color=NAVY, width=1.5)),
                        textfont=dict(color="#fff", family=MONO, size=11), cliponaxis=False,
                        customdata=[[EIDNAME[t], dfmt(e["date"]), mname(dd.MONTHS[e["idx"]]), money(m[e["idx"]])] for e in ev],
                        hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>%{customdata[2]} received: %{customdata[3]}<extra></extra>")
    fig.update_yaxes(tickvals=ticks, ticktext=[money_axis(top)(t) for t in ticks], range=[0, top * 1.2])
    jan = [l for l in labs if l.endswith("-01")]
    fig.update_xaxes(tickvals=[f"{l}-01" for l in jan[1:]], ticktext=[l[:4] for l in jan[1:]], range=[x_lo, x_hi])
    return fig


def eid_effect(sel, from_fy):
    _, s = dd.series(sel)
    recs = []
    for e in EIDS:
        ym = dd.MONTHS[e["idx"]]
        fy = int(ym[:4]) + 1 if int(ym[5:]) >= 7 else int(ym[:4])
        if fy < from_fy:
            continue
        run = e["idx"] if e["day"] >= 16 else e["idx"] - 1
        if run < 0:
            continue
        base_ = [s[j] for j in range(max(0, run - 6), min(dd.NM - 1, run + 6) + 1) if j not in AFF and s[j] > 0]
        if len(base_) < 3 or not s[run] > 0:
            continue
        b = sum(base_) / len(base_)
        recs.append({"e": e, "run": run, "b": b, "u": s[run] / b - 1, "v": s[run]})
    if len(recs) < 3:
        return None, "Not enough monthly data for this selection in the chosen period."
    fig = base(300)
    us = [r["u"] for r in recs]
    ticks, lo, hi = nice_range(min(us), max(us), 5)
    fig.add_bar(x=list(range(len(recs))), y=us, marker_color=[EIDCOL[r["e"]["type"]] for r in recs],
                customdata=[[EIDNAME[r["e"]["type"]], dfmt(r["e"]["date"]), mname(dd.MONTHS[r["run"]]), money(r["v"]), money(r["b"]), spct(r["u"])] for r in recs],
                hovertemplate="<b>%{customdata[0]} · %{customdata[1]}</b><br>Run-up month: %{customdata[2]}<br>Received: %{customdata[3]}"
                              "<br>Usual level: %{customdata[4]}<br>Difference: %{customdata[5]}<extra></extra>")
    fig.update_yaxes(tickvals=ticks, ticktext=[fmt_pct_axis(t) for t in ticks], range=[lo, hi])
    fig.add_hline(y=0, line=dict(color=NAVY, width=1.5))
    tv = [k for k in range(len(recs)) if k % 2 == 0 or len(recs) < 14]
    fig.update_xaxes(tickvals=tv, ticktext=["'" + recs[k]["e"]["date"][2:4] for k in tv])
    fig.update_layout(bargap=0.15)

    def mean(a):
        return sum(a) / len(a) if a else float("nan")

    fi = [r["u"] for r in recs if r["e"]["type"] == "fitr"]
    ad = [r["u"] for r in recs if r["e"]["type"] == "adha"]
    last = [r["u"] for r in recs[-8:]]
    up = sum(1 for r in recs if r["u"] > 0)
    summ = (f"On average the run-up month is {spct(mean(us))} against its usual level (Eid al-Fitr {spct(mean(fi))}, "
            f"Eid al-Adha {spct(mean(ad))}), and it was higher in {up} of {len(recs)} cases. For the latest eight Eids the "
            f"average is {spct(mean(last))}. Other things move the monthly figure too, so read this as a pattern, not a precise effect.")
    return fig, summ


# ---------------------------------------------------------------- table
def table_html(S, sel):
    i = dd.yi(S["year"])
    all_fy = dd.series(dd.ALL)[0]
    heads = ["Region / country", f"FY{S['year']}", "Share of region", "Share of total", f"FY{S['year'] - 1}", "Change"]

    def chg(v, p):
        return spct(v / p - 1) if p > 0 else "—"

    def cls(v, p):
        return "" if not p > 0 else ("up" if v >= p else "down")

    rows = []
    regs = []
    for r in dd.REGIONS:
        fy = dd.series(("region", r))[0]
        regs.append((r, fy[i], fy[i - 1] if i > 0 else 0))
    regs.sort(key=lambda x: -x[1])
    for r, v, p in regs:
        on = sel[0] == "region" and sel[1] == r
        rows.append(f'<tr class="reg{" on" if on else ""}"><td style="border-left:8px solid {REGCOL[r]}">{r}</td><td>{num(v)}</td><td>100%</td>'
                    f'<td>{pct(v / all_fy[i]) if all_fy[i] else "—"}</td><td>{num(p)}</td><td class="{cls(v, p)}">{chg(v, p)}</td></tr>')
        cs = [c for c in dd.C if c["region"] == r and (c["fy"][i] > 0 or (i > 0 and c["fy"][i - 1] > 0))]
        cs.sort(key=lambda c: -c["fy"][i])
        mxs = max([(c["fy"][i] / v if v else 0) for c in cs] + [1e-9])
        for c in cs:
            cv, cp = c["fy"][i], c["fy"][i - 1] if i > 0 else 0
            w = (cv / v / mxs * 100) if v else 0
            on = sel[0] == "country" and sel[1] == c["id"]
            bg = f"background-image:linear-gradient(90deg,{REGCOL[r]}52 {w:.1f}%,transparent {w:.1f}%)"
            rows.append(f'<tr class="ctry{" on" if on else ""}"><td>{c["name"]}</td><td>{num(cv)}</td>'
                        f'<td style="{bg}">{pct(cv / v) if v else "—"}</td><td>{pct(cv / all_fy[i]) if all_fy[i] else "—"}</td>'
                        f'<td>{num(cp)}</td><td class="{cls(cv, cp)}">{chg(cv, cp)}</td></tr>')
    p_all = all_fy[i - 1] if i > 0 else 0
    rows.append(f'<tr class="reg"><td>All countries</td><td>{num(all_fy[i])}</td><td></td><td>100%</td><td>{num(p_all)}</td><td>{chg(all_fy[i], p_all)}</td></tr>')
    return ('<div class="tabwrap"><table class="rt"><thead><tr>' + "".join(f"<th>{h}</th>" for h in heads) + "</tr></thead><tbody>"
            + "".join(rows) + "</tbody></table></div>")
