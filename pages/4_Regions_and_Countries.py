import streamlit as st

from core import charts as ch
from core import data as dd
from core.style import card, card_title, footer, note, page_header

S, sel = page_header(title="Regions and countries")

with card("table"):
    card_title(f"Regions and countries, FY{S['year']}")
    note("Amounts in millions of US dollars. “Share of region” is the country’s part of its region’s total; “Share of total” is its part "
         "of all remittances. Countries with no remittances in both the chosen year and the year before are hidden.")
    st.markdown(ch.table_html(S, sel), unsafe_allow_html=True)

with card("about"):
    card_title("About the data")
    st.markdown(
        '<ul class="about">'
        '<li>Source: State Bank of Pakistan, country-wise workers’ remittances. Fiscal years run July to June. FY2027 has July to September only, so it is left out of the year list.</li>'
        '<li>Regions are the Gallup Pakistan Digital Analytics team’s grouping: Gulf (Saudi Arabia, the four UAE lines, Bahrain, Kuwait, Qatar, Oman); Europe (United Kingdom, ten EU countries, Norway, Switzerland); North America (USA, Canada); Asia-Pacific (Australia, Japan, Malaysia, South Korea); Africa (South Africa); and “Other &amp; unallocated”.</li>'
        '<li>Countries the State Bank did not report separately in a given period appear as zero and are counted in “All other countries”. That group also holds the small encashment line for certificates (FEBCs and FCBCs).</li>'
        '<li>From July 2019 the State Bank assigns remittances by the remitter’s original country, so USA falls and EU countries rise around FY2020. Roshan Digital Account conversions are included from September 2020. The last August figure is marked revised in the source.</li>'
        '<li>Two extra columns at the end of the last sheet (labelled Aug-27 and Aug-28) repeat other months’ totals and are excluded. Every country and region reconciles to the State Bank’s total for every month.</li>'
        '</ul>', unsafe_allow_html=True)
footer()
