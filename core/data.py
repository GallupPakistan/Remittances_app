"""Data loading and aggregation (a direct port of the HTML dashboard's JS logic)."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import numpy as np
import streamlit as st

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "remittances_data.json"

REGIONS = ["Gulf (GCC)", "Europe", "North America", "Asia-Pacific", "Africa", "Other & unallocated"]

# Aggregates that appear in the country dropdown
AGG = {
    "uae_all": {"name": "UAE – all emirates", "region": "Gulf (GCC)",
                "members": ["dubai", "abudhabi", "sharjah", "uae_oth"]},
    "eu_all": {"name": "EU – all ten countries", "region": "Europe",
               "members": ["germany", "france", "nl", "spain", "italy", "greece",
                           "sweden", "denmark", "ireland", "belgium"]},
}


@st.cache_resource
def load():
    D = json.loads(DATA_FILE.read_text())
    for c in D["countries"]:
        c["fy"] = np.array(c["fy"], dtype=float)
        c["m"] = np.array(c["m"], dtype=float)
    return D


D = load()
C = D["countries"]
BY_ID = {c["id"]: c for c in C}
FY0 = D["fys"][0]
NFY = len(D["fys"])
NM = len(D["months"])
MONTHS = D["months"]
PARTIAL = {int(k): v for k, v in D["partial"].items()}
FULL = [y for y in D["fys"] if y not in PARTIAL]
LASTFULL = FULL[-1]


def yi(y: int) -> int:
    return y - FY0


# ---- selection / series -------------------------------------------------
# A selection is a tuple (type, id) with type in {"all","region","agg","country"}
ALL = ("all", "all")


def members(sel):
    t, i = sel
    if t == "all":
        return C
    if t == "region":
        return [c for c in C if c["region"] == i]
    if t == "agg":
        return [BY_ID[m] for m in AGG[i]["members"]]
    return [BY_ID[i]]


@lru_cache(maxsize=None)
def series(sel):
    ms = members(sel)
    fy = np.sum([c["fy"] for c in ms], axis=0)
    m = np.sum([c["m"] for c in ms], axis=0)
    return fy, m


def cur_sel(state) -> tuple:
    if state["country"] != "all":
        return ("agg" if state["country"] in AGG else "country", state["country"])
    if state["region"] != "all":
        return ("region", state["region"])
    return ALL


def sel_name(sel) -> str:
    t, i = sel
    if t == "all":
        return "All countries"
    if t == "region":
        return i
    if t == "agg":
        return AGG[i]["name"]
    return BY_ID[i]["name"]


def sel_region(sel):
    t, i = sel
    if t == "all":
        return None
    if t == "region":
        return i
    if t == "agg":
        return AGG[i]["region"]
    return BY_ID[i]["region"]


def region_of_country(cid: str) -> str:
    return AGG[cid]["region"] if cid in AGG else BY_ID[cid]["region"]


def country_options(region: str):
    """Ordered list of (id, label) for the country dropdown."""
    out = []
    for r in REGIONS:
        if region != "all" and r != region:
            continue
        for k, a in AGG.items():
            if a["region"] == r:
                out.append((k, a["name"]))
        for c in C:
            if c["region"] == r:
                out.append((c["id"], c["name"]))
    return out
