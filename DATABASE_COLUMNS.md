# Database Schema Documentation

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique identifier for DApp |
| `name` | VARCHAR(255) | NOT NULL | DApp name |
| `slug` | VARCHAR(255) | UNIQUE NOT NULL | URL-friendly identifier |
| `category_id` | INTEGER | REFERENCES categories(id) | Link to category table |
| `status` | VARCHAR(50) | DEFAULT 'active' | DApp status (active, inactive, etc.) |
| `industry` | VARCHAR(100) | | Industry classification |
| `description` | TEXT | | Detailed description of the DApp |
| `website` | VARCHAR(500) | | Official website URL |
| `chains` | TEXT | | Blockchain networks (comma-separated for multi-chain) |
| `multi_chain` | BOOLEAN | DEFAULT FALSE | Whether DApp operates on multiple chains |
| `birth_date` | DATE | | Launch date of the DApp |
| `ownership_status` | VARCHAR(100) | | Ownership structure (e.g., DAO, Centralized) |
| `decentralisation_lvl` | VARCHAR(50) | | Level of decentralization |
| `capital_raised` | NUMERIC | DEFAULT 0 | Amount of capital raised |
| `showcase_fun` | BOOLEAN | DEFAULT FALSE | Featured/showcase flag |
| `token_name` | VARCHAR(100) | | Primary token name |
| `token_symbol` | VARCHAR(20) | | Primary token symbol |
| `token_format` | VARCHAR(50) | | Token format (ERC-20, BEP-20, etc.) |
| `governance_type` | VARCHAR(100) | | Governance model (DAO, Centralized, Multi-sig) |
| `twitter` | VARCHAR(200) | | Twitter handle/URL |
| `discord` | VARCHAR(200) | | Discord server URL |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update timestamp |

Suggestion: 
- use DappRadar as primary source
- scrape ranking for DAPPs based on UAW (unique active wallets)
- build own classification for dapp categories (multi-level)
- full list & description of variables that are scraped
- possible values for each variable
- send a pilot dataset of 20-30 dapps max consisting variability

Use DappRadar to get the 500 top Dapps
Use 500 tickers from DappRadar to scrape additional data for each DAPP from CMC & DefiLlama