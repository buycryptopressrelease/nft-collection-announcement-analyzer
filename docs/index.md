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

### NFT Analysis Report: MetaPixel Creatures

Ethereum · ERC-721 · Generative Art

Report date: 2027-02-01

#### Key numbers

| Metric | Value |
|---|---|
| Total supply | 5,000 |
| Minted supply | 1,200 |
| Remaining | 3,800 |
| Minted percent | 24.0% |
| Supply status | Minting |
| Trait categories | 8 |
| Mint price | 0.05 ETH |
| Mint date | 2027-02-15 (Upcoming) |
| Reveal date | 2027-02-20 (Upcoming) |

#### Suggested announcement angles

1. NFT mint schedule announcement
2. Mint progress update
3. Collection reveal announcement
4. Generative Art collection introduction
5. Trait and artwork design reveal
6. Holder utility and community benefits
7. Milestone achieved: Collection Website Launch
8. Roadmap update
9. Launch on Ethereum

#### Headline ideas

1. MetaPixel Creatures Sets February 15, 2027 Public Mint Date for Its 5,000 Piece Generative Art NFT Collection on Ethereum
2. MetaPixel Creatures Reaches 1,200 Minted of 5,000 NFTs
3. MetaPixel Creatures Shares NFT Mint and Collection Reveal Schedule
4. MetaPixel Creatures Introduces Eight Trait Categories for Its Generative Art Collection
5. MetaPixel Creatures Announces Collection Website Launch
6. MetaPixel Creatures Outlines Holder Benefits Including Holder Membership

#### Recommended press release topics

- NFT collection launch announcement
- Upcoming mint date announcement
- Mint progress and community update
- Generative Art project introduction
- NFT utility and community announcement
- Milestone and partnership announcement
- Roadmap announcement

#### Milestones

**Completed:** Collection Website Launch (2027-01-10)

**Upcoming:** NFT Mint Opening (2027-02-15); Collection Reveal (2027-02-20)

**Planned:** none

#### Press release outline

**Headline:** MetaPixel Creatures Sets February 15, 2027 Public Mint Date for Its 5,000 Piece Generative Art NFT Collection on Ethereum  
**Subheadline:** MetaPixel Creatures: 5,000 NFT collection, built on Ethereum (ERC-721), listed on OpenSea  
**Dateline:** [CITY], [DATE]  
**Opening paragraph:** MetaPixel Creatures (MPC), a Generative Art collection on Ethereum, is scheduled to open its mint on February 15, 2027.  
**Collection details:** Total supply: 5,000; Minted: 1,200 (24.0%); Mint price: 0.05 ETH; Marketplace: OpenSea  
**Art and traits:** 8 trait categories: Background, Body, Eyes, Headwear, Clothing, Mouth, Accessories, Special Effects  
**Schedule:** Mint: February 15, 2027; Reveal: February 20, 2027  
**Utility (project stated):** Holder membership; Digital collectibles; Community access  
**Roadmap:** Completed: Collection Website Launch | Upcoming: NFT Mint Opening; Collection Reveal  
**Quote:** [Quote from the MetaPixel Creatures founder or lead artist]  
**About:** About MetaPixel Creatures: [two sentences] Website: https://metapixel.example  
**Media contact:** [Name, email, website]  
**Disclaimer:** NFTs are digital assets and carry risk. This announcement is for information only and is not financial advice.  

#### Facts to check before publishing

| Statement | Type |
|---|---|
| Total supply is 5,000 | Project data |
| 1,200 NFTs minted as of 2027-02-01 | Project data, verify on chain |
| Mint date 2027-02-15 | Scheduled |
| Reveal date 2027-02-20 | Scheduled |
| Collection Website Launch | Completed, keep proof ready |
| NFT Mint Opening | Upcoming, describe as scheduled |
| Collection Reveal | Upcoming, describe as scheduled |
| Holder membership | Project claim |
| Digital collectibles | Project claim |
| Community access | Project claim |

#### Warnings

- Minted supply is above zero but the mint date is in the future. If this is a presale or allowlist mint, say so in the release; otherwise check the numbers.

#### Distribution resource

Explore NFT focused media distribution through BuyCryptoPressRelease.com. [NFT Project PR](https://buycryptopressrelease.com/nft-project-pr/)


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
