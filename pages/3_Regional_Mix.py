import streamlit as st

from core import charts as ch
from core import data as dd
from core.fmt import money
from core.style import card, card_title, footer, note, page_header
from core.ui import chart

S, sel = page_header(title="Regional mix over time")

with card("mix"):
    card_title("Regional mix over time")
    note("Fiscal-year totals by region, in billions of US dollars, from FY2011. Malaysia, South Africa and South Korea are only reported "
         "separately from FY2019 and sit in “Other &amp; unallocated” before that. From FY2020 the State Bank assigns remittances by the "
         "remitter’s original country, which moves money between regions (notably USA and Europe).")
    years = [y for y in dd.FULL if y >= 2011]
    sr = ch.mix_series(years)
    reg = dd.sel_region(sel)
    st.markdown(ch.legend_html(sr, reg), unsafe_allow_html=True)
    chart(ch.stacked_fig(years, sr, percent=False, hl=reg, mark=2020), "mix")

reg, reg_t, items, yrs, sr, hl = ch.inside_data(S, sel)
left, right = st.columns(2)
with left:
    with card("inside"):
        card_title(f"Inside {reg} – country share of the region, FY{S['year']}")
        pre = "" if dd.sel_region(sel) else f"No region is chosen, so this shows {reg}. "
        note(f"{pre}Each bar is the country’s part of {reg}’s total of {money(reg_t)}.")
        st.markdown(ch.hbars_html(items, S["country"]), unsafe_allow_html=True)
with right:
    with card("insidemix"):
        card_title(f"Country shares of {reg} over time")
        note("Each country’s share of its region’s total, by fiscal year from FY2011. Smaller countries are grouped as “Others in region”.")
        st.markdown(ch.legend_html(sr, hl), unsafe_allow_html=True)
        chart(ch.stacked_fig(yrs, sr, percent=True, hl=hl, mark=2020), "insidemix")
footer()
