"""
DApp Ecosystem Analysis - Comparative Category Analysis
========================================================
This script provides comprehensive comparison across DApp categories.

Key Message Target: "Category-specific success patterns" - what works 
in gaming doesn't work in DeFi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

from config import DATA_PATH, OUTPUT_DIR

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def main():
    print("\n" + "="*60)
    print("COMPARATIVE CATEGORY ANALYSIS")
    print("="*60)
    
    df = pd.read_csv(DATA_PATH)
    print(f"✓ Loaded {len(df)} DApps")
    
    # Focus on top categories
    top_cats = df['dapp_category'].value_counts().head(6).index
    df_top = df[df['dapp_category'].isin(top_cats)].copy()
    
    print(f"\nComparing {len(top_cats)} major categories with {len(df_top)} DApps...")
    
    # Aggregate metrics by category
    cat_summary = df_top.groupby('dapp_category').agg({
        'users': ['sum', 'mean', 'median'],
        'market_cap': ['sum', 'mean', 'median'],
        'tvl': ['sum', 'mean', 'median'],
        'volume': ['sum', 'mean', 'median'],
        'transactions': ['sum', 'mean', 'median'],
        'governance_score': ['mean', 'median'],
        'is_multi_chain': 'mean',
        'has_token': 'mean',
        'tx_per_user': 'median',
        'volume_per_user': 'median'
    })
    
    print(f"\nCategory Summary:")
    print(cat_summary)
    
    # Visualize comprehensive comparison
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    fig.suptitle('Comprehensive Category Comparison', fontsize=14, fontweight='bold')
    
    # Plot 1: Total users by category
    ax1 = fig.add_subplot(gs[0, 0])
    user_totals = df_top.groupby('dapp_category')['users'].sum().sort_values(ascending=False)
    colors = plt.cm.Set3(np.linspace(0, 1, len(user_totals)))
    ax1.bar(range(len(user_totals)), user_totals.values, color=colors, edgecolor='black')
    ax1.set_xticks(range(len(user_totals)))
    ax1.set_xticklabels(user_totals.index, rotation=45, ha='right', fontsize=8)
    ax1.set_ylabel('Total Users', fontsize=9)
    ax1.set_title('Total User Base', fontsize=10, fontweight='bold')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
    
    # Plot 2: Total market cap by category
    ax2 = fig.add_subplot(gs[0, 1])
    mcap_totals = df_top[df_top['market_cap'] > 0].groupby('dapp_category')['market_cap'].sum().sort_values(ascending=False)
    ax2.bar(range(len(mcap_totals)), mcap_totals.values, color=colors[:len(mcap_totals)], edgecolor='black')
    ax2.set_xticks(range(len(mcap_totals)))
    ax2.set_xticklabels(mcap_totals.index, rotation=45, ha='right', fontsize=8)
    ax2.set_ylabel('Total Market Cap', fontsize=9)
    ax2.set_title('Total Market Cap', fontsize=10, fontweight='bold')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e9:.1f}B'))
    
    # Plot 3: Total volume by category
    ax3 = fig.add_subplot(gs[0, 2])
    vol_totals = df_top[df_top['volume'] > 0].groupby('dapp_category')['volume'].sum().sort_values(ascending=False)
    ax3.bar(range(len(vol_totals)), vol_totals.values, color=colors[:len(vol_totals)], edgecolor='black')
    ax3.set_xticks(range(len(vol_totals)))
    ax3.set_xticklabels(vol_totals.index, rotation=45, ha='right', fontsize=8)
    ax3.set_ylabel('Total Volume', fontsize=9)
    ax3.set_title('Total Trading Volume', fontsize=10, fontweight='bold')
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e9:.1f}B'))
    
    # Plot 4: Governance score by category
    ax4 = fig.add_subplot(gs[1, 0])
    gov_scores = df_top.groupby('dapp_category')['governance_score'].mean().sort_values(ascending=False)
    colors_gov = plt.cm.RdYlGn(gov_scores.values)
    ax4.barh(range(len(gov_scores)), gov_scores.values, color=colors_gov, edgecolor='black')
    ax4.set_yticks(range(len(gov_scores)))
    ax4.set_yticklabels(gov_scores.index, fontsize=8)
    ax4.set_xlabel('Avg Governance Score', fontsize=9)
    ax4.set_title('Governance by Category', fontsize=10, fontweight='bold')
    ax4.invert_yaxis()
    
    # Plot 5: Multi-chain adoption by category
    ax5 = fig.add_subplot(gs[1, 1])
    multichain_pct = df_top.groupby('dapp_category')['is_multi_chain'].mean() * 100
    multichain_pct = multichain_pct.sort_values(ascending=False)
    ax5.barh(range(len(multichain_pct)), multichain_pct.values, color=colors[:len(multichain_pct)], edgecolor='black')
    ax5.set_yticks(range(len(multichain_pct)))
    ax5.set_yticklabels(multichain_pct.index, fontsize=8)
    ax5.set_xlabel('Multi-Chain Adoption (%)', fontsize=9)
    ax5.set_title('Multi-Chain Strategy', fontsize=10, fontweight='bold')
    ax5.invert_yaxis()
    
    # Plot 6: Token adoption by category
    ax6 = fig.add_subplot(gs[1, 2])
    token_pct = df_top.groupby('dapp_category')['has_token'].mean() * 100
    token_pct = token_pct.sort_values(ascending=False)
    ax6.barh(range(len(token_pct)), token_pct.values, color=colors[:len(token_pct)], edgecolor='black')
    ax6.set_yticks(range(len(token_pct)))
    ax6.set_yticklabels(token_pct.index, fontsize=8)
    ax6.set_xlabel('Token Adoption (%)', fontsize=9)
    ax6.set_title('Tokenization Rate', fontsize=10, fontweight='bold')
    ax6.invert_yaxis()
    
    # Plot 7: Median tx per user by category
    ax7 = fig.add_subplot(gs[2, 0])
    tx_per_user = df_top[df_top['tx_per_user'] > 0].groupby('dapp_category')['tx_per_user'].median()
    tx_per_user = tx_per_user.sort_values(ascending=False)
    ax7.barh(range(len(tx_per_user)), tx_per_user.values, color=colors[:len(tx_per_user)], edgecolor='black')
    ax7.set_yticks(range(len(tx_per_user)))
    ax7.set_yticklabels(tx_per_user.index, fontsize=8)
    ax7.set_xlabel('Median Tx per User', fontsize=9)
    ax7.set_title('Engagement Intensity', fontsize=10, fontweight='bold')
    ax7.invert_yaxis()
    ax7.set_xscale('log')
    
    # Plot 8: Median volume per user by category
    ax8 = fig.add_subplot(gs[2, 1])
    vol_per_user = df_top[df_top['volume_per_user'] > 0].groupby('dapp_category')['volume_per_user'].median()
    vol_per_user = vol_per_user.sort_values(ascending=False)
    ax8.barh(range(len(vol_per_user)), vol_per_user.values, color=colors[:len(vol_per_user)], edgecolor='black')
    ax8.set_yticks(range(len(vol_per_user)))
    ax8.set_yticklabels(vol_per_user.index, fontsize=8)
    ax8.set_xlabel('Median Volume per User ($)', fontsize=9)
    ax8.set_title('Economic Value per User', fontsize=10, fontweight='bold')
    ax8.invert_yaxis()
    ax8.set_xscale('log')
    
    # Plot 9: Category radar/spider chart placeholder - show DApp count
    ax9 = fig.add_subplot(gs[2, 2])
    dapp_counts = df_top['dapp_category'].value_counts()
    ax9.pie(dapp_counts.values, labels=dapp_counts.index, autopct='%1.0f%%',
           colors=colors[:len(dapp_counts)], startangle=90)
    ax9.set_title('DApp Distribution', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '08_category_comparison.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()
    
    # ── Additional: Token type breakdown by category ──
    fig2, axes2 = plt.subplots(1, 2, figsize=(16, 7))
    fig2.suptitle('Token Type & Sector Flags by Category', fontsize=14, fontweight='bold')

    # Token type stacked bar per category
    ax = axes2[0]
    df_tok = df_top[df_top['has_token']].copy()
    if 'token_type_primary' in df_tok.columns and len(df_tok) > 0:
        ct = pd.crosstab(df_tok['dapp_category'], df_tok['token_type_primary'],
                         normalize='index') * 100
        type_cols = [c for c in ['GOVERNANCE', 'UTILITY', 'REWARD', 'SPECULATIVE', 'SOCIAL']
                     if c in ct.columns]
        ct[type_cols].plot(kind='barh', stacked=True, ax=ax)
        ax.set_xlabel('Percentage (%)')
        ax.set_title('Token Type Distribution by Category', fontsize=11, fontweight='bold')
        ax.legend(title='Token Type', fontsize=8, bbox_to_anchor=(1.05, 1))

    # Governance token adoption rate by category
    ax = axes2[1]
    if 'is_governance_token' in df_top.columns:
        gov_rate = df_top.groupby('dapp_category')['is_governance_token'].mean() * 100
        gov_rate = gov_rate.sort_values(ascending=True)
        gov_rate.plot(kind='barh', ax=ax, color='coral', edgecolor='black')
        ax.set_xlabel('Governance Token Adoption (%)')
        ax.set_title('Governance Token Rate by Category', fontsize=11, fontweight='bold')
        for i, v in enumerate(gov_rate.values):
            ax.text(v + 0.5, i, f'{v:.1f}%', va='center', fontsize=9)

    plt.tight_layout()
    output_path2 = OUTPUT_DIR / '08_category_token_type.png'
    plt.savefig(output_path2, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path2}")
    plt.close()

    # Key category insights
    print("\n" + "="*60)
    print("KEY CATEGORY INSIGHTS")
    print("="*60)
    
    print(f"\n1. USER LEADERS:")
    user_leaders = df_top.groupby('dapp_category')['users'].sum().sort_values(ascending=False).head(3)
    for i, (cat, users) in enumerate(user_leaders.items(), 1):
        print(f"   {i}. {cat}: {users:,.0f} users")
    
    print(f"\n2. VALUE LEADERS:")
    mcap_leaders = df_top[df_top['market_cap'] > 0].groupby('dapp_category')['market_cap'].sum().sort_values(ascending=False).head(3)
    for i, (cat, mcap) in enumerate(mcap_leaders.items(), 1):
        print(f"   {i}. {cat}: ${mcap:,.0f}")
    
    print(f"\n3. GOVERNANCE LEADERS:")
    gov_leaders = df_top.groupby('dapp_category')['governance_score'].mean().sort_values(ascending=False).head(3)
    for i, (cat, score) in enumerate(gov_leaders.items(), 1):
        print(f"   {i}. {cat}: {score:.2f}")
    
    print("\n" + "="*60)
    print("CATEGORY ANALYSIS COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    main()

