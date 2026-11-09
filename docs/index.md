# NFT Collection Announcement Analyzer

Free tool that analyzes NFT collection details, supply, traits, blockchain, mint schedule and milestones to generate announcement angles, headline ideas, press release topics and a press release outline. Built by [BuyCryptoPressRelease.com](https://buycryptopressrelease.com/).

!!! tip "Try it online"
    Open the browser version at [https://buycryptopressrelease.github.io/nft-collection-announcement-analyzer/](https://buycryptopressrelease.github.io/nft-collection-announcement-analyzer/). Nothing you type leaves your browser.

## Install

```bash
pip install nft-collection-announcement-analyzer
# or
npm install -g nft-collection-announcement-analyzer
```

## Use

```bash
nft-analyzer my_collection.json
nft-analyzer my_collections.csv --format json
nft-analyzer data/nft_collections.json --id 2 --today 2027-03-12
```

## Commands and Options

| Command / option | What it does |
|---|---|
| `nft-analyzer FILE` | Analyze every collection in a JSON or CSV file |
| `--id N` | Analyze only collection N |
| `--list` | List the collections in the file |
| `--format md\|json\|txt` | Output format (default md) |
| `--today YYYY-MM-DD` | Report date used to decide what is upcoming or past |

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

## Honesty Rules

- Milestones keep the status you give them. Planned stays planned.
- A milestone marked Completed with a future date is flagged.
- Minted supply above zero before the mint date is flagged as a possible presale.
- Utility is labelled as a project claim in the fact check list.
- Words like guaranteed, profit, returns and 100x are flagged and kept out of headlines.

## Sample Report

See [`dataset/sample_report_metapixel.md`](https://github.com/buycryptopressrelease/nft-collection-announcement-analyzer/blob/main/dataset/sample_report_metapixel.md) for a full report on the MetaPixel Creatures sample.

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
| NFT Project PR | https://buycryptopressrelease.com/nft-project-pr/ |
