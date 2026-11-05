import streamlit as st

from core import charts as ch
from core import data as dd
from core.style import PAL, card, card_title, footer, note, page_header
from core.ui import chart

S, sel = page_header(title="Eid and remittances")
name = dd.sel_name(sel)
left, right = st.columns(2)

with left:
    with card("eid"):
        card_title(f"{name} – Eid and the monthly flow")
        note("Monthly remittances with each Eid marked: <b>F</b> for Eid al-Fitr and <b>A</b> for Eid al-Adha. Shaded bands are Ramadan. "
             "Eid dates are calculated from the Islamic calendar and can differ by a day from Pakistan’s moon-sighting decision.")
        yrs = st.columns([1, 2])[0].selectbox("Show", [5, 10, 20], index=1, format_func=lambda v: f"last {v} years", key="eid_range")
        st.markdown(ch.legend_html([{"name": "Eid al-Fitr", "color": ch.EIDCOL["fitr"]}, {"name": "Eid al-Adha", "color": ch.EIDCOL["adha"]},
                                    {"name": "Ramadan", "color": PAL[4]}]), unsafe_allow_html=True)
        chart(ch.eid_fig(sel, yrs), "eid")

with right:
    with card("eff"):
        card_title(f"{name} – how much Eid lifts remittances")
        note("For each Eid, the “run-up month” is the month that holds most of the 30 days before it. Each bar compares that month with "
             "the average of the months around it (six either side, leaving out other Eid months and run-up months).")
        frm = st.columns([1, 2])[0].selectbox("Events since", [2001, 2011, 2016], index=1, format_func=lambda v: f"FY{v}", key="eff_from")
        st.markdown(ch.legend_html([{"name": "Eid al-Fitr", "color": ch.EIDCOL["fitr"]}, {"name": "Eid al-Adha", "color": ch.EIDCOL["adha"]}]),
                    unsafe_allow_html=True)
        fig, summ = ch.eid_effect(sel, frm)
        if fig is None:
            note(summ)
        else:
            chart(fig, "eff")
            note(summ, "margin-top:10px")
footer()
