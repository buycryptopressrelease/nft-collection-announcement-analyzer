"""
nft_announcement_analyzer: NFT Collection Announcement Analyzer.

A free, dependency free tool that reads NFT collection details (supply, traits,
blockchain, mint schedule, utility and milestones) and generates announcement
angles, headline ideas, recommended press release topics and a press release
outline. It keeps confirmed facts, scheduled plans and project claims apart,
and never describes a planned milestone as completed.

Usage:
    python nft_announcement_analyzer.py data/nft_collections.json --id 1
    python nft_announcement_analyzer.py my_collection.json --format md
    python nft_announcement_analyzer.py my_collections.csv --format json
    python nft_announcement_analyzer.py data/nft_collections.json --list
    python nft_announcement_analyzer.py data/nft_collections.json --id 2 --today 2027-03-01

Built by BuyCryptoPressRelease.com (https://buycryptopressrelease.com/). MIT License.
"""

import csv
import datetime as _dt
import io
import json
import re
import sys

__version__ = "1.0.1"

WEBSITE = "https://buycryptopressrelease.com/"
NFT_PR_PAGE = "https://buycryptopressrelease.com/nft-project-pr/"
REPO = "https://github.com/buycryptopressrelease/nft-collection-announcement-analyzer"

REQUIRED = ["project_name", "blockchain", "total_supply"]
STATUSES = ["Completed", "Upcoming", "Planned"]
RISKY_WORDS = ["guaranteed", "guarantee", "profit", "profits", "returns", "roi", "investment",
               "passive income", "moon", "risk free", "riskfree", "100x", "10x", "price will"]
LIST_FIELDS = ["traits", "utility", "announcement_angles"]


# ---------------------------------------------------------------- helpers

def _num(value):
    """Parse 5000, "5,000" or "5000" into an int; None when missing."""
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value).replace(",", "").strip()
    try:
        return int(float(text))
    except ValueError:
        return None


def _date(value):
    text = str(value or "").strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return None
    try:
        return _dt.date.fromisoformat(text)
    except ValueError:
        return None


def _fmt_int(n):
    return f"{n:,}"


def _fmt_date(d):
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def _words(n):
    small = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
             "ten", "eleven", "twelve"]
    return small[n] if 0 <= n < len(small) else str(n)


def _title(text):
    return " ".join(w[:1].upper() + w[1:] for w in text.split(" "))


def _short(title):
    return title[:-13] if title.endswith(" Announcement") else title


def _risky(text):
    padded = " " + text.lower().replace(",", " ").replace(".", " ") + " "
    return [w for w in RISKY_WORDS if f" {w} " in padded]


def _as_list(value):
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return [v.strip() for v in str(value).split("|") if v.strip()]


def _norm_status(value):
    text = str(value or "").strip().lower()
    for s in STATUSES:
        if text == s.lower():
            return s
    return None


# ---------------------------------------------------------------- loading

def normalize(raw):
    """Clean one collection record into the analyzer's standard shape."""
    c = dict(raw)
    for key in LIST_FIELDS:
        c[key] = _as_list(c.get(key))
    ms = c.get("milestones") or []
    if isinstance(ms, str):
        parsed = []
        for part in ms.split("|"):
            bits = [b.strip() for b in part.split(":")]
            if bits and bits[0]:
                parsed.append({"title": bits[0], "status": bits[1] if len(bits) > 1 else "",
                               "date": bits[2] if len(bits) > 2 else ""})
        ms = parsed
    c["milestones"] = [{"title": str(m.get("title", "")).strip(), "status": str(m.get("status", "")).strip(),
                        "date": str(m.get("date", "")).strip()} for m in ms if str(m.get("title", "")).strip()]
    for key in ["project_name", "symbol", "website", "blockchain", "nft_standard", "collection_type",
                "marketplace", "mint_price", "mint_date", "reveal_date", "description"]:
        c[key] = str(c.get(key) or "").strip()
    return c


def load(path):
    """Load collections from a .json file (one record, a list, or {"collections": [...]}) or a .csv file."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return loads(text, "csv" if path.lower().endswith(".csv") else "json")


def loads(text, fmt="json"):
    if fmt == "csv":
        rows = list(csv.DictReader(io.StringIO(text)))
        return [normalize(r) for r in rows]
    data = json.loads(text)
    if isinstance(data, dict) and "collections" in data:
        data = data["collections"]
    if isinstance(data, dict):
        data = [data]
    return [normalize(r) for r in data]


# ---------------------------------------------------------------- analysis

def analyze(collection, today=None):
    """Analyze one collection. `today` (YYYY-MM-DD or date) fixes the reference date for scheduling."""
    c = normalize(collection)
    if today is None:
        today = _dt.date.today()
    elif not isinstance(today, _dt.date):
        today = _date(today) or _dt.date.today()
    name = c["project_name"] or "Unnamed collection"
    warnings = []

    for key in REQUIRED:
        if not c.get(key) and c.get(key) != 0:
            warnings.append(f"Missing required field: {key}.")

    # supply
    total = _num(c.get("total_supply"))
    minted = _num(c.get("minted_supply"))
    supply = {"total": total, "minted": minted, "remaining": None, "minted_percent": None, "status": "Unknown"}
    if total is not None and total <= 0:
        warnings.append("Total supply must be greater than zero.")
        total = None
        supply["total"] = None
    if minted is not None and minted < 0:
        warnings.append("Minted supply cannot be negative.")
        minted = None
        supply["minted"] = None
    if total is not None and minted is not None:
        if minted > total:
            warnings.append("Minted supply is higher than total supply. Check both numbers before publishing.")
        else:
            supply["remaining"] = total - minted
            supply["minted_percent"] = int(minted * 1000 / total + 0.5) / 10
            supply["status"] = "Not started" if minted == 0 else ("Fully minted" if minted == total else "Minting")

    # traits
    traits = c["traits"]
    declared = _num(c.get("trait_categories"))
    trait_count = len(traits) if traits else (declared or 0)
    if traits and declared is not None and declared != len(traits):
        warnings.append(f"Trait categories says {declared} but {len(traits)} trait names are listed.")

    # schedule
    mint = _date(c["mint_date"])
    reveal = _date(c["reveal_date"])
    if c["mint_date"] and not mint:
        warnings.append("Mint date is not a valid YYYY-MM-DD date.")
    if c["reveal_date"] and not reveal:
        warnings.append("Reveal date is not a valid YYYY-MM-DD date.")

    def when(d):
        if d is None:
            return None
        delta = (d - today).days
        return {"date": d.isoformat(), "days_from_today": delta,
                "status": "Today" if delta == 0 else ("Upcoming" if delta > 0 else "Past")}

    schedule = {"as_of": today.isoformat(), "mint": when(mint), "reveal": when(reveal), "days_mint_to_reveal": None}
    if mint and reveal:
        schedule["days_mint_to_reveal"] = (reveal - mint).days
        if reveal < mint:
            warnings.append("Reveal date is before the mint date.")
    if mint and mint > today and minted:
        warnings.append("Minted supply is above zero but the mint date is in the future. If this is a presale or allowlist mint, say so in the release; otherwise check the numbers.")
    if mint and mint < today and minted == 0:
        warnings.append("Mint date has passed but minted supply is 0. Update the minted supply or the mint date.")

    # milestones: status is taken exactly as given, never upgraded
    groups = {s: [] for s in STATUSES}
    for m in c["milestones"]:
        status = _norm_status(m["status"])
        if status is None:
            warnings.append(f"Milestone \"{m['title']}\" has no valid status (use Completed, Upcoming or Planned). It was treated as Planned.")
            status = "Planned"
        d = _date(m["date"])
        if status == "Completed" and d and d > today:
            warnings.append(f"Milestone \"{m['title']}\" is marked Completed but its date is in the future.")
        groups[status].append({"title": m["title"], "date": m["date"]})

    # claims check
    flagged = _risky(" ".join(c["utility"] + [c["description"]] + [m["title"] for m in c["milestones"]]))
    if flagged:
        warnings.append("Financial promise language found (" + ", ".join(flagged) + "). Remove it; most outlets reject guaranteed returns or profit claims.")

    report = {
        "tool": "NFT Collection Announcement Analyzer",
        "version": __version__,
        "project": {k: c[k] for k in ["project_name", "symbol", "website", "blockchain", "nft_standard",
                                      "collection_type", "marketplace", "mint_price"]},
        "supply": supply,
        "traits": {"count": trait_count, "names": traits},
        "schedule": schedule,
        "utility": c["utility"],
        "milestones": groups,
    }
    report["project"]["project_name"] = name
    report["angles"] = _angles(report)
    report["headlines"] = _headlines(report)
    report["topics"] = _topics(report)
    report["outline"] = _outline(report)
    report["facts"] = _facts(report)
    report["warnings"] = warnings
    report["distribution"] = {"label": "NFT Project PR", "url": NFT_PR_PAGE,
                              "note": "Explore NFT focused media distribution through BuyCryptoPressRelease.com."}
    return report


def _angles(r):
    p, s, sch = r["project"], r["supply"], r["schedule"]
    out = []
    mint_up = sch["mint"] and sch["mint"]["status"] in ("Upcoming", "Today")
    if s["status"] in ("Not started", "Unknown") and mint_up:
        out.append("Upcoming NFT collection launch")
    if mint_up:
        out.append("NFT mint schedule announcement")
    if s["status"] == "Minting":
        out.append("Mint progress update")
    if s["status"] == "Fully minted":
        out.append("Collection fully minted announcement")
    if sch["reveal"] and sch["reveal"]["status"] in ("Upcoming", "Today"):
        out.append("Collection reveal announcement")
    ctype = p["collection_type"].lower()
    if "gaming" in ctype or "game" in ctype:
        out.append("Blockchain gaming collection introduction")
    elif "art" in ctype:
        out.append(f"{p['collection_type']} collection introduction")
    elif p["collection_type"]:
        out.append(f"{p['collection_type']} collection introduction")
    if r["traits"]["count"]:
        out.append("Trait and artwork design reveal")
    if r["utility"]:
        out.append("Holder utility and community benefits")
    for m in r["milestones"]["Completed"]:
        out.append(f"Milestone achieved: {m['title']}")
    if r["milestones"]["Upcoming"] or r["milestones"]["Planned"]:
        out.append("Roadmap update")
    if p["blockchain"] and mint_up:
        out.append(f"Launch on {p['blockchain']}")
    seen, uniq = set(), []
    for a in out:
        if a not in seen:
            seen.add(a)
            uniq.append(a)
    return uniq


def _headlines(r):
    p, s, sch = r["project"], r["supply"], r["schedule"]
    name, chain = p["project_name"], p["blockchain"]
    ctype = p["collection_type"] or "NFT"
    kind = ctype if "nft" in ctype.lower() else f"{ctype} NFT"
    out = []
    size = f"{_fmt_int(s['total'])} Piece " if s["total"] else ""
    mint_up = sch["mint"] and sch["mint"]["status"] in ("Upcoming", "Today")
    if mint_up:
        on = f" on {chain}" if chain else ""
        if s["status"] in ("Not started", "Unknown"):
            out.append(f"{name} Announces Upcoming {size}{kind} Collection{on}")
            out.append(f"{name} Sets {_fmt_date(_date(sch['mint']['date']))} Mint Date for Its {ctype} Collection")
        else:
            out.append(f"{name} Sets {_fmt_date(_date(sch['mint']['date']))} Public Mint Date for Its {size}{kind} Collection{on}")
    if s["status"] == "Minting":
        out.append(f"{name} Reaches {_fmt_int(s['minted'])} Minted of {_fmt_int(s['total'])} NFTs")
    if s["status"] == "Fully minted":
        out.append(f"{name} Completes Mint of All {_fmt_int(s['total'])} NFTs")
    if mint_up and sch["reveal"] and sch["reveal"]["status"] in ("Upcoming", "Today"):
        out.append(f"{name} Shares NFT Mint and Collection Reveal Schedule")
    elif sch["reveal"] and sch["reveal"]["status"] in ("Upcoming", "Today"):
        out.append(f"{name} Schedules Collection Reveal for {_fmt_date(_date(sch['reveal']['date']))}")
    if r["traits"]["count"]:
        n = r["traits"]["count"]
        out.append(f"{name} Introduces {_words(n).capitalize()} Trait Categories for Its {ctype} Collection")
    for m in r["milestones"]["Completed"][:2]:
        out.append(f"{name} Announces {_short(m['title'])}")
    if r["milestones"]["Planned"]:
        out.append(f"{name} Shares Roadmap Including {r['milestones']['Planned'][0]['title']}")
    safe = [u for u in r["utility"] if not _risky(u)]
    if safe:
        out.append(f"{name} Outlines Holder Benefits Including {_title(safe[0])}")
    return out[:6]


def _topics(r):
    out = []
    sch, s = r["schedule"], r["supply"]
    if sch["mint"] and sch["mint"]["status"] in ("Upcoming", "Today"):
        out += ["NFT collection launch announcement", "Upcoming mint date announcement"]
    if s["status"] == "Minting":
        out.append("Mint progress and community update")
    if s["status"] == "Fully minted":
        out.append("Sold out collection announcement")
    if r["project"]["collection_type"]:
        out.append(f"{r['project']['collection_type']} project introduction")
    if r["utility"]:
        out.append("NFT utility and community announcement")
    if r["milestones"]["Completed"]:
        out.append("Milestone and partnership announcement")
    if r["milestones"]["Upcoming"] or r["milestones"]["Planned"]:
        out.append("Roadmap announcement")
    return out


def _outline(r):
    p, s, sch, t = r["project"], r["supply"], r["schedule"], r["traits"]
    name = p["project_name"]
    lines = []
    headline = r["headlines"][0] if r["headlines"] else f"{name} Announces NFT Collection"
    lines.append(("Headline", headline))
    sub = []
    if s["total"]:
        sub.append(f"{_fmt_int(s['total'])} NFT collection")
    if p["blockchain"]:
        sub.append(f"built on {p['blockchain']}" + (f" ({p['nft_standard']})" if p["nft_standard"] else ""))
    if p["marketplace"]:
        sub.append(f"listed on {p['marketplace']}")
    lines.append(("Subheadline", (name + ": " + ", ".join(sub)) if sub else name))
    lines.append(("Dateline", "[CITY], [DATE]"))
    intro = f"{name}"
    if p["symbol"]:
        intro += f" ({p['symbol']})"
    intro += f", a {p['collection_type'] or 'NFT'} collection" + (f" on {p['blockchain']}" if p["blockchain"] else "")
    if sch["mint"] and sch["mint"]["status"] in ("Upcoming", "Today"):
        intro += f", is scheduled to open its mint on {_fmt_date(_date(sch['mint']['date']))}."
    elif s["status"] == "Minting":
        intro += f", has minted {_fmt_int(s['minted'])} of {_fmt_int(s['total'])} NFTs."
    else:
        intro += ", today announced its collection."
    lines.append(("Opening paragraph", intro))
    det = []
    if s["total"]:
        det.append(f"Total supply: {_fmt_int(s['total'])}")
    if s["minted_percent"] is not None:
        det.append(f"Minted: {_fmt_int(s['minted'])} ({s['minted_percent']}%)")
    if p["mint_price"]:
        det.append(f"Mint price: {p['mint_price']}")
    if p["marketplace"]:
        det.append(f"Marketplace: {p['marketplace']}")
    lines.append(("Collection details", "; ".join(det) or "[Add supply, price and marketplace]"))
    if t["count"]:
        lines.append(("Art and traits", f"{t['count']} trait categories" + (": " + ", ".join(t["names"]) if t["names"] else "")))
    if sch["mint"] or sch["reveal"]:
        sched = []
        if sch["mint"]:
            sched.append(f"Mint: {_fmt_date(_date(sch['mint']['date']))}")
        if sch["reveal"]:
            sched.append(f"Reveal: {_fmt_date(_date(sch['reveal']['date']))}")
        lines.append(("Schedule", "; ".join(sched)))
    if r["utility"]:
        lines.append(("Utility (project stated)", "; ".join(r["utility"])))
    ms = r["milestones"]
    parts = []
    if ms["Completed"]:
        parts.append("Completed: " + "; ".join(m["title"] for m in ms["Completed"]))
    if ms["Upcoming"]:
        parts.append("Upcoming: " + "; ".join(m["title"] for m in ms["Upcoming"]))
    if ms["Planned"]:
        parts.append("Planned: " + "; ".join(m["title"] for m in ms["Planned"]))
    if parts:
        lines.append(("Roadmap", " | ".join(parts)))
    lines.append(("Quote", f"[Quote from the {name} founder or lead artist]"))
    lines.append(("About", f"About {name}: [two sentences]" + (f" Website: {p['website']}" if p["website"] else "")))
    lines.append(("Media contact", "[Name, email, website]"))
    lines.append(("Disclaimer", "NFTs are digital assets and carry risk. This announcement is for information only and is not financial advice."))
    return [{"section": k, "text": v} for k, v in lines]


def _facts(r):
    """Every statement the release relies on, labelled by how certain it is."""
    p, s, sch = r["project"], r["supply"], r["schedule"]
    out = []
    def add(label, kind):
        out.append({"statement": label, "type": kind})
    if s["total"]:
        add(f"Total supply is {_fmt_int(s['total'])}", "Project data")
    if s["minted"] is not None:
        add(f"{_fmt_int(s['minted'])} NFTs minted as of {sch['as_of']}", "Project data, verify on chain")
    if sch["mint"]:
        add(f"Mint date {sch['mint']['date']}", "Scheduled" if sch["mint"]["status"] != "Past" else "Past date, confirm it happened")
    if sch["reveal"]:
        add(f"Reveal date {sch['reveal']['date']}", "Scheduled" if sch["reveal"]["status"] != "Past" else "Past date, confirm it happened")
    for m in r["milestones"]["Completed"]:
        add(m["title"], "Completed, keep proof ready")
    for m in r["milestones"]["Upcoming"]:
        add(m["title"], "Upcoming, describe as scheduled")
    for m in r["milestones"]["Planned"]:
        add(m["title"], "Planned, describe as a plan")
    for u in r["utility"]:
        add(u, "Project claim")
    return out


# ---------------------------------------------------------------- output

def to_markdown(r):
    p, s, sch, t = r["project"], r["supply"], r["schedule"], r["traits"]
    L = [f"# NFT Analysis Report: {p['project_name']}", ""]
    meta = " · ".join(x for x in [p["blockchain"], p["nft_standard"], p["collection_type"]] if x)
    if meta:
        L += [meta, ""]
    L += [f"Report date: {sch['as_of']}", "", "## Key numbers", "", "| Metric | Value |", "|---|---|"]
    L.append(f"| Total supply | {_fmt_int(s['total']) if s['total'] is not None else 'n/a'} |")
    L.append(f"| Minted supply | {_fmt_int(s['minted']) if s['minted'] is not None else 'n/a'} |")
    L.append(f"| Remaining | {_fmt_int(s['remaining']) if s['remaining'] is not None else 'n/a'} |")
    L.append(f"| Minted percent | {str(s['minted_percent']) + '%' if s['minted_percent'] is not None else 'n/a'} |")
    L.append(f"| Supply status | {s['status']} |")
    L.append(f"| Trait categories | {t['count']} |")
    L.append(f"| Mint price | {p['mint_price'] or 'n/a'} |")
    for key, label in (("mint", "Mint date"), ("reveal", "Reveal date")):
        v = sch[key]
        L.append(f"| {label} | {v['date'] + ' (' + v['status'] + ')' if v else 'n/a'} |")
    L += ["", "## Suggested announcement angles", ""] + [f"{i}. {a}" for i, a in enumerate(r["angles"], 1)]
    L += ["", "## Headline ideas", ""] + [f"{i}. {h}" for i, h in enumerate(r["headlines"], 1)]
    L += ["", "## Recommended press release topics", ""] + [f"- {x}" for x in r["topics"]]
    L += ["", "## Milestones", ""]
    for st in STATUSES:
        items = r["milestones"][st]
        L.append(f"**{st}:** " + ("; ".join(f"{m['title']} ({m['date']})" if m["date"] else m["title"] for m in items) if items else "none"))
        L.append("")
    L += ["## Press release outline", ""] + [f"**{o['section']}:** {o['text']}" + "  " for o in r["outline"]]
    L += ["", "## Facts to check before publishing", "", "| Statement | Type |", "|---|---|"]
    L += [f"| {f['statement']} | {f['type']} |" for f in r["facts"]]
    L += ["", "## Warnings", ""] + ([f"- {w}" for w in r["warnings"]] or ["- None"])
    L += ["", "## Distribution resource", "", f"{r['distribution']['note']} [{r['distribution']['label']}]({r['distribution']['url']})", ""]
    return "\n".join(L)


def to_text(r):
    md = to_markdown(r)
    return md.replace("**", "").replace("# ", "").replace("#", "")


def render(r, fmt="md"):
    if fmt == "json":
        return json.dumps(r, indent=2, ensure_ascii=False) + "\n"
    if fmt == "txt":
        return to_text(r)
    return to_markdown(r)


USAGE = __doc__


def main(argv=None):
    args = sys.argv[1:] if argv is None else list(argv)
    if not args or args[0] in ("-h", "--help"):
        print(USAGE)
        return 0
    if args[0] == "--version":
        print(__version__)
        return 0
    path, rest = args[0], args[1:]
    fmt, pick, today, listing = "md", None, None, False
    i = 0
    while i < len(rest):
        a = rest[i]
        if a == "--format" and i + 1 < len(rest):
            fmt = rest[i + 1]; i += 2
        elif a == "--id" and i + 1 < len(rest):
            pick = rest[i + 1]; i += 2
        elif a == "--today" and i + 1 < len(rest):
            today = rest[i + 1]; i += 2
        elif a == "--list":
            listing = True; i += 1
        else:
            print(f"Unknown option: {a}")
            return 1
    if fmt not in ("md", "json", "txt"):
        print("Use --format md, json or txt")
        return 1
    try:
        cols = load(path)
    except (OSError, ValueError) as e:
        print(f"Could not read {path}: {e}")
        return 1
    if listing:
        for n, c in enumerate(cols, 1):
            print(f"{c.get('id') or n}. {c['project_name']} ({c['blockchain']})")
        return 0
    if pick is not None:
        cols = [c for n, c in enumerate(cols, 1) if str(c.get("id") or n) == str(pick)]
        if not cols:
            print(f"No collection with id {pick}. Try --list")
            return 1
    reports = [analyze(c, today) for c in cols]
    if fmt == "json":
        out = reports[0] if len(reports) == 1 else reports
        sys.stdout.write(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    else:
        sys.stdout.write("\n\n".join(render(r, fmt) for r in reports))
    return 0


if __name__ == "__main__":
    sys.exit(main())
