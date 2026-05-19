"""
DApp Ecosystem Analysis - Token Type Analysis
===============================================
Analyzes the token_type enum across the ecosystem: distribution,
cross-tabulation with governance/ownership/decentralisation,
market performance by token type, and category patterns.
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

TOKEN_TYPE_COLORS = {
    'UTILITY': '#2ecc71',
    'REWARD': '#e67e22',
    'GOVERNANCE': '#3498db',
    'SPECULATIVE': '#e74c3c',
    'SOCIAL': '#9b59b6',
    'NONE': '#95a5a6',
}

def load_prepared_data():
    df = pd.read_csv(DATA_PATH)
    print(f"✓ Loaded {len(df)} DApps with {len(df.columns)} columns")
    return df


def analyze_token_type_distribution(df):
    """Distribution of token types and multi-type tokens."""
    print("\n" + "="*60)
    print("TOKEN TYPE DISTRIBUTION")
    print("="*60)

    primary_counts = df['token_type_primary'].value_counts()
    full_counts = df['token_type_clean'].value_counts()

    print("\nPrimary token type:")
    print(primary_counts)
    print(f"\nMulti-type tokens: {df['is_multi_type_token'].sum()} "
          f"({df['is_multi_type_token'].mean()*100:.1f}%)")

    # Boolean flag breakdown
    for flag, label in [('is_governance_token', 'Governance'),
                        ('is_utility_token', 'Utility'),
                        ('is_reward_token', 'Reward'),
                        ('is_speculative_token', 'Speculative'),
                        ('is_social_token', 'Social')]:
        count = df[flag].sum()
        print(f"  {label} tokens: {count} ({count/len(df)*100:.1f}%)")

    # ── Visualisation ──
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Token Type Distribution Analysis', fontsize=14, fontweight='bold')

    # 1. Primary token type bar
    ax1 = axes[0, 0]
    colors = [TOKEN_TYPE_COLORS.get(t, '#7f8c8d') for t in primary_counts.index]
    primary_counts.plot(kind='barh', ax=ax1, color=colors, edgecolor='black')
    ax1.set_title('Primary Token Type Distribution', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Number of DApps')
    for i, v in enumerate(primary_counts.values):
        ax1.text(v + 3, i, f'{v} ({v/len(df)*100:.1f}%)', va='center', fontsize=9)

    # 2. Full token type (top 8)
    ax2 = axes[0, 1]
    top_full = full_counts.head(8)
    top_full.plot(kind='barh', ax=ax2, color='steelblue', edgecolor='black')
    ax2.set_title('Full Token Type Combinations', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Number of DApps')
    ax2.invert_yaxis()
    for i, v in enumerate(top_full.values):
        ax2.text(v + 1, i, str(v), va='center', fontsize=9)

    # 3. Token type flag presence (stacked)
    ax3 = axes[1, 0]
    flags = ['is_governance_token', 'is_utility_token', 'is_reward_token',
             'is_speculative_token', 'is_social_token']
    flag_labels = ['Governance', 'Utility', 'Reward', 'Speculative', 'Social']
    flag_counts = [df[f].sum() for f in flags]
    flag_colors = [TOKEN_TYPE_COLORS[l.upper()] for l in flag_labels]
    ax3.barh(flag_labels, flag_counts, color=flag_colors, edgecolor='black')
    ax3.set_title('Token Type Flag Presence\n(includes multi-type overlap)',
                  fontsize=12, fontweight='bold')
    ax3.set_xlabel('Number of DApps')
    for i, v in enumerate(flag_counts):
        ax3.text(v + 2, i, str(v), va='center', fontsize=9)

    # 4. Pie chart – tokens vs no tokens, with type breakdown
    ax4 = axes[1, 1]
    has_token = df['has_token'].sum()
    no_token = len(df) - has_token
    type_dist = df[df['has_token']]['token_type_primary'].value_counts()
    pie_labels = list(type_dist.index) + ['No Token']
    pie_values = list(type_dist.values) + [no_token]
    pie_colors = [TOKEN_TYPE_COLORS.get(l, '#7f8c8d') for l in pie_labels]
    ax4.pie(pie_values, labels=pie_labels, autopct='%1.1f%%', startangle=90,
            colors=pie_colors)
    ax4.set_title('Token Presence & Type Breakdown', fontsize=12, fontweight='bold')

    plt.tight_layout()
    out = OUTPUT_DIR / '10_token_type_distribution.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {out}")
    plt.close()


def analyze_token_type_governance_cross(df):
    """Cross-tabulation of token_type with governance dimensions."""
    print("\n" + "="*60)
    print("TOKEN TYPE × GOVERNANCE CROSS-TABULATION")
    print("="*60)

    df_clean = df[df['token_type_primary'] != 'NONE'].dropna(
        subset=['governance_type', 'ownership_status', 'level_of_decentralisation'])

    print(f"Analyzing {len(df_clean)} DApps with both token type and governance data")

    # Cross-tabs
    ct_gov = pd.crosstab(df_clean['token_type_primary'],
                         df_clean['governance_type'], normalize='index') * 100
    ct_own = pd.crosstab(df_clean['token_type_primary'],
                         df_clean['ownership_status'], normalize='index') * 100
    ct_dec = pd.crosstab(df_clean['token_type_primary'],
                         df_clean['level_of_decentralisation'], normalize='index') * 100

    print("\nToken Type vs Governance (%):")
    print(ct_gov.round(1))
    print("\nToken Type vs Decentralisation (%):")
    print(ct_dec.round(1))

    fig, axes = plt.subplots(1, 3, figsize=(22, 7))
    fig.suptitle('Token Type × Governance Dimensions', fontsize=14, fontweight='bold')

    sns.heatmap(ct_gov, annot=True, fmt='.1f', cmap='YlOrRd', ax=axes[0],
                cbar_kws={'label': '%'})
    axes[0].set_title('Token Type vs Governance Type', fontsize=11, fontweight='bold')
    plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=45, ha='right')

    sns.heatmap(ct_own, annot=True, fmt='.1f', cmap='YlGnBu', ax=axes[1],
                cbar_kws={'label': '%'})
    axes[1].set_title('Token Type vs Ownership Status', fontsize=11, fontweight='bold')
    plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45, ha='right')

    dec_order = ['CENTRALIZED', 'SEMI_DECENTRALIZED', 'DECENTRALIZED']
    dec_cols = [c for c in dec_order if c in ct_dec.columns]
    sns.heatmap(ct_dec[dec_cols], annot=True, fmt='.1f', cmap='RdYlGn', ax=axes[2],
                cbar_kws={'label': '%'})
    axes[2].set_title('Token Type vs Decentralisation', fontsize=11, fontweight='bold')

    plt.tight_layout()
    out = OUTPUT_DIR / '10_token_type_governance.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {out}")
    plt.close()


def analyze_token_type_market_performance(df):
    """Market performance metrics broken down by token type."""
    print("\n" + "="*60)
    print("TOKEN TYPE MARKET PERFORMANCE")
    print("="*60)

    df_market = df[(df['has_token']) & (df['market_cap'] > 0)].copy()
    print(f"Analyzing {len(df_market)} DApps with token & market cap")

    metrics = df_market.groupby('token_type_primary').agg({
        'market_cap': ['mean', 'median', 'count'],
        'users': 'median',
        'tvl': 'median',
        'volume': 'median',
        'volatility_index': 'median',
        'governance_score': 'mean',
    })
    print("\nMarket metrics by token type:")
    print(metrics)

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Market Performance by Token Type', fontsize=14, fontweight='bold')

    types = df_market['token_type_primary'].unique()
    type_order = ['GOVERNANCE', 'UTILITY', 'REWARD', 'SPECULATIVE', 'SOCIAL']
    type_order = [t for t in type_order if t in types]

    # 1. Market cap boxplot
    ax1 = axes[0, 0]
    data_boxes = [df_market[df_market['token_type_primary'] == t]['market_cap'].values
                  for t in type_order]
    bp = ax1.boxplot(data_boxes, labels=type_order, patch_artist=True, vert=True)
    for patch, tt in zip(bp['boxes'], type_order):
        patch.set_facecolor(TOKEN_TYPE_COLORS.get(tt, '#7f8c8d'))
    ax1.set_yscale('log')
    ax1.set_ylabel('Market Cap (USD, log)', fontsize=10)
    ax1.set_title('Market Cap Distribution by Token Type', fontsize=11, fontweight='bold')
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30, ha='right')

    # 2. Users boxplot
    ax2 = axes[0, 1]
    df_users = df_market[df_market['users'] > 0]
    data_users = [df_users[df_users['token_type_primary'] == t]['users'].values
                  for t in type_order]
    bp2 = ax2.boxplot(data_users, labels=type_order, patch_artist=True, vert=True)
    for patch, tt in zip(bp2['boxes'], type_order):
        patch.set_facecolor(TOKEN_TYPE_COLORS.get(tt, '#7f8c8d'))
    ax2.set_yscale('log')
    ax2.set_ylabel('Active Users (log)', fontsize=10)
    ax2.set_title('User Base by Token Type', fontsize=11, fontweight='bold')
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=30, ha='right')

    # 3. Median metrics comparison (grouped bar)
    ax3 = axes[1, 0]
    compare_metrics = ['market_cap', 'tvl', 'volume']
    medians = df_market.groupby('token_type_primary')[compare_metrics].median()
    medians = medians.loc[[t for t in type_order if t in medians.index]]
    medians_norm = medians.div(medians.max())
    x = np.arange(len(medians))
    width = 0.25
    for i, col in enumerate(compare_metrics):
        ax3.bar(x + i * width, medians_norm[col], width, label=col.replace('_', ' ').title())
    ax3.set_xticks(x + width)
    ax3.set_xticklabels(medians.index, rotation=30, ha='right')
    ax3.set_ylabel('Normalised Median Value', fontsize=10)
    ax3.set_title('Relative Market Metrics by Token Type', fontsize=11, fontweight='bold')
    ax3.legend(fontsize=9)

    # 4. Volatility by token type
    ax4 = axes[1, 1]
    vol_by_type = df_market.groupby('token_type_primary')['volatility_index'].median()
    vol_by_type = vol_by_type.loc[[t for t in type_order if t in vol_by_type.index]]
    bar_colors = [TOKEN_TYPE_COLORS.get(t, '#7f8c8d') for t in vol_by_type.index]
    ax4.bar(range(len(vol_by_type)), vol_by_type.values, color=bar_colors, edgecolor='black')
    ax4.set_xticks(range(len(vol_by_type)))
    ax4.set_xticklabels(vol_by_type.index, rotation=30, ha='right')
    ax4.set_ylabel('Median Volatility Index', fontsize=10)
    ax4.set_title('Price Volatility by Token Type', fontsize=11, fontweight='bold')

    plt.tight_layout()
    out = OUTPUT_DIR / '10_token_type_market.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {out}")
    plt.close()


def analyze_token_type_by_category(df):
    """Token type distribution across DApp categories."""
    print("\n" + "="*60)
    print("TOKEN TYPE BY CATEGORY")
    print("="*60)

    df_tok = df[df['has_token']].copy()
    top_cats = df_tok['dapp_category'].value_counts().head(10).index
    df_top = df_tok[df_tok['dapp_category'].isin(top_cats)]

    ct = pd.crosstab(df_top['dapp_category'], df_top['token_type_primary'],
                     normalize='index') * 100
    print("\nToken type % by category:")
    print(ct.round(1))

    fig, axes = plt.subplots(1, 2, figsize=(18, 7))
    fig.suptitle('Token Type Patterns by DApp Category', fontsize=14, fontweight='bold')

    # 1. Stacked bar
    ax1 = axes[0]
    type_cols = [c for c in ['GOVERNANCE', 'UTILITY', 'REWARD', 'SPECULATIVE', 'SOCIAL']
                 if c in ct.columns]
    ct_plot = ct[type_cols].sort_values(type_cols[0], ascending=True)
    ct_plot.plot(kind='barh', stacked=True, ax=ax1,
                 color=[TOKEN_TYPE_COLORS[c] for c in type_cols])
    ax1.set_xlabel('Percentage (%)', fontsize=10)
    ax1.set_title('Token Type Mix by Category', fontsize=12, fontweight='bold')
    ax1.legend(title='Token Type', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)

    # 2. Governance token prevalence by category
    ax2 = axes[1]
    gov_pct = df_top.groupby('dapp_category')['is_governance_token'].mean() * 100
    gov_pct = gov_pct.sort_values(ascending=True)
    colors = plt.cm.RdYlGn(gov_pct.values / gov_pct.max())
    ax2.barh(range(len(gov_pct)), gov_pct.values, color=colors, edgecolor='black')
    ax2.set_yticks(range(len(gov_pct)))
    ax2.set_yticklabels(gov_pct.index, fontsize=9)
    ax2.set_xlabel('Governance Token Adoption (%)', fontsize=10)
    ax2.set_title('Governance Token Prevalence by Category', fontsize=12, fontweight='bold')
    for i, v in enumerate(gov_pct.values):
        ax2.text(v + 0.5, i, f'{v:.1f}%', va='center', fontsize=9)

    plt.tight_layout()
    out = OUTPUT_DIR / '10_token_type_by_category.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {out}")
    plt.close()


def generate_token_type_insights(df):
    """Key insights about token types."""
    print("\n" + "="*60)
    print("KEY TOKEN TYPE INSIGHTS")
    print("="*60)

    primary = df['token_type_primary'].value_counts()
    dominant = primary.index[0] if primary.index[0] != 'NONE' else primary.index[1]
    dominant_pct = primary[dominant] / len(df) * 100

    gov_tokens = df['is_governance_token'].sum()
    gov_pct = gov_tokens / len(df) * 100

    # Governance tokens vs actual decentralisation
    gov_decent = df[df['is_governance_token']]
    gov_truly_decent = (gov_decent['level_of_decentralisation'] == 'DECENTRALIZED').mean() * 100

    # Market cap comparison
    df_mkt = df[df['market_cap'] > 0]
    gov_mcap = df_mkt[df_mkt['is_governance_token']]['market_cap'].median()
    util_mcap = df_mkt[df_mkt['is_utility_token']]['market_cap'].median()
    spec_mcap = df_mkt[df_mkt['is_speculative_token']]['market_cap'].median()

    print(f"\n1. DOMINANT TOKEN TYPE: {dominant} ({dominant_pct:.1f}%)")
    print(f"2. GOVERNANCE TOKENS: {gov_tokens} ({gov_pct:.1f}%)")
    print(f"   - Of those, only {gov_truly_decent:.1f}% are truly decentralized")
    print(f"3. MEDIAN MARKET CAP BY TYPE:")
    print(f"   Governance: ${gov_mcap:,.0f}")
    print(f"   Utility: ${util_mcap:,.0f}")
    if spec_mcap > 0:
        print(f"   Speculative: ${spec_mcap:,.0f}")

    return {
        'dominant_token_type': dominant,
        'governance_token_pct': gov_pct,
        'gov_token_truly_decentralized_pct': gov_truly_decent,
    }


def main():
    print("\n" + "="*60)
    print("TOKEN TYPE ANALYSIS")
    print("="*60)

    df = load_prepared_data()

    analyze_token_type_distribution(df)
    analyze_token_type_governance_cross(df)
    analyze_token_type_market_performance(df)
    analyze_token_type_by_category(df)
    insights = generate_token_type_insights(df)

    print("\n" + "="*60)
    print("TOKEN TYPE ANALYSIS COMPLETE!")
    print("="*60)
    print("✓ All visualizations saved to:", OUTPUT_DIR)
    return insights


if __name__ == "__main__":
    insights = main()
