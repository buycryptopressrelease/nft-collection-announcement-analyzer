"""Streamlit app for the NFT Collection Announcement Analyzer.

Run locally:
    pip install -r requirements.txt
    streamlit run app.py
"""
import datetime as dt
import json
import os

import streamlit as st

import nft_announcement_analyzer as nft

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLES = nft.load(os.path.join(HERE, "data", "nft_collections.json"))

st.set_page_config(page_title="NFT Collection Announcement Analyzer", page_icon="🖼️", layout="wide")
st.title("NFT Collection Announcement Analyzer")
st.caption("Turn NFT collection details into announcement angles, headline ideas and a press release outline. "
           "Free tool by [BuyCryptoPressRelease.com](https://buycryptopressrelease.com/).")

source = st.radio("Collection details", ["Use a sample", "Enter details", "Upload JSON or CSV"], horizontal=True)
collections = []

if source == "Use a sample":
    names = [c["project_name"] for c in SAMPLES]
    pick = st.selectbox("Sample collection (fictional demo data)", names)
    collections = [SAMPLES[names.index(pick)]]

elif source == "Enter details":
    with st.form("details"):
        a, b, c = st.columns(3)
        name = a.text_input("Project name", "MetaPixel Creatures")
        symbol = b.text_input("Collection symbol", "MPC")
        website = c.text_input("Project website", "https://metapixel.example")
        blockchain = a.text_input("Blockchain", "Ethereum")
        standard = b.text_input("NFT standard", "ERC-721")
        ctype = c.text_input("Collection type", "Generative Art")
        total = a.number_input("Total supply", min_value=0, value=5000, step=1)
        minted = b.number_input("Minted supply", min_value=0, value=0, step=1)
        price = c.text_input("Mint price", "0.05 ETH")
        marketplace = a.text_input("Marketplace", "OpenSea")
        mint_date = b.date_input("Mint date", dt.date.today() + dt.timedelta(days=30))
        reveal_date = c.date_input("Reveal date", dt.date.today() + dt.timedelta(days=35))
        traits = st.text_input("Trait categories (separate with |)", "Background|Body|Eyes|Headwear")
        utility = st.text_input("Utility (separate with |)", "Holder membership|Community access")
        milestones = st.text_area("Milestones, one per line as Title:Status:YYYY-MM-DD (Status is Completed, Upcoming or Planned)",
                                  "Collection Website Launch:Completed:" + dt.date.today().isoformat())
        description = st.text_input("Project description", "A generative art collection of digital creatures.")
        if st.form_submit_button("Analyze"):
            collections = [{
                "project_name": name, "symbol": symbol, "website": website, "blockchain": blockchain,
                "nft_standard": standard, "collection_type": ctype, "total_supply": int(total),
                "minted_supply": int(minted), "mint_price": price, "marketplace": marketplace,
                "mint_date": mint_date.isoformat(), "reveal_date": reveal_date.isoformat(),
                "traits": traits, "utility": utility, "description": description,
                "milestones": "|".join(line.strip() for line in milestones.splitlines() if line.strip()),
            }]

else:
    up = st.file_uploader("Upload a .json or .csv file (same fields as data/nft_collections.json)", type=["json", "csv"])
    if up is not None:
        try:
            collections = nft.loads(up.getvalue().decode("utf-8"), "csv" if up.name.lower().endswith(".csv") else "json")
        except ValueError as e:
            st.error(f"Could not read the file: {e}")
        if len(collections) > 1:
            names = [c["project_name"] or f"Row {i + 1}" for i, c in enumerate(collections)]
            pick = st.selectbox("Collection", names)
            collections = [collections[names.index(pick)]]

as_of = st.date_input("Report date (used to decide what is upcoming or past)", dt.date.today())

for col in collections:
    r = nft.analyze(col, as_of)
    p, s = r["project"], r["supply"]
    st.header(p["project_name"])
    st.caption(" · ".join(x for x in [p["blockchain"], p["nft_standard"], p["collection_type"]] if x))
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total supply", f"{s['total']:,}" if s["total"] is not None else "n/a")
    m2.metric("Minted", f"{s['minted']:,}" if s["minted"] is not None else "n/a",
              f"{s['minted_percent']}%" if s["minted_percent"] is not None else None)
    m3.metric("Remaining", f"{s['remaining']:,}" if s["remaining"] is not None else "n/a")
    m4.metric("Trait categories", r["traits"]["count"])
    m5.metric("Mint price", p["mint_price"] or "n/a")
    for w in r["warnings"]:
        st.warning(w)
    left, right = st.columns(2)
    with left:
        st.subheader("Announcement angles")
        st.markdown("\n".join(f"{i}. {a}" for i, a in enumerate(r["angles"], 1)))
        st.subheader("Headline ideas")
        st.markdown("\n".join(f"{i}. {h}" for i, h in enumerate(r["headlines"], 1)))
        st.subheader("Press release topics")
        st.markdown("\n".join(f"- {t}" for t in r["topics"]))
    with right:
        st.subheader("Press release outline")
        st.markdown("\n\n".join(f"**{o['section']}:** {o['text']}" for o in r["outline"]))
        st.subheader("Facts to check")
        st.table([{"Statement": f["statement"], "Type": f["type"]} for f in r["facts"]])
    st.info(f"{r['distribution']['note']} [{r['distribution']['label']}]({r['distribution']['url']})")
    slug = (p["project_name"] or "collection").lower().replace(" ", "_")
    d1, d2, d3 = st.columns(3)
    d1.download_button("Download JSON", nft.render(r, "json"), f"{slug}_analysis.json", "application/json")
    d2.download_button("Download Markdown", nft.render(r, "md"), f"{slug}_analysis.md", "text/markdown")
    d3.download_button("Download TXT", nft.render(r, "txt"), f"{slug}_analysis.txt", "text/plain")
