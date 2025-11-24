# Database Schema Documentation

## DApps Table Columns

| Column | Type | Constraints | Description | Source |
|--------|------|-------------|-------------|---------|
| **Core Identifiers** |||||
| `id` | SERIAL | PRIMARY KEY | Unique identifier for DApp | Auto-generated |
| `name` | VARCHAR(255) | NOT NULL | DApp name | DappRadar |
| `slug` | VARCHAR(255) | UNIQUE NOT NULL | URL-friendly identifier | DappRadar |
| `category_id` | INTEGER | REFERENCES categories(id) | Link to category table | DappRadar |
| **External IDs** |||||
| `gecko_id` | VARCHAR(100) | | CoinGecko API identifier | CoinGecko |
| `cmc_id` | VARCHAR(100) / VARCHAR(20) | | CoinMarketCap identifier | CoinMarketCap |
| **Basic Information** |||||
| `is_active` | BOOLEAN | DEFAULT TRUE | Whether DApp is currently active | DappRadar |
| `description` | TEXT | | Detailed description of the DApp | DappRadar |
| `website` | VARCHAR(500) | | Official website URL | DappRadar |
| `tags` | TEXT | | **Combined tags from all sources** | **DappRadar/CMC/CoinGecko/DeFiLlama** |
| `sub_category` | TEXT | | Sub-category for more granular classification | Manual/Research |
| **Blockchain Information** |||||
| `chains` | TEXT | | Blockchain networks (comma-separated) | DappRadar |
| `multi_chain` | BOOLEAN | DEFAULT FALSE | Whether DApp operates on multiple chains | Calculated |
| **Dates and Ownership** |||||
| `birth_date` | DATE | | Launch date of the DApp | DappRadar |
| **Financial Data** |||||
| `capital_raised` | NUMERIC | DEFAULT 0 | Amount of capital raised | DeFiLlama |
| **Token Information** |||||
| `token_name` | VARCHAR(100) | | Primary token name | DappRadar |
| `token_symbol` | VARCHAR(20) | | Primary token symbol | DappRadar |
| `token_format` | VARCHAR(50) | | Token format (ERC-20, BEP-20, etc.) | DappRadar |
| **🏛️ Governance & Ownership (ENUM Types)** |||||
| `governance_type` | governance_type_enum | | **Governance model** (see values below) | Manual/Research |
| `ownership_status` | ownership_status_enum | | **Ownership structure** (see values below) | Manual/Research |
| `level_of_decentralisation` | decentralisation_level_enum | | **Decentralization level** (see values below) | Manual/Research |
| `research_comments` | TEXT | | Research notes and comments about the DApp | Manual/Research |
| **DApp Metrics** |||||
| `tvl` | NUMERIC | DEFAULT 0 | Total Value Locked in USD | DeFiLlama |
| `tvl_ratio` | NUMERIC | DEFAULT 0 | TVL ratio metric | Calculated |
| `users` | BIGINT | DEFAULT 0 | Unique active wallets | DappRadar |
| `volume` | NUMERIC | DEFAULT 0 | Trading/transaction volume in USD | DappRadar |
| `transactions` | BIGINT | DEFAULT 0 | Total transaction count | DappRadar |
| `market_cap` | NUMERIC | DEFAULT 0 | Market capitalization | CoinMarketCap |
| `mcap` | NUMERIC | DEFAULT 0 | Market cap (alternative field) | CoinGecko |
| **Token Supply & Market Data** |||||
| `circulating_supply` | NUMERIC | DEFAULT 0 | Circulating token supply | CoinMarketCap |
| `total_supply` | NUMERIC | DEFAULT 0 | Total token supply | CoinMarketCap |
| `max_supply` | NUMERIC | DEFAULT 0 | Maximum token supply | CoinMarketCap |
| **Price and Market Data** |||||
| `price` | NUMERIC | DEFAULT 0 | Current token price in USD | CoinMarketCap |
| `volume_24h` | NUMERIC | DEFAULT 0 | 24-hour trading volume | CoinMarketCap |
| `volume_change_24h` | NUMERIC | DEFAULT 0 | 24-hour volume change percentage | CoinMarketCap |
| `percent_change_1h` | NUMERIC | DEFAULT 0 | 1-hour price change percentage | CoinMarketCap |
| `percent_change_24h` | NUMERIC | DEFAULT 0 | 24-hour price change percentage | CoinMarketCap |
| `percent_change_7d` | NUMERIC | DEFAULT 0 | 7-day price change percentage | CoinMarketCap |
| `percent_change_30d` | NUMERIC | DEFAULT 0 | 30-day price change percentage | CoinMarketCap |
| `percent_change_60d` | NUMERIC | DEFAULT 0 | 60-day price change percentage | CoinMarketCap |
| `percent_change_90d` | NUMERIC | DEFAULT 0 | 90-day price change percentage | CoinMarketCap |
| `cmc_rank` | INTEGER | DEFAULT 0 | CoinMarketCap ranking | CoinMarketCap |
| `market_cap_dominance` | NUMERIC | DEFAULT 0 | Market cap dominance percentage | CoinMarketCap |
| `fully_diluted_market_cap` | NUMERIC | DEFAULT 0 | Fully diluted market capitalization | CoinMarketCap |
| **Timestamps** |||||
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp | Auto-generated |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update timestamp | Auto-generated |

## 🏛️ ENUM Type Values Explained

The database uses PostgreSQL ENUM types to enforce data integrity for governance-related fields:

### ownership_status_enum
| Value | Description |
|-------|-------------|
| `COMPANY_OWNED` | Contracts/treasury controlled by a private company |
| `FOUNDATION_OWNED` | Primary control via non-profit foundation |
| `DAO_OWNED` | Admin + treasury controlled by on-chain DAO |
| `UNKNOWN` | Insufficient evidence to determine ownership |
| `MIXED` | Mixed ownership structure with multiple parties |
| `ORPHANED` | Abandoned or no clear maintainer |

### governance_type_enum
| Value | Description |
|-------|-------------|
| `NONE` | No formal governance structure |
| `TEAM_CONTROLLED` | Core team decides without external input |
| `SNAPSHOT_OFFCHAIN` | Off-chain snapshot voting for governance |
| `ONCHAIN_TOKEN_GOVERNANCE` | On-chain token-based governance |
| `HYBRID` | Hybrid governance combining multiple mechanisms |
| `MULTISIG_WITH_COMMUNITY_INPUT` | Multisig execution with community input |
| `DAO_WITH_TIMELOCK` | DAO governance with timelock protection |

### decentralisation_level_enum
| Value | Description |
|-------|-------------|
| `CENTRALIZED` | Centralized control and decision-making |
| `SEMI_DECENTRALIZED` | Mixed centralized and decentralized elements |
| `DECENTRALIZED` | Fully decentralized governance and control |

## Other Database Tables

### Categories Table
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique category identifier |
| `name` | VARCHAR(100) | UNIQUE NOT NULL | Category name (e.g., "DeFi", "Gaming", "NFT") |

### TVL Historical Table
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique record identifier |
| `dapp_id` | INTEGER | REFERENCES dapps(id) ON DELETE CASCADE | Link to DApp |
| `date` | DATE | NOT NULL | Date of TVL measurement |
| `total_liquidity_usd` | NUMERIC | NOT NULL | TVL in USD on that date |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |

### Raises/Funding Table
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique funding record identifier |
| `dapp_id` | INTEGER | REFERENCES dapps(id) ON DELETE CASCADE | Link to DApp |
| `date` | DATE | NOT NULL | Date of funding round |
| `name` | VARCHAR(255) | | Name of the funding round |
| `round` | VARCHAR(100) | | Funding round type (Seed, Series A, etc.) |
| `amount` | NUMERIC | | Amount raised in USD |
| `chains` | TEXT | | Blockchain networks |
| `sector` | TEXT | | Industry sector |
| `category` | VARCHAR(100) | | DeFiLlama category |
| `category_group` | VARCHAR(100) | | DeFiLlama category group |
| `source` | VARCHAR(500) | | Data source URL |
| `lead_investors` | TEXT | | Lead investors (comma-separated) |
| `other_investors` | TEXT | | Other investors (comma-separated) |
| `valuation` | NUMERIC | | Company valuation in USD |
| `defillama_id` | VARCHAR(100) | | DeFiLlama protocol identifier |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |

## Data Sources & Collection Strategy

- **Primary Source**: DappRadar (500 top DApps by UAW - Unique Active Wallets)
- **Secondary Sources**: 
  - CoinMarketCap (market data, price info)
  - CoinGecko (alternative market data)  
  - DeFiLlama (TVL data, funding information)
- **Manual Research**: Governance, ownership, and decentralization data added via manual research

## Notes

- Some columns have duplicates (e.g., `gecko_id`, `cmc_id`) due to schema evolution - will be cleaned up
- Missing values default to 0 or NULL depending on column type
- **ENUM Types**: `ownership_status`, `governance_type`, and `level_of_decentralisation` use PostgreSQL ENUMs for data integrity
- **Tags**: Combined from all sources with deduplication (DappRadar tags, CMC tags, CoinGecko categories, DeFiLlama categories)
- **Research Data**: Governance, ownership, and decentralization fields are populated via manual research and enrichment

## Database Migration Instructions

### For New Databases
Simply run: `python scripts/init_db.py`

### For Existing Databases
To update the schema with the latest changes (new columns, removed score columns, etc.):
```bash
python migrations/migrate_schema_updates.py
```

To ingest manually enriched data from a CSV file:
```bash
python scripts/ingest_pilot_data.py [path/to/csv_file.csv]
```
