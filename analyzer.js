/**
 * nft-collection-announcement-analyzer
 * NFT Collection Announcement Analyzer: library and CLI.
 *
 * Reads NFT collection details (supply, traits, blockchain, mint schedule,
 * utility and milestones) and generates announcement angles, headline ideas,
 * press release topics and a press release outline. Confirmed facts, scheduled
 * plans and project claims are kept apart, and a planned milestone is never
 * described as completed.
 *
 *   nft-analyzer data/nft_collections.json --id 1
 *   nft-analyzer my_collection.json --format md
 *   nft-analyzer my_collections.csv --format json --today 2027-02-01
 *
 * Built by BuyCryptoPressRelease.com (https://buycryptopressrelease.com/). MIT License.
 */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.NFTAnalyzer = api;
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var VERSION = "1.0.1";
  var WEBSITE = "https://buycryptopressrelease.com/";
  var NFT_PR_PAGE = "https://buycryptopressrelease.com/nft-project-pr/";
  var REPO = "https://github.com/buycryptopressrelease/nft-collection-announcement-analyzer";
  var REQUIRED = ["project_name", "blockchain", "total_supply"];
  var STATUSES = ["Completed", "Upcoming", "Planned"];
  var RISKY_WORDS = ["guaranteed", "guarantee", "profit", "profits", "returns", "roi", "investment",
    "passive income", "moon", "risk free", "riskfree", "100x", "10x", "price will"];
  var LIST_FIELDS = ["traits", "utility", "announcement_angles"];
  var TEXT_FIELDS = ["project_name", "symbol", "website", "blockchain", "nft_standard", "collection_type",
    "marketplace", "mint_price", "mint_date", "reveal_date", "description"];
  var MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
    "October", "November", "December"];
  var SMALL = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve"];

  // ------------------------------------------------------------ helpers
  function str(v) { return v === null || v === undefined ? "" : String(v); }

  function num(value) {
    if (value === null || value === undefined || value === "" || typeof value === "boolean") return null;
    if (typeof value === "number") return isFinite(value) ? Math.trunc(value) : null;
    var text = String(value).split(",").join("").trim();
    if (text === "") return null;
    var n = Number(text);
    return isFinite(n) ? Math.trunc(n) : null;
  }

  function parseDate(value) {
    var text = str(value).trim();
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(text);
    if (!m) return null;
    var y = +m[1], mo = +m[2], d = +m[3];
    var t = Date.UTC(y, mo - 1, d);
    var dt = new Date(t);
    if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== mo - 1 || dt.getUTCDate() !== d) return null;
    return { y: y, m: mo, d: d, t: t, iso: text };
  }

  function todayDate() {
    var n = new Date();
    var p = function (x) { return (x < 10 ? "0" : "") + x; };
    return parseDate(n.getFullYear() + "-" + p(n.getMonth() + 1) + "-" + p(n.getDate()));
  }

  function days(a, b) { return Math.round((a.t - b.t) / 86400000); }
  function fmtInt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ","); }
  function fmtDate(d) { return MONTHS[d.m - 1] + " " + d.d + ", " + d.y; }
  function words(n) { return n >= 0 && n < SMALL.length ? SMALL[n] : String(n); }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function title(text) { return text.split(" ").map(function (w) { return w.slice(0, 1).toUpperCase() + w.slice(1); }).join(" "); }
  function shortTitle(t) { return /\sAnnouncement$/.test(t) && t.length >= 13 && t.slice(-13) === " Announcement" ? t.slice(0, -13) : t; }

  function risky(text) {
    var padded = " " + text.toLowerCase().split(",").join(" ").split(".").join(" ") + " ";
    return RISKY_WORDS.filter(function (w) { return padded.indexOf(" " + w + " ") !== -1; });
  }

  function asList(value) {
    if (value === null || value === undefined || value === "") return [];
    if (Array.isArray(value)) return value.map(function (v) { return str(v).trim(); }).filter(Boolean);
    return String(value).split("|").map(function (v) { return v.trim(); }).filter(Boolean);
  }

  function normStatus(value) {
    var text = str(value).trim().toLowerCase();
    for (var i = 0; i < STATUSES.length; i++) if (text === STATUSES[i].toLowerCase()) return STATUSES[i];
    return null;
  }

  // ------------------------------------------------------------ loading
  function normalize(raw) {
    var c = {};
    Object.keys(raw || {}).forEach(function (k) { c[k] = raw[k]; });
    LIST_FIELDS.forEach(function (k) { c[k] = asList(c[k]); });
    var ms = c.milestones || [];
    if (typeof ms === "string") {
      ms = ms.split("|").map(function (part) {
        var bits = part.split(":").map(function (b) { return b.trim(); });
        return { title: bits[0] || "", status: bits[1] || "", date: bits[2] || "" };
      }).filter(function (m) { return m.title; });
    }
    c.milestones = ms.map(function (m) {
      return { title: str(m.title).trim(), status: str(m.status).trim(), date: str(m.date).trim() };
    }).filter(function (m) { return m.title; });
    TEXT_FIELDS.forEach(function (k) { c[k] = str(c[k] || "").trim(); });
    return c;
  }

  function parseCsv(text) {
    var rows = [], row = [], field = "", q = false;
    for (var i = 0; i < text.length; i++) {
      var ch = text[i];
      if (q) {
        if (ch === '"') { if (text[i + 1] === '"') { field += '"'; i++; } else q = false; }
        else field += ch;
      } else if (ch === '"') q = true;
      else if (ch === ",") { row.push(field); field = ""; }
      else if (ch === "\n" || ch === "\r") {
        if (ch === "\r" && text[i + 1] === "\n") i++;
        row.push(field); field = ""; rows.push(row); row = [];
      } else field += ch;
    }
    if (field !== "" || row.length) { row.push(field); rows.push(row); }
    rows = rows.filter(function (r) { return r.some(function (x) { return x !== ""; }); });
    if (!rows.length) return [];
    var head = rows[0];
    return rows.slice(1).map(function (r) {
      var o = {};
      head.forEach(function (h, j) { o[h] = r[j] === undefined ? null : r[j]; });
      return o;
    });
  }

  function loads(text, fmt) {
    if (fmt === "csv") return parseCsv(text).map(normalize);
    var data = JSON.parse(text);
    if (data && !Array.isArray(data) && typeof data === "object" && "collections" in data) data = data.collections;
    if (!Array.isArray(data)) data = [data];
    return data.map(normalize);
  }

  // ------------------------------------------------------------ analysis
  function analyze(collection, today) {
    var c = normalize(collection);
    if (today === undefined || today === null) today = todayDate();
    else if (typeof today === "string") today = parseDate(today) || todayDate();
    var name = c.project_name || "Unnamed collection";
    var warnings = [];

    REQUIRED.forEach(function (key) {
      var v = c[key];
      if (!v && v !== 0) warnings.push("Missing required field: " + key + ".");
    });

    var total = num(c.total_supply), minted = num(c.minted_supply);
    var supply = { total: total, minted: minted, remaining: null, minted_percent: null, status: "Unknown" };
    if (total !== null && total <= 0) {
      warnings.push("Total supply must be greater than zero.");
      total = null; supply.total = null;
    }
    if (minted !== null && minted < 0) {
      warnings.push("Minted supply cannot be negative.");
      minted = null; supply.minted = null;
    }
    if (total !== null && minted !== null) {
      if (minted > total) warnings.push("Minted supply is higher than total supply. Check both numbers before publishing.");
      else {
        supply.remaining = total - minted;
        supply.minted_percent = Math.floor(minted * 1000 / total + 0.5) / 10;
        supply.status = minted === 0 ? "Not started" : (minted === total ? "Fully minted" : "Minting");
      }
    }

    var traits = c.traits;
    var declared = num(c.trait_categories);
    var traitCount = traits.length ? traits.length : (declared || 0);
    if (traits.length && declared !== null && declared !== traits.length)
      warnings.push("Trait categories says " + declared + " but " + traits.length + " trait names are listed.");

    var mint = parseDate(c.mint_date), reveal = parseDate(c.reveal_date);
    if (c.mint_date && !mint) warnings.push("Mint date is not a valid YYYY-MM-DD date.");
    if (c.reveal_date && !reveal) warnings.push("Reveal date is not a valid YYYY-MM-DD date.");

    function when(d) {
      if (!d) return null;
      var delta = days(d, today);
      return { date: d.iso, days_from_today: delta, status: delta === 0 ? "Today" : (delta > 0 ? "Upcoming" : "Past") };
    }
    var schedule = { as_of: today.iso, mint: when(mint), reveal: when(reveal), days_mint_to_reveal: null };
    if (mint && reveal) {
      schedule.days_mint_to_reveal = days(reveal, mint);
      if (reveal.t < mint.t) warnings.push("Reveal date is before the mint date.");
    }
    if (mint && mint.t > today.t && minted)
      warnings.push("Minted supply is above zero but the mint date is in the future. If this is a presale or allowlist mint, say so in the release; otherwise check the numbers.");
    if (mint && mint.t < today.t && minted === 0)
      warnings.push("Mint date has passed but minted supply is 0. Update the minted supply or the mint date.");

    var groups = { Completed: [], Upcoming: [], Planned: [] };
    c.milestones.forEach(function (m) {
      var status = normStatus(m.status);
      if (status === null) {
        warnings.push("Milestone \"" + m.title + "\" has no valid status (use Completed, Upcoming or Planned). It was treated as Planned.");
        status = "Planned";
      }
      var d = parseDate(m.date);
      if (status === "Completed" && d && d.t > today.t)
        warnings.push("Milestone \"" + m.title + "\" is marked Completed but its date is in the future.");
      groups[status].push({ title: m.title, date: m.date });
    });

    var flagged = risky(c.utility.concat([c.description]).concat(c.milestones.map(function (m) { return m.title; })).join(" "));
    if (flagged.length)
      warnings.push("Financial promise language found (" + flagged.join(", ") + "). Remove it; most outlets reject guaranteed returns or profit claims.");

    var report = {
      tool: "NFT Collection Announcement Analyzer",
      version: VERSION,
      project: {
        project_name: name, symbol: c.symbol, website: c.website, blockchain: c.blockchain,
        nft_standard: c.nft_standard, collection_type: c.collection_type, marketplace: c.marketplace, mint_price: c.mint_price
      },
      supply: supply,
      traits: { count: traitCount, names: traits },
      schedule: schedule,
      utility: c.utility,
      milestones: groups
    };
    report.angles = angles(report);
    report.headlines = headlines(report);
    report.topics = topics(report);
    report.outline = outline(report);
    report.facts = facts(report);
    report.warnings = warnings;
    report.distribution = { label: "NFT Project PR", url: NFT_PR_PAGE,
      note: "Explore NFT focused media distribution through BuyCryptoPressRelease.com." };
    return report;
  }

  function upcoming(w) { return !!(w && (w.status === "Upcoming" || w.status === "Today")); }

  function angles(r) {
    var p = r.project, s = r.supply, sch = r.schedule, out = [];
    var mintUp = upcoming(sch.mint);
    if ((s.status === "Not started" || s.status === "Unknown") && mintUp) out.push("Upcoming NFT collection launch");
    if (mintUp) out.push("NFT mint schedule announcement");
    if (s.status === "Minting") out.push("Mint progress update");
    if (s.status === "Fully minted") out.push("Collection fully minted announcement");
    if (upcoming(sch.reveal)) out.push("Collection reveal announcement");
    var ctype = p.collection_type.toLowerCase();
    if (ctype.indexOf("gaming") !== -1 || ctype.indexOf("game") !== -1) out.push("Blockchain gaming collection introduction");
    else if (p.collection_type) out.push(p.collection_type + " collection introduction");
    if (r.traits.count) out.push("Trait and artwork design reveal");
    if (r.utility.length) out.push("Holder utility and community benefits");
    r.milestones.Completed.forEach(function (m) { out.push("Milestone achieved: " + m.title); });
    if (r.milestones.Upcoming.length || r.milestones.Planned.length) out.push("Roadmap update");
    if (p.blockchain && mintUp) out.push("Launch on " + p.blockchain);
    return out.filter(function (a, i) { return out.indexOf(a) === i; });
  }

  function headlines(r) {
    var p = r.project, s = r.supply, sch = r.schedule;
    var name = p.project_name, chain = p.blockchain;
    var ctype = p.collection_type || "NFT";
    var kind = ctype.toLowerCase().indexOf("nft") !== -1 ? ctype : ctype + " NFT";
    var out = [];
    var size = s.total ? fmtInt(s.total) + " Piece " : "";
    var mintUp = upcoming(sch.mint);
    if (mintUp) {
      var on = chain ? " on " + chain : "";
      if (s.status === "Not started" || s.status === "Unknown") {
        out.push(name + " Announces Upcoming " + size + kind + " Collection" + on);
        out.push(name + " Sets " + fmtDate(parseDate(sch.mint.date)) + " Mint Date for Its " + ctype + " Collection");
      } else {
        out.push(name + " Sets " + fmtDate(parseDate(sch.mint.date)) + " Public Mint Date for Its " + size + kind + " Collection" + on);
      }
    }
    if (s.status === "Minting") out.push(name + " Reaches " + fmtInt(s.minted) + " Minted of " + fmtInt(s.total) + " NFTs");
    if (s.status === "Fully minted") out.push(name + " Completes Mint of All " + fmtInt(s.total) + " NFTs");
    if (mintUp && upcoming(sch.reveal)) out.push(name + " Shares NFT Mint and Collection Reveal Schedule");
    else if (upcoming(sch.reveal)) out.push(name + " Schedules Collection Reveal for " + fmtDate(parseDate(sch.reveal.date)));
    if (r.traits.count) out.push(name + " Introduces " + cap(words(r.traits.count)) + " Trait Categories for Its " + ctype + " Collection");
    r.milestones.Completed.slice(0, 2).forEach(function (m) { out.push(name + " Announces " + shortTitle(m.title)); });
    if (r.milestones.Planned.length) out.push(name + " Shares Roadmap Including " + r.milestones.Planned[0].title);
    var safe = r.utility.filter(function (u) { return !risky(u).length; });
    if (safe.length) out.push(name + " Outlines Holder Benefits Including " + title(safe[0]));
    return out.slice(0, 6);
  }

  function topics(r) {
    var out = [], sch = r.schedule, s = r.supply;
    if (upcoming(sch.mint)) out.push("NFT collection launch announcement", "Upcoming mint date announcement");
    if (s.status === "Minting") out.push("Mint progress and community update");
    if (s.status === "Fully minted") out.push("Sold out collection announcement");
    if (r.project.collection_type) out.push(r.project.collection_type + " project introduction");
    if (r.utility.length) out.push("NFT utility and community announcement");
    if (r.milestones.Completed.length) out.push("Milestone and partnership announcement");
    if (r.milestones.Upcoming.length || r.milestones.Planned.length) out.push("Roadmap announcement");
    return out;
  }

  function outline(r) {
    var p = r.project, s = r.supply, sch = r.schedule, t = r.traits, name = p.project_name, L = [];
    L.push(["Headline", r.headlines.length ? r.headlines[0] : name + " Announces NFT Collection"]);
    var sub = [];
    if (s.total) sub.push(fmtInt(s.total) + " NFT collection");
    if (p.blockchain) sub.push("built on " + p.blockchain + (p.nft_standard ? " (" + p.nft_standard + ")" : ""));
    if (p.marketplace) sub.push("listed on " + p.marketplace);
    L.push(["Subheadline", sub.length ? name + ": " + sub.join(", ") : name]);
    L.push(["Dateline", "[CITY], [DATE]"]);
    var intro = name + (p.symbol ? " (" + p.symbol + ")" : "");
    intro += ", a " + (p.collection_type || "NFT") + " collection" + (p.blockchain ? " on " + p.blockchain : "");
    if (upcoming(sch.mint)) intro += ", is scheduled to open its mint on " + fmtDate(parseDate(sch.mint.date)) + ".";
    else if (s.status === "Minting") intro += ", has minted " + fmtInt(s.minted) + " of " + fmtInt(s.total) + " NFTs.";
    else intro += ", today announced its collection.";
    L.push(["Opening paragraph", intro]);
    var det = [];
    if (s.total) det.push("Total supply: " + fmtInt(s.total));
    if (s.minted_percent !== null) det.push("Minted: " + fmtInt(s.minted) + " (" + pyNum(s.minted_percent) + "%)");
    if (p.mint_price) det.push("Mint price: " + p.mint_price);
    if (p.marketplace) det.push("Marketplace: " + p.marketplace);
    L.push(["Collection details", det.join("; ") || "[Add supply, price and marketplace]"]);
    if (t.count) L.push(["Art and traits", t.count + " trait categories" + (t.names.length ? ": " + t.names.join(", ") : "")]);
    if (sch.mint || sch.reveal) {
      var sc = [];
      if (sch.mint) sc.push("Mint: " + fmtDate(parseDate(sch.mint.date)));
      if (sch.reveal) sc.push("Reveal: " + fmtDate(parseDate(sch.reveal.date)));
      L.push(["Schedule", sc.join("; ")]);
    }
    if (r.utility.length) L.push(["Utility (project stated)", r.utility.join("; ")]);
    var ms = r.milestones, parts = [];
    var titles = function (a) { return a.map(function (m) { return m.title; }).join("; "); };
    if (ms.Completed.length) parts.push("Completed: " + titles(ms.Completed));
    if (ms.Upcoming.length) parts.push("Upcoming: " + titles(ms.Upcoming));
    if (ms.Planned.length) parts.push("Planned: " + titles(ms.Planned));
    if (parts.length) L.push(["Roadmap", parts.join(" | ")]);
    L.push(["Quote", "[Quote from the " + name + " founder or lead artist]"]);
    L.push(["About", "About " + name + ": [two sentences]" + (p.website ? " Website: " + p.website : "")]);
    L.push(["Media contact", "[Name, email, website]"]);
    L.push(["Disclaimer", "NFTs are digital assets and carry risk. This announcement is for information only and is not financial advice."]);
    return L.map(function (x) { return { section: x[0], text: x[1] }; });
  }

  function facts(r) {
    var p = r.project, s = r.supply, sch = r.schedule, out = [];
    function add(statement, type) { out.push({ statement: statement, type: type }); }
    if (s.total) add("Total supply is " + fmtInt(s.total), "Project data");
    if (s.minted !== null) add(fmtInt(s.minted) + " NFTs minted as of " + sch.as_of, "Project data, verify on chain");
    if (sch.mint) add("Mint date " + sch.mint.date, sch.mint.status !== "Past" ? "Scheduled" : "Past date, confirm it happened");
    if (sch.reveal) add("Reveal date " + sch.reveal.date, sch.reveal.status !== "Past" ? "Scheduled" : "Past date, confirm it happened");
    r.milestones.Completed.forEach(function (m) { add(m.title, "Completed, keep proof ready"); });
    r.milestones.Upcoming.forEach(function (m) { add(m.title, "Upcoming, describe as scheduled"); });
    r.milestones.Planned.forEach(function (m) { add(m.title, "Planned, describe as a plan"); });
    r.utility.forEach(function (u) { add(u, "Project claim"); });
    return out;
  }

  // Python prints floats like 24.0; match that in text output
  function pyNum(x) { return Number.isInteger(x) ? x.toFixed(1) : String(x); }

  // ------------------------------------------------------------ output
  function toMarkdown(r) {
    var p = r.project, s = r.supply, sch = r.schedule, t = r.traits;
    var na = function (v, f) { return v === null || v === undefined ? "n/a" : f(v); };
    var L = ["# NFT Analysis Report: " + p.project_name, ""];
    var meta = [p.blockchain, p.nft_standard, p.collection_type].filter(Boolean).join(" · ");
    if (meta) L.push(meta, "");
    L.push("Report date: " + sch.as_of, "", "## Key numbers", "", "| Metric | Value |", "|---|---|");
    L.push("| Total supply | " + na(s.total, fmtInt) + " |");
    L.push("| Minted supply | " + na(s.minted, fmtInt) + " |");
    L.push("| Remaining | " + na(s.remaining, fmtInt) + " |");
    L.push("| Minted percent | " + na(s.minted_percent, function (v) { return pyNum(v) + "%"; }) + " |");
    L.push("| Supply status | " + s.status + " |");
    L.push("| Trait categories | " + t.count + " |");
    L.push("| Mint price | " + (p.mint_price || "n/a") + " |");
    [["mint", "Mint date"], ["reveal", "Reveal date"]].forEach(function (kv) {
      var v = sch[kv[0]];
      L.push("| " + kv[1] + " | " + (v ? v.date + " (" + v.status + ")" : "n/a") + " |");
    });
    L.push("", "## Suggested announcement angles", "");
    r.angles.forEach(function (a, i) { L.push((i + 1) + ". " + a); });
    L.push("", "## Headline ideas", "");
    r.headlines.forEach(function (h, i) { L.push((i + 1) + ". " + h); });
    L.push("", "## Recommended press release topics", "");
    r.topics.forEach(function (x) { L.push("- " + x); });
    L.push("", "## Milestones", "");
    STATUSES.forEach(function (st) {
      var items = r.milestones[st];
      L.push("**" + st + ":** " + (items.length ? items.map(function (m) { return m.date ? m.title + " (" + m.date + ")" : m.title; }).join("; ") : "none"));
      L.push("");
    });
    L.push("## Press release outline", "");
    r.outline.forEach(function (o) { L.push("**" + o.section + ":** " + o.text + "  "); });
    L.push("", "## Facts to check before publishing", "", "| Statement | Type |", "|---|---|");
    r.facts.forEach(function (f) { L.push("| " + f.statement + " | " + f.type + " |"); });
    L.push("", "## Warnings", "");
    if (r.warnings.length) r.warnings.forEach(function (w) { L.push("- " + w); }); else L.push("- None");
    L.push("", "## Distribution resource", "", r.distribution.note + " [" + r.distribution.label + "](" + r.distribution.url + ")", "");
    return L.join("\n");
  }

  function toText(r) { return toMarkdown(r).split("**").join("").split("# ").join("").split("#").join(""); }

  function render(r, fmt) {
    if (fmt === "json") return JSON.stringify(r, null, 2) + "\n";
    if (fmt === "txt") return toText(r);
    return toMarkdown(r);
  }

  var USAGE = "NFT Collection Announcement Analyzer v" + VERSION + "\n\nUsage:\n" +
    "  nft-analyzer data/nft_collections.json --id 1\n" +
    "  nft-analyzer my_collection.json --format md\n" +
    "  nft-analyzer my_collections.csv --format json\n" +
    "  nft-analyzer data/nft_collections.json --list\n" +
    "  nft-analyzer data/nft_collections.json --id 2 --today 2027-03-01\n" +
    "  nft-analyzer --version";

  function main(argv) {
    var fs = require("fs");
    var args = argv.slice();
    var out = function (s) { process.stdout.write(s); };
    if (!args.length || args[0] === "-h" || args[0] === "--help") { console.log(USAGE); return 0; }
    if (args[0] === "--version") { console.log(VERSION); return 0; }
    var path = args[0], rest = args.slice(1), fmt = "md", pick = null, today = null, listing = false;
    for (var i = 0; i < rest.length;) {
      var a = rest[i];
      if (a === "--format" && i + 1 < rest.length) { fmt = rest[i + 1]; i += 2; }
      else if (a === "--id" && i + 1 < rest.length) { pick = rest[i + 1]; i += 2; }
      else if (a === "--today" && i + 1 < rest.length) { today = rest[i + 1]; i += 2; }
      else if (a === "--list") { listing = true; i += 1; }
      else { console.log("Unknown option: " + a); return 1; }
    }
    if (["md", "json", "txt"].indexOf(fmt) === -1) { console.log("Use --format md, json or txt"); return 1; }
    var cols;
    try { cols = loads(fs.readFileSync(path, "utf8"), /\.csv$/i.test(path) ? "csv" : "json"); }
    catch (e) { console.log("Could not read " + path + ": " + e.message); return 1; }
    if (listing) {
      cols.forEach(function (c, n) { console.log(((c.id || n + 1)) + ". " + c.project_name + " (" + c.blockchain + ")"); });
      return 0;
    }
    if (pick !== null) {
      cols = cols.filter(function (c, n) { return String(c.id || n + 1) === String(pick); });
      if (!cols.length) { console.log("No collection with id " + pick + ". Try --list"); return 1; }
    }
    var reports = cols.map(function (c) { return analyze(c, today); });
    if (fmt === "json") out(JSON.stringify(reports.length === 1 ? reports[0] : reports, null, 2) + "\n");
    else out(reports.map(function (r) { return render(r, fmt); }).join("\n\n"));
    return 0;
  }

  return {
    VERSION: VERSION, WEBSITE: WEBSITE, NFT_PR_PAGE: NFT_PR_PAGE, REPO: REPO,
    analyze: analyze, loads: loads, normalize: normalize, render: render,
    toMarkdown: toMarkdown, toText: toText, main: main
  };
});
