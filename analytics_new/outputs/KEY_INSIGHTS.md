# Key insights (machine-assisted draft)

## Governance mix (eligible population)
- TEAM_CONTROLLED: 62.7%
- SNAPSHOT_OFFCHAIN: 19.5%
- NONE: 6.2%
- ONCHAIN_TOKEN_GOVERNANCE: 4.8%
- HYBRID: 2.8%

## Token types (eligible)
- UTILITY: 47.7%
- REWARD: 25.8%
- GOVERNANCE: 16.6%
- SPECULATIVE: 6.3%
- GOVERNANCE, UTILITY: 1.9%
- UTILITY, GOVERNANCE: 1.0%

## Multi-chain share
- Eligible DApps with `is_multi_chain`: **36.2%**; primary cohort: **36.9%**.

## Cohort vs full eligible (by sector counts)
| dapp_sector | eligible_all | primary_cohort |
| --- | --- | --- |
| collectibles | 57 | 52 |
| defi | 105 | 105 |
| exchanges | 76 | 56 |
| gambling | 116 | 113 |
| games | 115 | 80 |
| high-risk | 120 | 106 |
| marketplaces | 73 | 62 |
| other | 84 | 84 |
| social | 88 | 88 |

## Theme cohorts (eligible matches)
| theme | description | n_all_matched | n_eligible_matched | pct_governance_token | top_governance_type |
| --- | --- | --- | --- | --- | --- |
| prediction_markets | dapp_category == Prediction Market OR text match (prediction, polymarket, augur, forecast) | 32 | 32 | 0.0 | TEAM_CONTROLLED |
| ai_dapps | regex on tags, sub_category, research_comments, name: ai, llm, machine learning, ai gaming, ai-big-data | 66 | 66 | 0.1212121212121212 | TEAM_CONTROLLED |
| depin_rwa | Payments/RWA category OR tags/text: depin, rwa, move to earn, tokenized real world | 70 | 69 | 0.072463768115942 | TEAM_CONTROLLED |

### Theme rulebook (audit)
- **prediction_markets:** dapp_category == Prediction Market OR text match (prediction, polymarket, augur, forecast)
- **ai_dapps:** regex on tags, sub_category, research_comments, name: ai, llm, machine learning, ai gaming, ai-big-data
- **depin_rwa:** Payments/RWA category OR tags/text: depin, rwa, move to earn, tokenized real world
