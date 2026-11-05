"""Overview page – entry point.  Run with:  streamlit run app.py"""
import streamlit as st

from core import charts as ch
from core import data as dd
from core.style import card, card_title, footer, note, page_header
from core.ui import chart

S, sel = page_header(hero=True)
name = dd.sel_name(sel)

st.markdown(ch.tiles_html(S, sel), unsafe_allow_html=True)

# ---- fiscal-year totals
with card("annual"):
    card_title(f"{name} – fiscal-year totals")
    note("US dollars received in each fiscal year (July to June). Click a bar to choose that year. The chosen year is highlighted.")
    chart(ch.annual_fig(S, sel), "annual", pick_year=True)

# ---- share of all remittances (country only)
if sel[0] in ("country", "agg"):
    with card("share"):
        card_title(f"{name} – share of all remittances, by fiscal year")
        note("The chosen country’s part of all remittances received in each fiscal year. Periods before a country was reported "
             "separately show as zero, because its money was counted in “All other countries”.")
        chart(ch.share_fig(S, sel), "share")

# ---- economy comparison
with card("macro"):
    card_title(f"{name} – remittances compared with the size of the economy")
    note("Remittances divided by GDP, by GDP adjusted for purchasing power (PPP), and by exports of goods and services, for each "
         "fiscal year. Dashed segments use newer or provisional figures (see the notes under the charts). Hover for the values.")
    cols = st.columns(3)
    spec = [("As % of GDP", "gdp", 2025), ("As % of GDP at PPP", "ppp", 2024), ("As % of exports of goods and services", "exp", 2026)]
    for col, (title, key, solid_end) in zip(cols, spec):
        fig, big = ch.macro_fig(S, sel, key, solid_end)
        with col:
            st.markdown(f'<p class="macro-h">{title}</p><div class="macro-big">{big}</div>', unsafe_allow_html=True)
            chart(fig, f"macro_{key}")
    note("GDP in current US dollars: World Bank to FY2025; FY2026 is the Economic Survey 2025-26 figure ($452.1bn), which is provisional "
         "and from a different source, so the last step is not strictly comparable. GDP at PPP (current international dollars): World Bank "
         "to FY2024, then IMF projections for FY2025 and FY2026. Exports of goods and services (balance-of-payments basis): IMF/World Bank "
         "to FY2021 and for FY2024, World Bank via The Global Economy for FY2022 and FY2023, State Bank of Pakistan for FY2025 and FY2026. "
         "PPP starts in FY1980 and exports in FY1976. The very early GDP figures in US dollars are affected by the 1972 devaluation.",
         "margin-top:12px")
footer()
