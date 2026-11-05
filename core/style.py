"""Global CSS and shared page chrome: top bar, brand header, running ticker, filter bar."""
from __future__ import annotations

from contextlib import contextmanager

import streamlit as st

from . import data as dd
from .fmt import mname, money, pct, spct

# ---- palette (taken from the dashboard screenshots) ------------------------
NAVY = "#0b1f4b"
GOLD = "#b8860b"
GOLD_LIGHT = "#e8b923"
CREAM = "#fbf8ee"
BEIGE = "#f6efd9"
LINE = "#e6dcb8"
GRID = "#ece6d2"
MUTED = "#5b6477"
DIM = "#c8d1e8"
GOOD = "#0e8a5f"
BAD = "#d6264f"
PAL = ["#1f5fd6", "#e8710a", "#0e9f6e", "#7c4dff", "#b8a361", "#d92d2d", "#1597b3", "#8a5a2b"]
REGCOL = dict(zip(dd.REGIONS, PAL))
MONO = "'JetBrains Mono','IBM Plex Mono',Consolas,'Courier New',monospace"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&family=Libre+Baskerville:wght@700&display=swap');
:root {{ --navy:{NAVY}; --gold:{GOLD}; --cream:{CREAM}; --beige:{BEIGE}; --line:{LINE}; --muted:{MUTED};
  --good:{GOOD}; --bad:{BAD}; --mono:{MONO}; }}
html, body, [class*="stApp"] {{ background:{CREAM}; color:{NAVY}; }}
header[data-testid="stHeader"] {{ background:transparent; height:0; }}
[data-testid="stToolbar"], [data-testid="stDecoration"], footer {{ display:none !important; }}
.block-container {{ max-width:1340px; padding:0 1.2rem 3rem 1.2rem !important; }}
[data-testid="stSidebar"] {{ background:{BEIGE}; border-right:1px solid {LINE}; }}
[data-testid="stSidebarNav"] a span {{ font-family:{MONO}; font-size:13px; font-weight:600; color:{NAVY}; }}
.st-key-nav {{ border-bottom:1px solid {LINE}; margin-bottom:10px; }}
.st-key-nav a {{ border-radius:0; border-bottom:3px solid transparent; padding:.35rem .9rem; }}
.st-key-nav a p {{ font:700 12px {MONO}; letter-spacing:.08em; text-transform:uppercase; color:{MUTED}; }}
.st-key-nav a[aria-current="page"] {{ border-bottom-color:{GOLD_LIGHT}; background:{BEIGE}; }}
.st-key-nav a[aria-current="page"] p {{ color:{NAVY}; }}
h1,h2,h3 {{ font-family:'Segoe UI',Arial,sans-serif; color:{NAVY}; }}

/* top bar */
.topbar {{ display:flex; gap:26px; align-items:center; background:{NAVY}; color:#f3d98b; font:700 12px/1 {MONO};
  letter-spacing:.06em; text-transform:uppercase; padding:0 18px 0 0; margin:0 -1.2rem; height:26px; }}
.topbar b {{ background:{GOLD_LIGHT}; color:{NAVY}; padding:0 16px; height:26px; line-height:26px; }}
.topbar .r {{ margin-left:auto; }}
/* brand */
.brand {{ display:flex; justify-content:space-between; align-items:flex-start; margin:18px 0 8px; }}
.brand .mk {{ border-left:4px solid {GOLD_LIGHT}; padding-left:10px; line-height:1.05; }}
.brand .g1 {{ display:block; font:700 24px 'Libre Baskerville',Georgia,serif; letter-spacing:.07em; color:{NAVY}; }}
.brand .g2 {{ display:block; font:700 10px {MONO}; letter-spacing:.2em; color:{GOLD}; text-transform:uppercase; margin-top:3px; }}
.brand .tag {{ font:500 11px {MONO}; letter-spacing:.14em; color:{MUTED}; text-transform:uppercase; }}
.sticker {{ display:inline-block; border:1.5px solid {GOLD}; color:{GOLD}; font:700 11px {MONO}; letter-spacing:.08em; padding:3px 9px; margin:6px 0 10px; text-transform:uppercase; }}
.hero h1 {{ font:800 30px/1.2 'Segoe UI',Arial,sans-serif; margin:0 0 6px; color:{NAVY}; }}
.hero p {{ color:{MUTED}; font-size:15px; max-width:880px; margin:0 0 14px; border-bottom:1px solid {LINE}; padding-bottom:14px; }}
.pagetitle {{ font:800 26px/1.2 'Segoe UI',Arial,sans-serif; margin:2px 0 12px; }}

/* ticker */
.ticker {{ background:{NAVY}; overflow:hidden; white-space:nowrap; padding:10px 0; margin:0 0 14px; }}
.ticker .trk {{ display:inline-block; padding-left:0; animation:tick 55s linear infinite; }}
.ticker:hover .trk {{ animation-play-state:paused; }}
.ticker span {{ color:#f3d98b; font:700 13px {MONO}; margin:0 18px; }}
.ticker span.sep {{ color:#6f7fa8; margin:0 4px; font-weight:400; }}
@keyframes tick {{ from {{ transform:translateX(0); }} to {{ transform:translateX(-50%); }} }}

/* filter bar */
.st-key-filterbar {{ background:{BEIGE}; border:1px solid {LINE}; border-top:2px solid {GOLD_LIGHT}; padding:10px 14px 12px; margin-bottom:14px;
  position:sticky; top:0; z-index:50; }}
.st-key-filterbar label p {{ font:700 10px {MONO} !important; letter-spacing:.12em; color:{GOLD} !important; text-transform:uppercase; }}
.st-key-filterbar [data-baseweb="select"] > div {{ background:#fff; border:1px solid {LINE}; border-radius:2px; font:500 14px {MONO}; color:{NAVY}; min-height:38px; }}
.st-key-filterbar .stButton button {{ background:{NAVY}; color:#f3d98b; border:0; border-radius:2px; font:800 13px {MONO}; letter-spacing:.08em; padding:.45rem 1.1rem; margin-top:1.55rem; }}
.st-key-filterbar .stButton button:hover {{ background:{GOLD}; color:#fff; }}
.showing {{ text-align:right; font:500 13px {MONO}; color:{MUTED}; padding-top:1.9rem; }}
.showing b {{ color:{GOLD}; }}

/* tiles */
.tiles {{ display:grid; grid-template-columns:repeat(6,1fr); gap:10px; margin-bottom:14px; }}
.tile {{ background:#fff; border:1px solid {LINE}; border-top:3px solid var(--tc); padding:10px 14px 12px; min-width:0; }}
.tile .lab {{ font:700 10px {MONO}; letter-spacing:.1em; text-transform:uppercase; color:{MUTED}; }}
.tile .val {{ font:800 21px/1.3 {MONO}; color:{NAVY}; margin:4px 0 2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.tile .val.up {{ color:{GOOD}; }} .tile .val.down {{ color:{BAD}; }}
.tile .sub {{ font:400 11px {MONO}; color:{MUTED}; }}
@media (max-width:1000px) {{ .tiles {{ grid-template-columns:repeat(2,1fr); }} }}

/* cards */
[class*="st-key-card"] {{ background:#fff; border:1px solid {LINE}; border-top:2px solid {GOLD_LIGHT}; padding:14px 18px 14px; margin-bottom:14px; }}
[class*="st-key-card"] h2.ct {{ font:800 14px {MONO}; letter-spacing:.07em; text-transform:uppercase; color:{NAVY}; margin:0 0 6px; padding:0; }}
h2.ct::before {{ content:""; display:inline-block; width:9px; height:9px; background:{GOLD_LIGHT}; margin-right:10px; }}
p.note {{ color:{MUTED}; font-size:13px; line-height:1.5; margin:0 0 10px; }}
.macro-h {{ font:700 11px {MONO}; letter-spacing:.1em; text-transform:uppercase; color:{MUTED}; margin:0; }}
.macro-big {{ font:800 26px {MONO}; color:{GOLD}; margin:2px 0 4px; }}
[class*="st-key-card"] [data-testid="stSelectbox"] label p {{ font:500 13px {MONO}; color:{MUTED}; }}
[class*="st-key-card"] [data-baseweb="select"] > div {{ font:500 13px {MONO}; border-radius:2px; }}

/* legend chips */
.leg {{ display:flex; flex-wrap:wrap; gap:6px; margin:4px 0 8px; }}
.leg span {{ border:1px solid {LINE}; background:#fff; padding:3px 9px; font:500 12px {MONO}; color:{NAVY}; display:inline-flex; align-items:center; gap:6px; }}
.leg i {{ width:11px; height:11px; display:inline-block; }}

/* horizontal bars */
.hb .row {{ display:grid; grid-template-columns:190px 1fr 150px; align-items:center; gap:14px; margin:0 0 10px; font:500 13px {MONO}; }}
.hb .row.on .nm {{ font-weight:800; }}
.hb .track {{ background:#eee8d6; height:12px; }}
.hb .fill {{ height:100%; }}
.hb .num {{ text-align:right; white-space:nowrap; }}
.hb .num b {{ font-weight:800; }}

/* events list */
.evlist {{ display:grid; grid-template-columns:repeat(4,1fr); gap:10px 22px; margin-top:12px; }}
.ev {{ display:flex; gap:10px; padding:4px; }}
.ev .bd {{ flex:none; width:24px; height:24px; background:{NAVY}; color:#f3d98b; font:800 12px/24px {MONO}; text-align:center; }}
.ev b {{ display:block; font:700 13px 'Segoe UI',Arial,sans-serif; }}
.ev .tx {{ font-size:12.5px; color:{MUTED}; line-height:1.4; }}
@media (max-width:1000px) {{ .evlist {{ grid-template-columns:repeat(2,1fr); }} }}

/* table */
.tabwrap {{ max-height:620px; overflow:auto; }}
table.rt {{ width:100%; border-collapse:collapse; font:500 13px {MONO}; }}
table.rt th, table.rt td {{ border-left:0 !important; border-right:0 !important; border-top:0 !important; }}
table.rt th {{ position:sticky; top:0; background:{BEIGE}; text-transform:uppercase; font:700 10.5px {MONO}; letter-spacing:.1em; color:{GOLD}; padding:8px 10px; text-align:right; border-bottom:1px solid {LINE}; }}
table.rt th:first-child, table.rt td:first-child {{ text-align:left; }}
table.rt td {{ padding:6px 10px; text-align:right; border-bottom:1px solid #f0ead7; }}
table.rt tr.reg td {{ background:{BEIGE}; font-weight:800; border-bottom:1px solid {LINE}; }}
table.rt tr.ctry td:first-child {{ padding-left:26px; }}
table.rt tr.on td {{ outline:0; box-shadow:inset 0 0 0 9999px rgba(232,185,35,.18); }}
table.rt td.up {{ color:{GOOD}; font-weight:700; }} table.rt td.down {{ color:{BAD}; font-weight:700; }}
ul.about {{ margin:0; padding-left:20px; font-size:13.5px; line-height:1.55; color:{MUTED}; }}
ul.about li {{ margin:5px 0; }}
.brandfoot {{ border-top:2px solid {GOLD_LIGHT}; margin-top:18px; padding-top:12px; display:flex; flex-wrap:wrap; gap:8px 28px; align-items:baseline; font:500 12px {MONO}; color:{MUTED}; }}
.brandfoot b {{ font:700 15px 'Libre Baskerville',Georgia,serif; letter-spacing:.07em; color:{NAVY}; }}
.brandfoot .a {{ color:{GOLD}; font-weight:700; }}
.brandfoot .r {{ margin-left:auto; }}
</style>
"""


NAV = [("Overview.py", "Overview"), ("pages/1_Shocks_and_Monthly.py", "Shocks & Monthly"),
       ("pages/2_Eid_Effect.py", "Eid Effect"), ("pages/3_Regional_Mix.py", "Regional Mix"),
       ("pages/4_Regions_and_Countries.py", "Regions & Countries")]


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def card_title(text: str):
    st.markdown(f'<h2 class="ct">{text}</h2>', unsafe_allow_html=True)


def note(text: str, style: str = ""):
    st.markdown(f'<p class="note" style="{style}">{text}</p>', unsafe_allow_html=True)


@contextmanager
def card(key: str):
    with st.container(key=f"card_{key}"):
        yield


# ---- ticker ------------------------------------------------------------------
def ticker_html() -> str:
    all_s = dd.series(dd.ALL)
    li = dd.yi(dd.LASTFULL)
    cum = all_s[1].sum()
    pk = int(all_s[1].argmax())
    gulf = dd.series(("region", "Gulf (GCC)"))[0][li] / all_s[0][li]
    cand = [(c["name"], c["fy"][li]) for c in dd.C
            if c["id"] != "other" and c["id"] not in dd.AGG["uae_all"]["members"]]
    cand.append(("UAE", dd.series(("agg", "uae_all"))[0][li]))
    cand.sort(key=lambda x: -x[1])
    tot = all_s[0][li]
    facts = [
        f"{money(cum)} sent home since July 1972",
        f"FY{dd.LASTFULL}: {money(tot)} ({spct(tot / all_s[0][li - 1] - 1)})",
        f"Gulf supplies {pct(gulf)}",
        f"{cand[0][0]} is #1 at {pct(cand[0][1] / tot)}",
        f"{cand[1][0]} is #2 at {pct(cand[1][1] / tot)}",
        f"Record month: {mname(dd.MONTHS[pk])} {money(all_s[1][pk])}",
    ]
    one = "".join(f"<span>★ {f}</span><span class='sep'>|</span>" for f in facts) * 2
    return f'<div class="ticker"><div class="trk">{one}{one}</div></div>'


# ---- state + filters ---------------------------------------------------------
def init_state():
    if "S" not in st.session_state:
        st.session_state.S = {"region": "all", "country": "all", "year": dd.LASTFULL}
    return st.session_state.S


def _on_region():
    S = st.session_state.S
    S["region"] = st.session_state["w_region"]
    if S["country"] != "all" and S["region"] != "all" and dd.region_of_country(S["country"]) != S["region"]:
        S["country"] = "all"


def _on_country():
    S = st.session_state.S
    S["country"] = st.session_state["w_country"]


def _on_year():
    st.session_state.S["year"] = st.session_state["w_year"]


def _reset():
    st.session_state.S.update({"region": "all", "country": "all", "year": dd.LASTFULL})


def set_year(y: int):
    st.session_state.S["year"] = int(y)


def filter_bar():
    S = init_state()
    sel = dd.cur_sel(S)
    with st.container(key="filterbar"):
        c1, c2, c3, c4, c5 = st.columns([2, 2.2, 2.4, 1.1, 2.6])
        # keep widget values in sync with S (S is the single source of truth across pages)
        st.session_state["w_region"] = S["region"]
        opts = dd.country_options(S["region"])
        ids = ["all"] + [i for i, _ in opts]
        if S["country"] not in ids:
            S["country"] = "all"
        st.session_state["w_country"] = S["country"]
        st.session_state["w_year"] = S["year"]
        c1.selectbox("Region", ["all"] + dd.REGIONS, key="w_region", on_change=_on_region,
                     format_func=lambda v: "All regions" if v == "all" else v)
        labels = dict(opts)
        c2.selectbox("Country", ids, key="w_country", on_change=_on_country,
                     format_func=lambda v: "All countries" if v == "all" else labels[v])
        c3.selectbox("Fiscal year", list(reversed(dd.FULL)), key="w_year", on_change=_on_year,
                     format_func=lambda y: f"FY{y} (Jul {y - 1} – Jun {y})")
        c4.button("RESET", on_click=_reset, key="w_reset")
        c5.markdown(f'<div class="showing">Showing <b>{dd.sel_name(sel)}</b> · FY{S["year"]}</div>',
                    unsafe_allow_html=True)
    return S, dd.cur_sel(S)


def page_header(hero: bool = False, title: str = ""):
    """Shared chrome for every page. Returns (state, selection)."""
    st.set_page_config(page_title="Pakistan Workers' Remittances – Gallup Pakistan", page_icon="★", layout="wide")
    inject_css()
    st.markdown(
        '<div class="topbar"><b>PKREM &lt;GO&gt;</b><span>Gallup Pakistan Digital Analytics</span>'
        '<span>Source: State Bank of Pakistan</span><span class="r">US$ million · Jul 1972 – Sep 2026</span></div>'
        '<div class="brand"><div class="mk"><span class="g1">GALLUP PAKISTAN</span><span class="g2">Digital Analytics</span></div>'
        '<span class="tag">Data journalism · Economy</span></div>',
        unsafe_allow_html=True)
    if hero:
        st.markdown(
            '<span class="sticker">COUNTRY &amp; REGION MONITOR</span>'
            '<div class="hero"><h1>Pakistan Workers’ Remittances – Country and Regional Monitor</h1>'
            '<p>Remittances received from July 1972 to September 2026, from the State Bank of Pakistan’s country-wise series. '
            'Filter by region or country, pick a fiscal year, and see each country’s share of its region.</p></div>',
            unsafe_allow_html=True)
    elif title:
        st.markdown(f'<span class="sticker">COUNTRY &amp; REGION MONITOR</span><div class="pagetitle">{title}</div>',
                    unsafe_allow_html=True)
    st.markdown(ticker_html(), unsafe_allow_html=True)
    return filter_bar()


def footer():
    st.markdown(
        '<div class="brandfoot"><b>GALLUP PAKISTAN</b><span>Analysis: <span class="a">Gallup Pakistan Digital Analytics team</span></span>'
        '<span>Data: State Bank of Pakistan, World Bank, IMF, Pakistan Economic Survey</span>'
        '<span class="r">Remittances in US$, fiscal years July–June</span></div>', unsafe_allow_html=True)
