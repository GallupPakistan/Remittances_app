"""Small Streamlit helpers shared by the pages."""
import streamlit as st

from . import data as dd
from .charts import FIG_CFG
from .style import set_year


def _plot(fig, key, **kw):
    try:  # newer Streamlit
        return st.plotly_chart(fig, width="stretch", config=FIG_CFG, key=key, **kw)
    except TypeError:  # older Streamlit
        return st.plotly_chart(fig, use_container_width=True, config=FIG_CFG, key=key, **kw)


def chart(fig, key, pick_year=False):
    """Render a Plotly figure; if pick_year, clicking a bar selects that fiscal year (like the HTML dashboard)."""
    if not pick_year:
        _plot(fig, key)
        return
    ev = _plot(fig, key, on_select="rerun", selection_mode="points")
    try:
        pts = ev.selection.points
    except Exception:
        pts = []
    for p in pts:
        if p.get("curve_number", 0) == 0 and p.get("x") in dd.FULL:
            if int(p["x"]) != st.session_state.S["year"]:
                set_year(int(p["x"]))
                st.rerun()
            break
