# Pakistan Workers' Remittances – Country & Regional Monitor (Streamlit)

Streamlit rebuild of the Gallup Pakistan HTML dashboard (State Bank of Pakistan data, Jul 1972 – Sep 2026).

## Run
```bash
pip install -r requirements.txt
streamlit run Overview.py
```

## Structure
```
Overview.py                      Home: running ticker, tiles, fiscal-year totals, share, GDP/PPP/exports
pages/1_Shocks_and_Monthly.py    Major shocks chart + event list, last 5 years monthly, regions in chosen year
pages/2_Eid_Effect.py            Eid & Ramadan on the monthly flow, Eid lift per event
pages/3_Regional_Mix.py          Regional mix over time, inside-region shares
pages/4_Regions_and_Countries.py Region/country table + About the data
core/data.py                     Data loading, aggregation (UAE / EU groups), selections
core/charts.py                   All Plotly figures and HTML fragments
core/style.py                    CSS, top bar, running ticker, shared filter bar
core/fmt.py, core/ui.py          Formatting helpers, chart wrapper
data/remittances_data.json       Dashboard data (country monthly + fiscal-year series, GDP/PPP/exports, Eid, shocks)
data/Homeremit_Arch_1.xlsx       Source workbook (reference)
```

Filters (Region / Country / Fiscal year / Reset) are shared across all pages.
Click a bar in the fiscal-year or shocks chart to choose that year.
