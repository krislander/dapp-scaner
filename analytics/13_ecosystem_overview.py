"""
DApp Ecosystem Analysis - Ecosystem Overview & Presentation Charts
====================================================================
High-level, presentation-ready overview of the entire DApp ecosystem.
Designed to produce clean charts suitable for 5-10 slide presentations.

Outputs:
  - Ecosystem "at a glance" infographic
  - Category landscape map
  - Governance maturity spectrum
  - Token economy overview
  - Key numbers summary
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from collections import Counter
import warnings

from config import DATA_PATH, OUTPUT_DIR

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def load_prepared_data():
    df = pd.read_csv(DATA_PATH)
    print(f"✓ Loaded {len(df)} DApps with {len(df.columns)} columns")
    return df


# ─────────────────────────────────────────────────────────────────
def ecosystem_at_a_glance(df):
    """Single infographic with key ecosystem numbers."""
    print("\n" + "="*60)
    print("ECOSYSTEM AT A GLANCE")
    print("="*60)

    # Compute headline numbers
    total_dapps = len(df)
    total_users = df['users'].sum()
    total_mcap = df[df['market_cap'] > 0]['market_cap'].sum()
    total_tvl = df[df['tvl'] > 0]['tvl'].sum()
    total_volume = df[df['volume'] > 0]['volume'].sum()
    n_categories = df['dapp_category'].nunique()
    n_chains = len(set(c.strip() for chains in df['chains'].dropna()
                       for c in str(chains).split(',')))
    has_token_pct = df['has_token'].mean() * 100
    multichain_pct = df['is_multi_chain'].mean() * 100
    decent_pct = (df['level_of_decentralisation'] == 'DECENTRALIZED').mean() * 100

    stats = {
        'Total DApps': f'{total_dapps:,}',
        'Categories': str(n_categories),
        'Blockchains': str(n_chains),
        'Total Users': f'{total_users/1e6:.1f}M',
        'Total Market Cap': f'${total_mcap/1e9:.1f}B',
        'Total TVL': f'${total_tvl/1e9:.1f}B',
        'Total Volume': f'${total_volume/1e9:.1f}B',
        'Token Adoption': f'{has_token_pct:.0f}%',
        'Multi-Chain': f'{multichain_pct:.0f}%',
        'Truly Decentralized': f'{decent_pct:.0f}%',
    }

    for k, v in stats.items():
        print(f"  {k}: {v}")

    # Build infographic
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    ax.text(5, 5.6, 'DApp Ecosystem at a Glance', fontsize=22,
            fontweight='bold', ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#2c3e50',
                      edgecolor='none', alpha=0.9),
            color='white')

    positions = [
        (1.0, 4.2), (3.5, 4.2), (6.0, 4.2), (8.5, 4.2),
        (1.0, 2.6), (3.5, 2.6), (6.0, 2.6), (8.5, 2.6),
        (2.25, 1.0), (5.0, 1.0),
    ]
    stat_items = list(stats.items())
    bg_colors = ['#3498db', '#2ecc71', '#e67e22', '#9b59b6',
                 '#1abc9c', '#e74c3c', '#f39c12', '#2980b9',
                 '#16a085', '#c0392b']

    for i, ((label, value), (x, y)) in enumerate(zip(stat_items, positions)):
        ax.add_patch(plt.Rectangle((x - 0.9, y - 0.6), 1.8, 1.2,
                                    facecolor=bg_colors[i % len(bg_colors)],
                                    edgecolor='white', linewidth=2,
                                    alpha=0.85, zorder=2,
                                    transform=ax.transData))
        ax.text(x, y + 0.15, value, fontsize=18, fontweight='bold',
                ha='center', va='center', color='white', zorder=3)
        ax.text(x, y - 0.3, label, fontsize=9, ha='center', va='center',
                color='white', alpha=0.9, zorder=3)

    plt.tight_layout()
    out = OUTPUT_DIR / '13_ecosystem_at_a_glance.png'
    plt.savefig(out, dpi=300, bbox_inches='tight', facecolor='#ecf0f1')
    print(f"✓ Saved: {out}")
    plt.close()

    return stats


# ─────────────────────────────────────────────────────────────────
def category_landscape(df):
    """Bubble chart showing all categories by size, users, TVL."""
    print("\n" + "="*60)
    print("CATEGORY LANDSCAPE")
    print("="*60)

    cat_agg = df.groupby('dapp_category').agg(
        count=('name', 'count'),
        total_users=('users', 'sum'),
        total_mcap=('market_cap', 'sum'),
        total_tvl=('tvl', 'sum'),
        avg_gov_score=('governance_score', 'mean'),
        token_pct=('has_token', 'mean'),
    ).reset_index()

    print(cat_agg.sort_values('count', ascending=False).to_string(index=False))

    fig, ax = plt.subplots(figsize=(14, 9))

    # Bubble: x=count, y=total_tvl, size=total_mcap, color=avg_gov_score
    scatter = ax.scatter(
        cat_agg['count'],
        cat_agg['total_tvl'].clip(lower=1),
        s=np.sqrt(cat_agg['total_mcap'].clip(lower=1e5)) / 50,
        c=cat_agg['avg_gov_score'],
        cmap='RdYlGn', alpha=0.7, edgecolors='black', linewidth=0.5
    )
    ax.set_yscale('log')
    ax.set_xlabel('Number of DApps in Category', fontsize=12)
    ax.set_ylabel('Total TVL (USD, log scale)', fontsize=12)
    ax.set_title('DApp Category Landscape\n(bubble size = total market cap, '
                 'color = governance score)', fontsize=13, fontweight='bold')

    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Avg Governance Score', fontsize=10)

    # Annotate categories
    for _, row in cat_agg.iterrows():
        ax.annotate(row['dapp_category'],
                    (row['count'], max(row['total_tvl'], 1)),
                    fontsize=8, alpha=0.8, ha='center',
                    textcoords='offset points', xytext=(0, 8))

    plt.tight_layout()
    out = OUTPUT_DIR / '13_category_landscape.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {out}")
    plt.close()


# ─────────────────────────────────────────────────────────────────
def governance_maturity_spectrum(df):
    """Visualise the governance maturity of the entire ecosystem."""
    print("\n" + "="*60)
    print("GOVERNANCE MATURITY SPECTRUM")
    print("="*60)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Governance Maturity Spectrum', fontsize=14, fontweight='bold')

    # 1. Governance score histogram
    ax = axes[0]
    ax.hist(df['governance_score'].dropna(), bins=30, color='steelblue',
            edgecolor='black', alpha=0.7)
    ax.axvline(df['governance_score'].median(), color='red', linestyle='--',
               linewidth=2, label=f'Median: {df["governance_score"].median():.2f}')
    ax.set_xlabel('Governance Score (0=Centralized, 1=Decentralized)')
    ax.set_ylabel('Number of DApps')
    ax.set_title('Governance Score Distribution', fontsize=11, fontweight='bold')
    ax.legend()

    # 2. Decentralisation pie
    ax = axes[1]
    dec_counts = df['level_of_decentralisation'].value_counts()
    dec_colors = {'CENTRALIZED': '#d62728', 'SEMI_DECENTRALIZED': '#ff7f0e',
                  'DECENTRALIZED': '#2ca02c'}
    ax.pie(dec_counts.values, labels=dec_counts.index,
           autopct='%1.1f%%', startangle=90,
           colors=[dec_colors.get(d, '#999') for d in dec_counts.index])
    ax.set_title('Decentralisation Levels', fontsize=11, fontweight='bold')

    # 3. Ownership pie
    ax = axes[2]
    own_counts = df['ownership_status'].value_counts()
    ax.pie(own_counts.values, labels=own_counts.index,
           autopct='%1.1f%%', startangle=90)
    ax.set_title('Ownership Status', fontsize=11, fontweight='bold')

    plt.tight_layout()
    out = OUTPUT_DIR / '13_governance_maturity.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {out}")
    plt.close()


# ─────────────────────────────────────────────────────────────────
def token_economy_overview(df):
    """Overview of the token economy across the ecosystem."""
    print("\n" + "="*60)
    print("TOKEN ECONOMY OVERVIEW")
    print("="*60)

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Token Economy Overview', fontsize=14, fontweight='bold')

    # 1. Token adoption: has token vs no token, by category
    ax = axes[0, 0]
    top_cats = df['dapp_category'].value_counts().head(10).index
    token_by_cat = df[df['dapp_category'].isin(top_cats)].groupby('dapp_category').agg(
        with_token=('has_token', 'sum'),
        total=('has_token', 'count')
    )
    token_by_cat['without_token'] = token_by_cat['total'] - token_by_cat['with_token']
    token_by_cat[['with_token', 'without_token']].plot(
        kind='barh', stacked=True, ax=ax,
        color=['#2ecc71', '#e74c3c'])
    ax.set_xlabel('Number of DApps')
    ax.set_title('Token Adoption by Category', fontsize=11, fontweight='bold')
    ax.legend(['Has Token', 'No Token'], fontsize=9)

    # 2. Token type distribution (primary)
    ax = axes[0, 1]
    tt_counts = df[df['has_token']]['token_type_primary'].value_counts()
    colors = ['#2ecc71', '#e67e22', '#3498db', '#e74c3c', '#9b59b6']
    tt_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90,
                   colors=colors[:len(tt_counts)])
    ax.set_ylabel('')
    ax.set_title('Token Type Distribution (DApps with tokens)', fontsize=11, fontweight='bold')

    # 3. Governance token vs actual governance
    ax = axes[1, 0]
    gov_tok = df[df['is_governance_token']].copy()
    if len(gov_tok) > 0:
        gov_type_in_gov_tok = gov_tok['governance_type'].value_counts()
        gov_type_in_gov_tok.plot(kind='barh', ax=ax, color='coral', edgecolor='black')
        ax.set_xlabel('Count')
        ax.set_title('Governance Type Among DApps WITH Governance Tokens',
                      fontsize=11, fontweight='bold')

    # 4. Token type vs governance score
    ax = axes[1, 1]
    tt_gov = df[df['has_token']].groupby('token_type_primary')['governance_score'].agg(
        ['mean', 'median', 'count'])
    tt_gov = tt_gov.sort_values('mean', ascending=True)
    colors_bar = ['#3498db'] * len(tt_gov)
    ax.barh(range(len(tt_gov)), tt_gov['mean'], color=colors_bar, edgecolor='black')
    ax.set_yticks(range(len(tt_gov)))
    ax.set_yticklabels(tt_gov.index)
    ax.set_xlabel('Average Governance Score')
    ax.set_title('Governance Score by Token Type', fontsize=11, fontweight='bold')
    for i, (idx, row) in enumerate(tt_gov.iterrows()):
        ax.text(row['mean'] + 0.005, i, f'{row["mean"]:.2f} (n={int(row["count"])})',
                va='center', fontsize=9)

    plt.tight_layout()
    out = OUTPUT_DIR / '13_token_economy_overview.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {out}")
    plt.close()


# ─────────────────────────────────────────────────────────────────
def sector_overview_chart(df):
    """High-level sector composition chart for presentation."""
    print("\n" + "="*60)
    print("SECTOR COMPOSITION OVERVIEW")
    print("="*60)

    sectors = {
        'DeFi': df['is_defi'].sum(),
        'Gaming': df['is_gaming'].sum(),
        'Social': df['is_social'].sum(),
        'Prediction Markets': df['is_prediction_market'].sum(),
        'RWA / Payments': df['is_rwa'].sum(),
        'AI': df['is_ai'].sum(),
        'DePIN': df['is_depin'].sum(),
    }
    # Add "Other" for uncategorised
    identified = sum(sectors.values())
    sectors['Other'] = len(df) - identified if identified < len(df) else 0

    # Remove zero sectors
    sectors = {k: v for k, v in sectors.items() if v > 0}

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('DApp Ecosystem Sector Composition', fontsize=14, fontweight='bold')

    # Pie chart
    ax = axes[0]
    sect_colors = ['#3498db', '#2ecc71', '#9b59b6', '#e67e22',
                   '#1abc9c', '#e74c3c', '#f39c12', '#95a5a6']
    ax.pie(sectors.values(), labels=sectors.keys(), autopct='%1.1f%%',
           startangle=90, colors=sect_colors[:len(sectors)])
    ax.set_title('Sector Distribution', fontsize=12, fontweight='bold')

    # Bar chart with counts
    ax = axes[1]
    sorted_sectors = dict(sorted(sectors.items(), key=lambda x: x[1], reverse=True))
    ax.barh(list(sorted_sectors.keys()), list(sorted_sectors.values()),
            color=sect_colors[:len(sorted_sectors)], edgecolor='black')
    ax.set_xlabel('Number of DApps')
    ax.set_title('DApps per Sector', fontsize=12, fontweight='bold')
    ax.invert_yaxis()
    for i, (k, v) in enumerate(sorted_sectors.items()):
        ax.text(v + 2, i, str(v), va='center', fontsize=10)

    plt.tight_layout()
    out = OUTPUT_DIR / '13_sector_composition.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {out}")
    plt.close()


# ─────────────────────────────────────────────────────────────────
def key_numbers_for_presentation(df):
    """Generate a clean text summary of key numbers for slides."""
    print("\n" + "="*60)
    print("KEY NUMBERS FOR PRESENTATION")
    print("="*60)

    lines = []
    lines.append("KEY NUMBERS – DApp Ecosystem Analysis")
    lines.append("=" * 50)

    lines.append(f"\nDataset: {len(df)} DApps")
    lines.append(f"Categories: {df['dapp_category'].nunique()}")
    n_chains = len(set(c.strip() for chains in df['chains'].dropna()
                       for c in str(chains).split(',')))
    lines.append(f"Blockchains: {n_chains}")

    lines.append(f"\n--- MARKET ---")
    lines.append(f"Total Market Cap: ${df[df['market_cap']>0]['market_cap'].sum()/1e9:.1f}B")
    lines.append(f"Total TVL: ${df[df['tvl']>0]['tvl'].sum()/1e9:.1f}B")
    lines.append(f"Total Users: {df['users'].sum()/1e6:.1f}M")

    lines.append(f"\n--- GOVERNANCE ---")
    dec = df['level_of_decentralisation'].value_counts(normalize=True) * 100
    for level in ['DECENTRALIZED', 'SEMI_DECENTRALIZED', 'CENTRALIZED']:
        if level in dec.index:
            lines.append(f"{level}: {dec[level]:.1f}%")

    lines.append(f"\n--- TOKENS ---")
    lines.append(f"DApps with tokens: {df['has_token'].sum()} ({df['has_token'].mean()*100:.1f}%)")
    tt = df[df['has_token']]['token_type_primary'].value_counts()
    for t, c in tt.items():
        lines.append(f"  {t}: {c}")

    lines.append(f"\n--- SECTORS ---")
    for label, col in [('DeFi', 'is_defi'), ('Gaming', 'is_gaming'),
                        ('Social', 'is_social'),
                        ('Prediction Markets', 'is_prediction_market'),
                        ('RWA', 'is_rwa'), ('AI', 'is_ai'),
                        ('DePIN', 'is_depin')]:
        lines.append(f"  {label}: {df[col].sum()} DApps")

    lines.append(f"\n--- CONCENTRATION ---")
    df_mkt = df[df['market_cap'] > 0].sort_values('market_cap', ascending=False)
    top10_pct = df_mkt.head(10)['market_cap'].sum() / df_mkt['market_cap'].sum() * 100
    lines.append(f"Top 10 DApps control {top10_pct:.1f}% of market cap")

    df_tvl = df[df['tvl'] > 0].sort_values('tvl', ascending=False)
    tvl10_pct = df_tvl.head(10)['tvl'].sum() / df_tvl['tvl'].sum() * 100
    lines.append(f"Top 10 DApps control {tvl10_pct:.1f}% of TVL")

    text = '\n'.join(lines)
    print(text)

    out = OUTPUT_DIR / '13_KEY_NUMBERS.txt'
    with open(out, 'w') as f:
        f.write(text)
        f.write(f"\n\nDate: {pd.Timestamp.now().strftime('%Y-%m-%d')}\n")
    print(f"\n✓ Saved: {out}")


def main():
    print("\n" + "="*60)
    print("ECOSYSTEM OVERVIEW & PRESENTATION CHARTS")
    print("="*60)

    df = load_prepared_data()

    stats = ecosystem_at_a_glance(df)
    category_landscape(df)
    governance_maturity_spectrum(df)
    token_economy_overview(df)
    sector_overview_chart(df)
    key_numbers_for_presentation(df)

    print("\n" + "="*60)
    print("ECOSYSTEM OVERVIEW COMPLETE!")
    print("="*60)
    print("✓ All outputs saved to:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
