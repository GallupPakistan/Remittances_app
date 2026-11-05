import streamlit as st

from core import charts as ch
from core import data as dd
from core.style import card, card_title, footer, note, page_header
from core.ui import chart

S, sel = page_header(title="Major shocks and the monthly flow")
name = dd.sel_name(sel)

with card("shocks"):
    card_title(f"{name} – major shocks and the remittance flow")
    note("Numbered markers show events that hit Pakistan’s economy or the Gulf economies where most migrant workers earn. "
         "Hover a marker or a list item for details. Switch between the amount and the growth on the year before.")
    mode = st.radio("Chart type", ["Amount", "Growth on year before"], horizontal=True, label_visibility="collapsed", key="shock_mode")
    chart(ch.shocks_fig(S, sel, "level" if mode == "Amount" else "growth"), "shocks", pick_year=True)
    st.markdown(ch.events_html(), unsafe_allow_html=True)

left, right = st.columns(2)
with left:
    with card("monthly"):
        card_title(f"{name} – last five years, by month")
        note("US dollars received each month. The peak month is marked.")
        chart(ch.monthly_fig(sel), "monthly")
with right:
    with card("regions"):
        card_title("Regions in the chosen year")
        note("Each region’s amount and share of all remittances.")
        st.markdown(ch.region_bars_html(S, sel), unsafe_allow_html=True)
footer()
