"""
DApp Ecosystem Analysis - Key Insights & Messages
==================================================
Synthesizes findings from all analyses (01-08 + 10-13) into
comprehensive key messages for the thesis and presentation.

Now includes:
  - Token type insights (new enum)
  - Sector deep-dive highlights
  - Anomaly / contradiction highlights
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from collections import Counter

from config import DATA_PATH, OUTPUT_DIR

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-darkgrid')


def main():
    print("\n" + "="*70)
    print(" " * 10 + "KEY INSIGHTS - DAPP ECOSYSTEM ANALYSIS (EXTENDED)")
    print("="*70)

    df = pd.read_csv(DATA_PATH)

    df_gov = df.dropna(subset=['level_of_decentralisation'])
    df_market = df[df['market_cap'] > 0]
    df_users = df[df['users'] > 0]
    df_tvl = df[df['tvl'] > 0]

    insights = []

    # ── INSIGHT 1: Governance Centralization Paradox ──
    truly_decent_pct = (df_gov['level_of_decentralisation'] == 'DECENTRALIZED').mean() * 100
    company_owned_pct = (df_gov['ownership_status'] == 'COMPANY_OWNED').mean() * 100
    team_controlled = (df_gov['governance_type'] == 'TEAM_CONTROLLED').sum()
    team_controlled_pct = team_controlled / len(df_gov) * 100

    insight_1 = f"""
KEY INSIGHT #1: THE GOVERNANCE CENTRALIZATION PARADOX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Only {truly_decent_pct:.1f}% of DApps are truly decentralized
• {company_owned_pct:.1f}% are company-owned despite blockchain foundation
• {team_controlled_pct:.1f}% use team-controlled governance
• Gap between rhetoric and reality in "decentralized" applications
"""
    insights.append(insight_1)

    # ── INSIGHT 2: Chain Ecosystem Specialization ──
    chain_dist = []
    for chains_str in df['chains'].dropna():
        chains = [c.strip() for c in str(chains_str).split(',')]
        chain_dist.extend(chains)
    chain_counts = Counter(chain_dist)
    top_chain = chain_counts.most_common(1)[0]
    multichain_pct = df['is_multi_chain'].mean() * 100
    n_chains = len(chain_counts)

    insight_2 = f"""
KEY INSIGHT #2: CHAIN ECOSYSTEM SPECIALIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• {n_chains} unique blockchains hosting DApps
• {top_chain[0]} leads with {top_chain[1]} DApp deployments
• Only {multichain_pct:.1f}% of DApps deploy across multiple chains
• Chains developing specialized niches (DeFi vs Gaming vs Social)
"""
    insights.append(insight_2)

    # ── INSIGHT 3: Extreme Market Concentration ──
    total_mcap = df_market['market_cap'].sum()
    top_10_mcap = df_market.nlargest(10, 'market_cap')['market_cap'].sum()
    top_10_pct = top_10_mcap / total_mcap * 100

    total_users = df_users['users'].sum()
    top_10_users = df_users.nlargest(10, 'users')['users'].sum()
    top_10_user_pct = top_10_users / total_users * 100

    insight_3 = f"""
KEY INSIGHT #3: EXTREME WEALTH AND USER CONCENTRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Top 10 DApps control {top_10_pct:.1f}% of total market cap
• Top 10 DApps attract {top_10_user_pct:.1f}% of all users
• Power law distribution (winner-takes-all dynamics)
• Total market cap: ${total_mcap/1e9:.1f}B concentrated in few players
"""
    insights.append(insight_3)

    # ── INSIGHT 4: Engagement Dichotomy ──
    gaming = df[df['dapp_category'] == 'NFT Gaming']
    dex = df[df['dapp_category'] == 'DEX']
    gaming_users = gaming['users'].sum()
    dex_users = dex['users'].sum()
    gaming_vol = gaming[gaming['volume'] > 0]['volume'].sum()
    dex_vol = dex[dex['volume'] > 0]['volume'].sum()

    insight_4 = f"""
KEY INSIGHT #4: THE ENGAGEMENT DICHOTOMY (Gaming vs DeFi)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Gaming: {gaming_users:,.0f} users, ${gaming_vol/1e6:.0f}M volume
• DeFi/DEX: {dex_users:,.0f} users, ${dex_vol/1e9:.1f}B volume
• Gaming = high users, low economic activity per user
• DeFi = fewer users, massive value per transaction
"""
    insights.append(insight_4)

    # ── INSIGHT 5: TVL Concentration ──
    total_tvl = df_tvl['tvl'].sum()
    top_10_tvl = df_tvl.nlargest(10, 'tvl')['tvl'].sum()
    tvl_conc = top_10_tvl / total_tvl * 100

    insight_5 = f"""
KEY INSIGHT #5: TVL CONCENTRATION & EFFICIENCY GAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Total TVL: ${total_tvl/1e9:.1f}B across ecosystem
• Top 10 DApps control {tvl_conc:.1f}% of all TVL
• Capital flows to established players
"""
    insights.append(insight_5)

    # ── INSIGHT 6: Funding Paradox ──
    df_funded = df[df['raised_capital'] > 0].copy()
    total_funding = df_funded['raised_capital'].sum()
    df_funded['funding_eff'] = np.where(
        df_funded['market_cap'] > 0,
        df_funded['market_cap'] / (df_funded['raised_capital'] * 1e6), 0)
    eff_clean = df_funded[(df_funded['funding_eff'] > 0) &
                          (df_funded['funding_eff'] < df_funded['funding_eff'].quantile(0.95))]
    median_roi = eff_clean['funding_eff'].median() if len(eff_clean) > 0 else 0

    insight_6 = f"""
KEY INSIGHT #6: THE FUNDING EFFICIENCY PARADOX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Total capital raised: ${total_funding:,.0f}M across {len(df_funded)} DApps
• Median market cap / funding ratio: {median_roi:.2f}x
• Funding does not guarantee success or adoption
"""
    insights.append(insight_6)

    # ── INSIGHT 7: Multi-Chain Premium ──
    multichain_mcap = df[(df['is_multi_chain'] == True) & (df['market_cap'] > 0)]['market_cap'].mean()
    singlechain_mcap = df[(df['is_multi_chain'] == False) & (df['market_cap'] > 0)]['market_cap'].mean()
    premium = multichain_mcap / singlechain_mcap if singlechain_mcap > 0 else 0

    insight_7 = f"""
KEY INSIGHT #7: THE MULTI-CHAIN PREMIUM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Multi-chain DApps: avg market cap ${multichain_mcap/1e6:.1f}M
• Single-chain DApps: avg market cap ${singlechain_mcap/1e6:.1f}M
• Multi-chain premium: {premium:.1f}x higher valuation
• Only {multichain_pct:.1f}% of DApps deploy multi-chain
"""
    insights.append(insight_7)

    # ── INSIGHT 8: Governance-Performance Link ──
    gov_corr_data = df[(df['governance_score'].notna()) & (df['market_cap'] > 0)].copy()
    gov_corr_data['mcap_log'] = np.log1p(gov_corr_data['market_cap'])
    gov_corr = gov_corr_data[['governance_score', 'mcap_log']].corr().iloc[0, 1]

    decent_mcap = df_gov[df_gov['level_of_decentralisation'] == 'DECENTRALIZED']['market_cap'].median()
    central_mcap = df_gov[df_gov['level_of_decentralisation'] == 'CENTRALIZED']['market_cap'].median()

    insight_8 = f"""
KEY INSIGHT #8: GOVERNANCE-PERFORMANCE CORRELATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Governance score correlates {gov_corr:.2f} with log(market cap)
• Decentralized DApps: median market cap ${decent_mcap/1e6:.1f}M
• Centralized DApps: median market cap ${central_mcap/1e6:.1f}M
"""
    insights.append(insight_8)

    # ── INSIGHT 9: Token Type Economy (NEW) ──
    tt_dist = df[df['has_token']]['token_type_primary'].value_counts()
    dominant_tt = tt_dist.index[0]
    dominant_tt_pct = tt_dist.values[0] / df['has_token'].sum() * 100

    gov_tokens = df['is_governance_token'].sum()
    gov_token_pct = gov_tokens / len(df) * 100
    gov_tok_decent = df[df['is_governance_token']]
    gov_tok_truly_decent = (gov_tok_decent['level_of_decentralisation'] == 'DECENTRALIZED').mean() * 100

    gov_tok_mcap = df_market[df_market['is_governance_token']]['market_cap'].median()
    util_tok_mcap = df_market[df_market['is_utility_token']]['market_cap'].median()

    insight_9 = f"""
KEY INSIGHT #9: TOKEN TYPE ECONOMY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Dominant token type: {dominant_tt} ({dominant_tt_pct:.1f}% of tokenized DApps)
• {gov_tokens} DApps ({gov_token_pct:.1f}%) have governance tokens
• Of governance-token DApps, only {gov_tok_truly_decent:.1f}% are truly decentralized
• Governance tokens: median MCap ${gov_tok_mcap/1e6:.1f}M
• Utility tokens: median MCap ${util_tok_mcap/1e6:.1f}M
• Token type predicts governance model adoption patterns
"""
    insights.append(insight_9)

    # ── INSIGHT 10: Sector Specialization (NEW) ──
    sector_counts = {
        'DeFi': df['is_defi'].sum(),
        'Gaming': df['is_gaming'].sum(),
        'Social': df['is_social'].sum(),
        'Prediction Mkt': df['is_prediction_market'].sum(),
        'RWA': df['is_rwa'].sum(),
        'AI': df['is_ai'].sum(),
    }
    defi_tvl = df[df['is_defi']]['tvl'].sum()
    defi_tvl_pct = defi_tvl / total_tvl * 100 if total_tvl > 0 else 0

    insight_10 = f"""
KEY INSIGHT #10: SECTOR SPECIALIZATION & EMERGING NICHES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• DeFi: {sector_counts['DeFi']} DApps, controlling {defi_tvl_pct:.1f}% of total TVL
• Gaming: {sector_counts['Gaming']} DApps (largest user base)
• Prediction Markets: {sector_counts['Prediction Mkt']} DApps (emerging niche)
• AI DApps: {sector_counts['AI']} DApps (nascent but growing)
• RWA: {sector_counts['RWA']} DApps (bridging traditional finance)
• Each sector shows distinct governance and tokenomics patterns
"""
    insights.append(insight_10)

    # ── INSIGHT 11: Anomalies & Contradictions (NEW) ──
    decent_company = ((df['level_of_decentralisation'] == 'DECENTRALIZED') &
                      (df['ownership_status'] == 'COMPANY_OWNED')).sum()
    gov_tok_team = (df['is_governance_token'] &
                    (df['governance_type'] == 'TEAM_CONTROLLED')).sum()

    df_unfunded = df[(df['raised_capital'].fillna(0) == 0) & (df['market_cap'] > 0)]
    df_funded_mkt = df[(df['raised_capital'] > 0) & (df['market_cap'] > 0)]
    funded_median = df_funded_mkt['market_cap'].median() if len(df_funded_mkt) > 0 else 0
    unfunded_above = len(df_unfunded[df_unfunded['market_cap'] > funded_median])

    insight_11 = f"""
KEY INSIGHT #11: ECOSYSTEM CONTRADICTIONS & ANOMALIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• {decent_company} DApps labelled "Decentralized" but Company-Owned
• {gov_tok_team} DApps have governance tokens but are Team-Controlled
• {unfunded_above} unfunded DApps outperform funded DApps' median MCap
• These contradictions raise questions about labelling accuracy
  and the real meaning of "decentralization" in the sector
"""
    insights.append(insight_11)

    # ── Print all ──
    for insight in insights:
        print(insight)

    # ── Summary visualization ──
    fig, ax = plt.subplots(figsize=(14, 12))
    ax.axis('off')

    title_text = f"11 KEY INSIGHTS: DApp Ecosystem Analysis\n(Based on {len(df)} DApps)\n"

    summary_lines = [
        f"1. GOVERNANCE PARADOX: Only {truly_decent_pct:.1f}% truly decentralized",
        f"2. CHAIN SPECIALIZATION: {n_chains} blockchains, {top_chain[0]} leads",
        f"3. MARKET CONCENTRATION: Top 10 control {top_10_pct:.1f}% of MCap",
        f"4. ENGAGEMENT DICHOTOMY: Gaming = users; DeFi = value",
        f"5. TVL EFFICIENCY GAP: Top 10 control {tvl_conc:.1f}% of TVL",
        f"6. FUNDING PARADOX: Capital ≠ success ({median_roi:.2f}x median ROI)",
        f"7. MULTI-CHAIN PREMIUM: {premium:.1f}x higher valuation",
        f"8. GOVERNANCE-PERFORMANCE: r={gov_corr:.2f} with market cap",
        f"9. TOKEN TYPES: {dominant_tt} dominates; gov tokens ≠ decentralization",
        f"10. SECTOR NICHES: DeFi, Gaming, AI, Prediction Markets diverge",
        f"11. ANOMALIES: {decent_company} contradictions challenge sector narratives",
    ]

    ax.text(0.5, 0.97, title_text, transform=ax.transAxes,
            fontsize=16, fontweight='bold', ha='center', va='top',
            bbox=dict(boxstyle='round', facecolor='#2c3e50', alpha=0.9),
            color='white')

    y_start = 0.85
    for i, line in enumerate(summary_lines):
        ax.text(0.05, y_start - i * 0.07, line, transform=ax.transAxes,
                fontsize=11, ha='left', va='top', family='monospace',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.3))

    ax.text(0.5, 0.02,
            f'Analysis of {len(df)} DApps | {df["dapp_category"].nunique()} categories | '
            f'{n_chains} blockchains',
            transform=ax.transAxes, fontsize=10, ha='center', va='bottom',
            style='italic', color='gray')

    plt.tight_layout()
    output_path = OUTPUT_DIR / '09_key_insights_summary.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Summary visualization saved: {output_path}")
    plt.close()

    # ── Save insights text ──
    insights_file = OUTPUT_DIR / '09_KEY_INSIGHTS.txt'
    with open(insights_file, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write(" " * 10 + "11 KEY INSIGHTS - DAPP ECOSYSTEM ANALYSIS\n")
        f.write("=" * 70 + "\n\n")
        for insight in insights:
            f.write(insight + "\n")
        f.write("\n" + "=" * 70 + "\n")
        f.write(f"Analysis based on {len(df)} DApps\n")
        f.write(f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}\n")
        f.write("=" * 70 + "\n")

    print(f"✓ Insights document saved: {insights_file}")

    print("\n" + "="*70)
    print("KEY INSIGHTS SYNTHESIS COMPLETE!")
    print("="*70)
    print("\nThese 11 insights provide the foundation for your thesis:")
    for i, line in enumerate(summary_lines, 1):
        print(f"  {line}")


if __name__ == "__main__":
    main()
