# DApp Data Scraper

A streamlined tool for gathering and analyzing Decentralized Application (DApp) data from multiple sources including DappRadar, DeFiLlama, and CMC.

## Features

🚀 **Multi-Source Data Collection**
- **DappRadar**: Gaming, social, and various DApp categories with detailed metrics
- **DeFiLlama**: DeFi protocols with TVL, yield, and treasury data
- **CoinMarketCap**: DAO governance and organizational data

📊 **Simplified Data Model**
- Core DApp information (name, category, chains, status)
- Financial metrics (TVL, volume, users, transactions)
- Token information and governance
- Fee structures
- Multi-chain support

🗃️ **PostgreSQL Database**
- Simple, flattened schema for easy analysis
- 4 core tables: categories, dapps, categories, industries
- Fast queries and straightforward CSV exports

📈 **Analysis Tools**
- Easy CSV export with all data in one file
- Summary statistics and insights
- Quick data previews

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-repo/dapp-scraper.git
cd dapp-scraper
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up PostgreSQL database**
- Install PostgreSQL on your system
- Create a database and user
- Update `config/config.ini` with your database credentials

4. **Configure API keys**
- Get a DappRadar API key from [DappRadar API](https://dappradar.com/api)
- Update the API key in `config/config.ini`

## Configuration

Edit `config/config.ini`:

```ini
[database]
user = your_postgres_user
password = your_postgres_password
host = localhost
port = 5432
name = dappscanerdb

[dappradar]
api_origin = https://apis.dappradar.com/v2/
api_key = your_dappradar_api_key

[defillama]
api_origin = https://api.llama.fi/

[coinmarketcap]
api_key = 
api_origin =
```

**Note**: Do not use quotes around values in the configuration file.

## Usage

### 1. Initialize Database

```bash
python scripts/init_db.py
```

This creates the simplified database schema with 3 tables:
- `categories` - DApp categories lookup
- `dapps` - Main DApp information (flattened)


```

## CSV Export

The CSV export creates files with all DApp data flattened into single rows:
- One row per DApp with all related information
- Metrics as separate columns (metric_tvl, metric_users, etc.)
- Fees information included
- Easy to import into Excel, Google Sheets, or analysis tools

## API Endpoints Used

### DappRadar API
- `/dapps` - List of DApps with basic metrics
- `/dapps/{id}` - Detailed DApp information
- `/dapps/{id}/history` - Historical data

### DeFiLlama API
- `/protocols` - List of DeFi protocols
- `/protocol/{slug}` - Detailed protocol information
- `/treasury/{slug}` - Treasury information
- `/summary/fees/{slug}` - Fee data

### CMC
- Web scraping from CMC website
- Fallback to curated DAO data
## License


next steps:
If the dapp has been funded by traditional VCs or something else
How do they make money, be sustainable and what business model they use?
who relies on tokenomics, who relies on fees or other approaches?
Governance type is important to determine

top 500 dapps based on UAW (take all of this data)

an output of csv with 500 dapps (based on metrics i scrape from APIs)
a text document with the architecture of the variables
what values can variables have?
business model, revenue model, governance_type models, more qualititative data for each of the 500 dapps

determine a methodology to analyze each dapp (step-by-step)
