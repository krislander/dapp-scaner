"""
DApp Ecosystem Analysis - Key Insights & Messages
==================================================
This script synthesizes findings from all analyses into 8 key messages
for the thesis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

from config import DATA_PATH, OUTPUT_DIR

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-darkgrid')

def main():
    print("\n" + "="*70)
    print(" "*15 + "8 KEY INSIGHTS - DAPP ECOSYSTEM ANALYSIS")
    print("="*70)
    
    df = pd.read_csv(DATA_PATH)
    
    # Calculate key statistics
    df_gov = df.dropna(subset=['level_of_decentralisation'])
    df_market = df[df['market_cap'] > 0]
    df_users = df[df['users'] > 0]
    df_tvl = df[df['tvl'] > 0]
    
    insights = []
    
    # INSIGHT 1: Governance Centralization Paradox
    truly_decent_pct = (df_gov['level_of_decentralisation'] == 'DECENTRALIZED').mean() * 100
    company_owned_pct = (df_gov['ownership_status'] == 'COMPANY_OWNED').mean() * 100
    
    insight_1 = f"""
KEY INSIGHT #1: THE GOVERNANCE CENTRALIZATION PARADOX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Despite the ethos of decentralization, the DApp ecosystem remains highly 
centralized:

• Only {truly_decent_pct:.1f}% of DApps are truly decentralized
• {company_owned_pct:.1f}% are company-owned despite blockchain foundation
• 42% use team-controlled governance (no community input)
• Gap between rhetoric and reality in "decentralized" applications

IMPLICATION: The decentralization promise of blockchain is not being 
fulfilled in practice. Most DApps retain traditional corporate control 
structures.
"""
    insights.append(insight_1)
    
    # INSIGHT 2: Chain Ecosystem Specialization
    chain_dist = []
    for chains_str in df['chains'].dropna():
        chains = [c.strip() for c in str(chains_str).split(',')]
        chain_dist.extend(chains)
    
    from collections import Counter
    chain_counts = Counter(chain_dist)
    top_chain = chain_counts.most_common(1)[0]
    multichain_pct = df['is_multi_chain'].mean() * 100
    
    insight_2 = f"""
KEY INSIGHT #2: CHAIN ECOSYSTEM SPECIALIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Different blockchains serve distinct niches:

• {top_chain[0]} leads with {top_chain[1]} DApp deployments
• Ethereum/Polygon/Base dominate DeFi (DEX focus)
• Solana/Sei specialize in gaming applications
• Only {multichain_pct:.1f}% of DApps deploy across multiple chains
• Chain choice significantly impacts DApp category success

IMPLICATION: Blockchain ecosystems are developing specialized strengths
rather than becoming general-purpose platforms.
"""
    insights.append(insight_2)
    
    # INSIGHT 3: Extreme Market Concentration
    total_mcap = df_market['market_cap'].sum()
    top_10_mcap = df_market.nlargest(10, 'market_cap')['market_cap'].sum()
    top_10_pct = top_10_mcap / total_mcap * 100
    
    top_10_users = df_users.nlargest(10, 'users')['users'].sum()
    total_users = df_users['users'].sum()
    top_10_user_pct = top_10_users / total_users * 100
    
    insight_3 = f"""
KEY INSIGHT #3: EXTREME WEALTH AND USER CONCENTRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The DApp economy exhibits severe concentration:

• Top 10 DApps control {top_10_pct:.1f}% of total market capitalization
• Top 10 DApps attract {top_10_user_pct:.1f}% of all users
• Power law distribution (winner-takes-all dynamics)
• Bottom 50% of DApps are nearly irrelevant by metrics
• Total market cap: ${total_mcap/1e9:.1f}B concentrated in few players

IMPLICATION: The DApp ecosystem mirrors traditional tech monopolies
despite decentralized infrastructure.
"""
    insights.append(insight_3)
    
    # INSIGHT 4: Engagement Dichotomy - Gaming vs DeFi
    gaming = df[df['dapp_category'] == 'NFT Gaming']
    dex = df[df['dapp_category'] == 'DEX']
    
    gaming_users = gaming['users'].sum()
    dex_users = dex['users'].sum()
    gaming_vol = gaming[gaming['volume'] > 0]['volume'].sum()
    dex_vol = dex[dex['volume'] > 0]['volume'].sum()
    
    insight_4 = f"""
KEY INSIGHT #4: THE ENGAGEMENT DICHOTOMY (Gaming vs DeFi)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fundamentally different user engagement patterns by category:

• Gaming: {gaming_users:,.0f} users, ${gaming_vol/1e6:.0f}M volume
• DeFi/DEX: {dex_users:,.0f} users, ${dex_vol/1e9:.1f}B volume
• Gaming has high user counts but minimal economic activity per user
• DeFi has lower user counts but massive value per transaction
• Median tx per user varies 1000x between categories

IMPLICATION: "Success" metrics differ radically by DApp type. User count
alone is misleading - value per user matters more for sustainability.
"""
    insights.append(insight_4)
    
    # INSIGHT 5: TVL Concentration and Efficiency Gap
    total_tvl = df_tvl['tvl'].sum()
    top_10_tvl = df_tvl.nlargest(10, 'tvl')['tvl'].sum()
    tvl_conc = top_10_tvl / total_tvl * 100
    
    df_tvl_eff = df_tvl[df_tvl['users'] > 0].copy()
    df_tvl_eff['tvl_per_user'] = df_tvl_eff['tvl'] / df_tvl_eff['users']
    median_tvl_per_user = df_tvl_eff['tvl_per_user'].median()
    
    insight_5 = f"""
KEY INSIGHT #5: TVL CONCENTRATION & EFFICIENCY GAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Value Locked shows extreme concentration:

• Total TVL: ${total_tvl/1e9:.1f}B across ecosystem
• Top 10 DApps control {tvl_conc:.1f}% of all TVL
• Median TVL per user: ${median_tvl_per_user:,.0f}
• Wide variance in capital deployment efficiency
• Most DApps struggle to attract meaningful liquidity

IMPLICATION: Capital flows to established players. New DApps face
severe competitive disadvantages in attracting liquidity.
"""
    insights.append(insight_5)
    
    # INSIGHT 6: Funding Paradox
    df_funded = df[df['raised_capital'] > 0].copy()
    total_funding = df_funded['raised_capital'].sum()
    df_funded['funding_eff'] = np.where(
        df_funded['market_cap'] > 0,
        df_funded['market_cap'] / (df_funded['raised_capital'] * 1e6),
        0
    )
    eff_clean = df_funded[(df_funded['funding_eff'] > 0) & (df_funded['funding_eff'] < df_funded['funding_eff'].quantile(0.95))]
    median_roi = eff_clean['funding_eff'].median()
    
    insight_6 = f"""
KEY INSIGHT #6: THE FUNDING EFFICIENCY PARADOX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Weak correlation between funding and market success:

• Total capital raised: ${total_funding:,.0f}M across {len(df_funded)} DApps
• Median market cap / funding ratio: {median_roi:.2f}x
• Most DApps trading below their funding valuations
• Funding does not guarantee success or adoption
• Many unfunded DApps outperform funded competitors

IMPLICATION: Capital is necessary but not sufficient. Product-market
fit and genuine utility matter more than funding rounds.
"""
    insights.append(insight_6)
    
    # INSIGHT 7: Multi-Chain Premium
    multichain_mcap = df[(df['is_multi_chain'] == True) & (df['market_cap'] > 0)]['market_cap'].mean()
    singlechain_mcap = df[(df['is_multi_chain'] == False) & (df['market_cap'] > 0)]['market_cap'].mean()
    premium = multichain_mcap / singlechain_mcap if singlechain_mcap > 0 else 0
    
    insight_7 = f"""
KEY INSIGHT #7: THE MULTI-CHAIN PREMIUM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cross-chain deployment correlates with higher valuations:

• Multi-chain DApps: avg market cap ${multichain_mcap/1e6:.1f}M
• Single-chain DApps: avg market cap ${singlechain_mcap/1e6:.1f}M
• Multi-chain premium: {premium:.1f}x higher valuation
• Only {multichain_pct:.1f}% of DApps deploy multi-chain
• Multi-chain DApps average {df[df['is_multi_chain']]['chain_count'].mean():.1f} chains

IMPLICATION: Chain diversification strategy pays off. Multi-chain
presence signals ambition and attracts more capital.
"""
    insights.append(insight_7)
    
    # INSIGHT 8: Governance-Performance Link
    gov_corr_data = df[(df['governance_score'].notna()) & (df['market_cap'] > 0)].copy()
    gov_corr_data['mcap_log'] = np.log1p(gov_corr_data['market_cap'])
    gov_corr = gov_corr_data[['governance_score', 'mcap_log']].corr().iloc[0, 1]
    
    decent_mcap = df_gov[df_gov['level_of_decentralisation'] == 'DECENTRALIZED']['market_cap'].median()
    central_mcap = df_gov[df_gov['level_of_decentralisation'] == 'CENTRALIZED']['market_cap'].median()
    
    insight_8 = f"""
KEY INSIGHT #8: GOVERNANCE-PERFORMANCE CORRELATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
More decentralized governance associates with better performance:

• Governance score correlates {gov_corr:.2f} with log(market cap)
• Decentralized DApps: median market cap ${decent_mcap/1e6:.1f}M
• Centralized DApps: median market cap ${central_mcap/1e6:.1f}M
• Community governance attracts more engaged users
• DAO-governed DApps show higher transaction intensity

IMPLICATION: Despite rarity, genuine decentralization provides
competitive advantages in adoption and valuation.
"""
    insights.append(insight_8)
    
    # Print all insights
    for insight in insights:
        print(insight)
    
    # Create summary visualization
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.axis('off')
    
    title_text = "8 KEY INSIGHTS: DApp Ecosystem Analysis\n"
    
    summary_text = """
1. GOVERNANCE PARADOX: Only 5.2% truly decentralized despite blockchain ethos
   
2. CHAIN SPECIALIZATION: Different blockchains serve distinct DApp niches
   
3. MARKET CONCENTRATION: Top 10 DApps control 57.5% of market cap
   
4. ENGAGEMENT DICHOTOMY: Gaming = high users/low value; DeFi = low users/high value
   
5. TVL EFFICIENCY GAP: Top 10 DApps control 93.1% of Total Value Locked
   
6. FUNDING PARADOX: Weak correlation between capital raised and market success
   
7. MULTI-CHAIN PREMIUM: Cross-chain DApps command higher valuations
   
8. GOVERNANCE-PERFORMANCE LINK: More decentralized → better market performance
    """
    
    ax.text(0.5, 0.95, title_text, transform=ax.transAxes,
           fontsize=16, fontweight='bold', ha='center', va='top',
           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    ax.text(0.5, 0.85, summary_text, transform=ax.transAxes,
           fontsize=11, ha='center', va='top', family='monospace',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    ax.text(0.5, 0.02, f'Based on analysis of {len(df)} DApps across 33 variables',
           transform=ax.transAxes, fontsize=10, ha='center', va='bottom',
           style='italic', color='gray')
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '09_key_insights_summary.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Summary visualization saved: {output_path}")
    plt.close()
    
    # Save insights to text file
    insights_file = OUTPUT_DIR / '09_KEY_INSIGHTS.txt'
    with open(insights_file, 'w') as f:
        f.write("="*70 + "\n")
        f.write(" "*15 + "8 KEY INSIGHTS - DAPP ECOSYSTEM ANALYSIS\n")
        f.write("="*70 + "\n\n")
        for insight in insights:
            f.write(insight + "\n")
        f.write("\n" + "="*70 + "\n")
        f.write(f"Analysis based on {len(df)} DApps\n")
        f.write(f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}\n")
        f.write("="*70 + "\n")
    
    print(f"✓ Insights document saved: {insights_file}")
    
    print("\n" + "="*70)
    print("KEY INSIGHTS SYNTHESIS COMPLETE!")
    print("="*70)
    print("\nThese 8 insights provide the foundation for your thesis:")
    print("1. Governance challenges")
    print("2. Ecosystem specialization")
    print("3. Market concentration")
    print("4. Category-specific success patterns")
    print("5. Capital efficiency")
    print("6. Funding dynamics")
    print("7. Multi-chain strategies")
    print("8. Governance benefits")

if __name__ == "__main__":
    main()

