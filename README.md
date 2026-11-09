# NFT Collection Announcement Analyzer 🖼️📣

[![Online tool](https://img.shields.io/badge/try%20it-online-8b5cf6?style=flat-square&labelColor=111827)](https://buycryptopressrelease.github.io/nft-collection-announcement-analyzer/)
[![npm](https://img.shields.io/npm/v/nft-collection-announcement-analyzer?style=flat-square&color=8b5cf6&labelColor=111827)](https://www.npmjs.com/package/nft-collection-announcement-analyzer)
[![PyPI](https://img.shields.io/pypi/v/nft-collection-announcement-analyzer?style=flat-square&color=8b5cf6&labelColor=111827)](https://pypi.org/project/nft-collection-announcement-analyzer/)
[![Docs](https://img.shields.io/badge/docs-readthedocs-8b5cf6?style=flat-square&labelColor=111827)](https://nft-collection-announcement-analyzer.readthedocs.io)
[![License](https://img.shields.io/badge/license-MIT-8A8A8A?style=flat-square&labelColor=111827)](LICENSE)

The NFT Collection Announcement Analyzer is a free tool that reads NFT collection details (supply, traits, blockchain, mint schedule, utility and milestones) and turns them into announcement angles, headline ideas, press release topics and a ready to fill press release outline. It is built for NFT founders, artists, Web3 startups, blockchain gaming studios and NFT marketing agencies. Built by [BuyCryptoPressRelease.com](https://buycryptopressrelease.com/).

**Try it in your browser:** [https://buycryptopressrelease.github.io/nft-collection-announcement-analyzer/](https://buycryptopressrelease.github.io/nft-collection-announcement-analyzer/) (nothing you type leaves your browser)

## Why it exists

NFT teams often have the facts but not the story. This tool organizes the facts and suggests what is newsworthy, while staying honest:

- Confirmed facts, scheduled plans and project claims are kept apart
- A planned milestone is never described as completed
- Supply and trait counts are never treated as proof of demand
- Financial promise words (guaranteed, profit, returns, 100x) are flagged so the release does not get rejected

## How It Works

1. Enter the collection details, upload a JSON or CSV file, or pick a sample.
2. The analyzer checks the data: supply math, valid dates, reveal after mint, trait counts, milestone status.
3. It works out what is upcoming or past from the report date.
4. It suggests announcement angles, headline ideas and press release topics that match the real status.
5. It builds a press release outline and a fact check list, and exports everything as Markdown, JSON or TXT.

## Features

| Feature | What it does |
|---|---|
| Collection Analyzer | Reads and cleans the collection record |
| Supply Analyzer | Calculates minted, remaining and percent minted |
| Trait Analyzer | Counts trait categories and checks them against the declared number |
| Mint Schedule Analyzer | Works out days to mint and reveal, and flags dates in the wrong order |
| Milestone Analyzer | Separates completed, upcoming and planned milestones exactly as given |
| Headline Generator | Suggests up to six headlines that match the real status |
| PR Angle Generator | Finds media announcement angles |
| Press Release Outline | Builds a structured outline with disclaimer and placeholders |
| Fact Check List | Labels every statement as data, scheduled, planned or project claim |
| Claim Checker | Flags financial promise words such as guaranteed, profit or returns |
| Export Report | Markdown, JSON or TXT |

## Quick Start

### In the browser
Open [https://buycryptopressrelease.github.io/nft-collection-announcement-analyzer/](https://buycryptopressrelease.github.io/nft-collection-announcement-analyzer/), load a sample or type your details, and press **Analyze**.

### Python
```bash
pip install nft-collection-announcement-analyzer
nft-analyzer my_collection.json
nft-analyzer my_collections.csv --format json
nft-analyzer my_collection.json --today 2027-02-01 --format txt
```

### Node.js
```bash
npm install -g nft-collection-announcement-analyzer
nft-analyzer my_collection.json --format md
```

### Streamlit app
```bash
git clone https://github.com/buycryptopressrelease/nft-collection-announcement-analyzer.git
cd nft-collection-announcement-analyzer
pip install -r requirements.txt
streamlit run app.py
```

### In code
```python
import nft_announcement_analyzer as nft

collections = nft.load("data/nft_collections.json")
report = nft.analyze(collections[0], today="2027-02-01")
print(report["headlines"])
print(nft.render(report, "md"))
```

```javascript
const nft = require("nft-collection-announcement-analyzer");
const fs = require("fs");

const [collection] = nft.loads(fs.readFileSync("data/nft_collections.json", "utf8"));
const report = nft.analyze(collection, "2027-02-01");
console.log(report.headlines);
```

## Commands and Options

| Command / option | What it does |
|---|---|
| `nft-analyzer FILE` | Analyze every collection in a JSON or CSV file |
| `--id N` | Analyze only collection N |
| `--list` | List the collections in the file |
| `--format md\|json\|txt` | Output format (default md) |
| `--today YYYY-MM-DD` | Report date used to decide what is upcoming or past |
| `--version` | Show the version |

## Input Fields

| Field | Description | Example |
|---|---|---|
| `project_name` | NFT collection name | MetaPixel Creatures |
| `symbol` | Collection ticker | MPC |
| `website` | Official website | https://metapixel.example |
| `blockchain` | Network | Ethereum |
| `nft_standard` | Token standard | `ERC-721` |
| `collection_type` | NFT category | Generative Art |
| `total_supply` | Maximum collection size | 5000 |
| `minted_supply` | Number already minted | 1200 |
| `trait_categories` | Number of trait categories | 8 |
| `traits` | Trait category names (list, or text separated by |) | Background, Body, Eyes |
| `marketplace` | NFT marketplace | OpenSea |
| `mint_price` | Price per NFT | 0.05 ETH |
| `mint_date` | Planned mint date, ISO format | `2027-02-15` |
| `reveal_date` | Planned reveal date, ISO format | `2027-02-20` |
| `utility` | Holder benefits (list) | Holder membership |
| `milestones` | List of title, status (Completed, Upcoming or Planned) and date | Website Launch, Completed |
| `description` | Short project introduction | A generative art collection |

Dates use the ISO format, for example `2027-02-15`. In CSV files, separate list values with `|` and write milestones as `Title:Status:Date|Title:Status:Date`. See [`data/nft_collections.json`](data/nft_collections.json) and [`data/nft_collections.csv`](data/nft_collections.csv).

## Sample Output

MetaPixel Creatures (fictional demo data), report date 2027-02-01:

| Metric | Value |
|---|---|
| Total supply | 5,000 |
| Minted supply | 1,200 (24.0%) |
| Trait categories | 8 |
| Mint price | 0.05 ETH |
| Mint date | 2027-02-15 (14 days away) |

**Headline ideas**

1. MetaPixel Creatures Sets February 15, 2027 Public Mint Date for Its 5,000 Piece Generative Art NFT Collection on Ethereum
2. MetaPixel Creatures Reaches 1,200 Minted of 5,000 NFTs
3. MetaPixel Creatures Shares NFT Mint and Collection Reveal Schedule
4. MetaPixel Creatures Introduces Eight Trait Categories for Its Generative Art Collection
5. MetaPixel Creatures Announces Collection Website Launch
6. MetaPixel Creatures Outlines Holder Benefits Including Holder Membership

**Warning raised**

- Minted supply is above zero but the mint date is in the future. If this is a presale or allowlist mint, say so in the release; otherwise check the numbers.

The full report is in [`dataset/sample_report_metapixel.md`](dataset/sample_report_metapixel.md).

## Datasets

- [`data/nft_collections.json`](data/nft_collections.json): three fictional sample collections (JSON)
- [`data/nft_collections.csv`](data/nft_collections.csv): the same samples as CSV
- [`dataset/nft_analysis_results.csv`](dataset/nft_analysis_results.csv): 15 analyses (3 samples at 5 report dates)
- [`dataset/expected_reports.json`](dataset/expected_reports.json): reference reports used by the tests and the heartbeat
- [`kaggle/notebook.ipynb`](kaggle/notebook.ipynb): walkthrough notebook

The sample collections are demonstration data, not real NFT projects.

## Distribution Resource

When your announcement is ready, explore NFT focused media distribution through [BuyCryptoPressRelease.com NFT Project PR](https://buycryptopressrelease.com/nft-project-pr/).

## Links

| Platform | URL |
|---|---|
| Online tool | https://buycryptopressrelease.github.io/nft-collection-announcement-analyzer/ |
| GitHub | https://github.com/buycryptopressrelease/nft-collection-announcement-analyzer |
| NPM | https://www.npmjs.com/package/nft-collection-announcement-analyzer |
| PyPI | https://pypi.org/project/nft-collection-announcement-analyzer/ |
| Hugging Face | https://huggingface.co/datasets/buycryptopressrelease/nft-collection-announcement-dataset |
| Kaggle | https://www.kaggle.com/datasets/buycryptopr/nft-collection-announcement-dataset |
| Zenodo | Add your DOI link after the first release |
| Docs | https://nft-collection-announcement-analyzer.readthedocs.io |

## Services

| Platform | URL |
|---|---|
| NFT Project PR | https://buycryptopressrelease.com/nft-project-pr/ |
| Website | https://buycryptopressrelease.com/ |
| Crypto Presale PR | https://buycryptopressrelease.com/crypto-presale-pr/ |
| Token Launch PR | https://buycryptopressrelease.com/token-launch-pr/ |
| Metaverse and Web3 PR | https://buycryptopressrelease.com/metaverse-web3-pr/ |
| FAQ Generator | https://github.com/buycryptopressrelease/buy-crypto-pressrelease-faq-generator |
| Contact | https://buycryptopressrelease.com/contact/ |

## Contact

| Platform | URL |
|---|---|
| Email | mojo@wewinconsultants.com |
| Telegram | https://t.me/indianmojojo |
| WhatsApp | https://wa.me/19177958348 |

## Keywords

NFT Collection Analyzer · NFT Press Release · NFT Announcement · NFT Launch PR · NFT Mint Announcement · NFT Headline Generator · Web3 Press Release · Generative Art NFT · Gaming NFT · BuyCryptoPressRelease

## License

MIT, BuyCryptoPressRelease.com. Analysis output is a starting point for your own writing and is not financial advice.
