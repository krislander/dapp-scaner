"""
DApp Ecosystem Analysis - Sector Deep Dives
=============================================
Deep-dive analysis of specific DApp sectors per supervisor meeting notes:
  1. DeFi ecosystem (DEX, Lending, Derivatives, Yield Aggregators)
  2. Prediction Markets
  3. RWA (Real World Assets / Payments)
  4. AI DApps
  5. Gaming ecosystem overview

Each sector gets its own dashboard with governance, token type, market,
and performance metrics.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
# Generic sector dashboard builder
# ─────────────────────────────────────────────────────────────────
def _sector_dashboard(df_sector, sector_name, filename, df_full):
    """Build a 3×2 dashboard for a given sector subset."""
    n = len(df_sector)
    if n < 3:
        print(f"  ⚠ Only {n} DApps in {sector_name} – skipping dashboard")
        return

    print(f"\n{'='*60}")
    print(f"  {sector_name.upper()} DEEP DIVE  ({n} DApps)")
    print(f"{'='*60}")

    fig, axes = plt.subplots(3, 2, figsize=(16, 18))
    fig.suptitle(f'{sector_name} Sector Deep Dive  (n={n})',
                 fontsize=15, fontweight='bold')

    # ── 1. Top DApps by market cap ──
    ax = axes[0, 0]
    df_mcap = df_sector[df_sector['market_cap'] > 0].nlargest(10, 'market_cap')
    if len(df_mcap) > 0:
        colors = plt.cm.viridis(np.linspace(0, 1, len(df_mcap)))
        ax.barh(range(len(df_mcap)), df_mcap['market_cap'], color=colors)
        ax.set_yticks(range(len(df_mcap)))
        ax.set_yticklabels(df_mcap['name'], fontsize=8)
        ax.set_xlabel('Market Cap (USD)')
        ax.invert_yaxis()
        ax.xaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, _: f'${x/1e6:.0f}M' if x < 1e9 else f'${x/1e9:.1f}B'))
    ax.set_title(f'Top {sector_name} DApps by Market Cap', fontsize=11, fontweight='bold')

    # ── 2. Governance / Decentralisation breakdown ──
    ax = axes[0, 1]
    if 'level_of_decentralisation' in df_sector.columns:
        dec_counts = df_sector['level_of_decentralisation'].value_counts()
        dec_colors = {'CENTRALIZED': '#d62728', 'SEMI_DECENTRALIZED': '#ff7f0e',
                      'DECENTRALIZED': '#2ca02c'}
        ax.pie(dec_counts.values,
               labels=dec_counts.index,
               autopct='%1.1f%%', startangle=90,
               colors=[dec_colors.get(d, '#999') for d in dec_counts.index])
    ax.set_title(f'{sector_name} Decentralisation', fontsize=11, fontweight='bold')

    # ── 3. Token type distribution ──
    ax = axes[1, 0]
    if 'token_type_primary' in df_sector.columns:
        tt_counts = df_sector['token_type_primary'].value_counts()
        tt_counts = tt_counts[tt_counts.index != 'NONE']
        if len(tt_counts) > 0:
            tt_counts.plot(kind='barh', ax=ax, color='steelblue', edgecolor='black')
            for i, v in enumerate(tt_counts.values):
                ax.text(v + 0.3, i, str(v), va='center', fontsize=9)
    ax.set_title(f'{sector_name} Token Types', fontsize=11, fontweight='bold')
    ax.set_xlabel('Number of DApps')

    # ── 4. Governance type breakdown ──
    ax = axes[1, 1]
    if 'governance_type' in df_sector.columns:
        gov_counts = df_sector['governance_type'].value_counts()
        gov_counts.plot(kind='barh', ax=ax, color='coral', edgecolor='black')
        for i, v in enumerate(gov_counts.values):
            ax.text(v + 0.2, i, str(v), va='center', fontsize=9)
    ax.set_title(f'{sector_name} Governance Types', fontsize=11, fontweight='bold')
    ax.set_xlabel('Number of DApps')

    # ── 5. Key metrics comparison vs full ecosystem ──
    ax = axes[2, 0]
    metrics_compare = ['market_cap', 'users', 'tvl', 'volume']
    sector_medians = []
    eco_medians = []
    for m in metrics_compare:
        s_val = df_sector[df_sector[m] > 0][m].median() if (df_sector[m] > 0).any() else 0
        e_val = df_full[df_full[m] > 0][m].median() if (df_full[m] > 0).any() else 0
        sector_medians.append(s_val)
        eco_medians.append(e_val)

    x = np.arange(len(metrics_compare))
    width = 0.35
    ax.bar(x - width/2, sector_medians, width, label=sector_name, color='#3498db')
    ax.bar(x + width/2, eco_medians, width, label='Full Ecosystem', color='#95a5a6')
    ax.set_xticks(x)
    ax.set_xticklabels([m.replace('_', ' ').title() for m in metrics_compare], fontsize=9)
    ax.set_yscale('log')
    ax.set_ylabel('Median Value (log)')
    ax.legend(fontsize=9)
    ax.set_title(f'{sector_name} vs Ecosystem (Median)', fontsize=11, fontweight='bold')

    # ── 6. Ownership status ──
    ax = axes[2, 1]
    if 'ownership_status' in df_sector.columns:
        own_counts = df_sector['ownership_status'].value_counts()
        own_counts.plot(kind='barh', ax=ax, color='mediumpurple', edgecolor='black')
        for i, v in enumerate(own_counts.values):
            ax.text(v + 0.2, i, str(v), va='center', fontsize=9)
    ax.set_title(f'{sector_name} Ownership Status', fontsize=11, fontweight='bold')
    ax.set_xlabel('Number of DApps')

    plt.tight_layout()
    out = OUTPUT_DIR / filename
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {out}")
    plt.close()

    # Print summary stats
    _print_sector_stats(df_sector, sector_name)


def _print_sector_stats(df_s, name):
    """Console summary for a sector."""
    print(f"\n  {name} SUMMARY:")
    print(f"    DApps: {len(df_s)}")
    has_mcap = df_s[df_s['market_cap'] > 0]
    if len(has_mcap) > 0:
        print(f"    Total Market Cap: ${has_mcap['market_cap'].sum():,.0f}")
        print(f"    Median Market Cap: ${has_mcap['market_cap'].median():,.0f}")
    has_tvl = df_s[df_s['tvl'] > 0]
    if len(has_tvl) > 0:
        print(f"    Total TVL: ${has_tvl['tvl'].sum():,.0f}")
    print(f"    Has Token: {df_s['has_token'].sum()} ({df_s['has_token'].mean()*100:.1f}%)")
    if 'level_of_decentralisation' in df_s.columns:
        dec = df_s['level_of_decentralisation'].value_counts(normalize=True) * 100
        for k, v in dec.items():
            print(f"    {k}: {v:.1f}%")
    if 'token_type_primary' in df_s.columns:
        tt = df_s[df_s['token_type_primary'] != 'NONE']['token_type_primary'].value_counts()
        if len(tt) > 0:
            print(f"    Dominant Token Type: {tt.index[0]} ({tt.values[0]})")

    # Top 5 by market cap
    top5 = df_s[df_s['market_cap'] > 0].nlargest(5, 'market_cap')
    if len(top5) > 0:
        print(f"    Top 5 by Market Cap:")
        for _, row in top5.iterrows():
            gov = row.get('governance_type', '?')
            tt = row.get('token_type_primary', '?')
            print(f"      - {row['name']} (MCap ${row['market_cap']:,.0f}, "
                  f"Gov: {gov}, Token: {tt})")


# ─────────────────────────────────────────────────────────────────
# DeFi-specific additional analysis
# ─────────────────────────────────────────────────────────────────
def analyze_defi_subcategories(df):
    """Break DeFi down into sub-sectors and compare."""
    defi_cats = ['DEX', 'Lending', 'Derivatives', 'Yield Aggregator']
    df_defi = df[df['dapp_category'].isin(defi_cats)].copy()

    if len(df_defi) < 5:
        return

    print(f"\n{'='*60}")
    print("  DeFi SUB-CATEGORY COMPARISON")
    print(f"{'='*60}")

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('DeFi Sub-Category Comparison', fontsize=14, fontweight='bold')

    # 1. Count + TVL by sub-category
    ax = axes[0, 0]
    cat_stats = df_defi.groupby('dapp_category').agg(
        count=('name', 'count'),
        total_tvl=('tvl', 'sum'),
        median_mcap=('market_cap', 'median')
    ).sort_values('total_tvl', ascending=False)
    cat_stats['total_tvl'].plot(kind='barh', ax=ax, color='steelblue', edgecolor='black')
    ax.set_title('Total TVL by DeFi Sub-Category', fontsize=11, fontweight='bold')
    ax.set_xlabel('Total TVL (USD)')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(
        lambda x, _: f'${x/1e9:.1f}B'))
    for i, (idx, row) in enumerate(cat_stats.iterrows()):
        ax.text(row['total_tvl'] + 1e7, i, f'n={int(row["count"])}',
                va='center', fontsize=9)

    # 2. Governance score by DeFi sub-category
    ax = axes[0, 1]
    gov_by_defi = df_defi.groupby('dapp_category')['governance_score'].agg(['mean', 'median'])
    gov_by_defi = gov_by_defi.sort_values('mean', ascending=True)
    gov_by_defi['mean'].plot(kind='barh', ax=ax, color='coral', edgecolor='black')
    ax.set_title('Avg Governance Score by DeFi Type', fontsize=11, fontweight='bold')
    ax.set_xlabel('Governance Score (0–1)')

    # 3. Token type distribution within DeFi
    ax = axes[1, 0]
    defi_tt = pd.crosstab(df_defi['dapp_category'],
                          df_defi['token_type_primary'], normalize='index') * 100
    type_cols = [c for c in ['GOVERNANCE', 'UTILITY', 'REWARD', 'SPECULATIVE', 'SOCIAL', 'NONE']
                 if c in defi_tt.columns]
    defi_tt[type_cols].plot(kind='barh', stacked=True, ax=ax)
    ax.set_xlabel('Percentage (%)')
    ax.set_title('Token Type Mix in DeFi Sub-Categories', fontsize=11, fontweight='bold')
    ax.legend(title='Token Type', fontsize=8, bbox_to_anchor=(1.05, 1))

    # 4. Multi-chain adoption in DeFi
    ax = axes[1, 1]
    mc_defi = df_defi.groupby('dapp_category')['is_multi_chain'].mean() * 100
    mc_defi = mc_defi.sort_values(ascending=True)
    mc_defi.plot(kind='barh', ax=ax, color='mediumseagreen', edgecolor='black')
    ax.set_xlabel('Multi-Chain Adoption (%)')
    ax.set_title('Multi-Chain Adoption in DeFi', fontsize=11, fontweight='bold')

    plt.tight_layout()
    out = OUTPUT_DIR / '11_defi_subcategories.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {out}")
    plt.close()


# ─────────────────────────────────────────────────────────────────
# Prediction Markets specific analysis
# ─────────────────────────────────────────────────────────────────
def analyze_prediction_markets_detail(df):
    """Detailed look at prediction market DApps."""
    df_pm = df[df['is_prediction_market']].copy()
    n = len(df_pm)
    if n < 2:
        print(f"  Only {n} prediction market DApps – skipping detail")
        return

    print(f"\n{'='*60}")
    print(f"  PREDICTION MARKETS DETAIL  ({n} DApps)")
    print(f"{'='*60}")

    # List all prediction market dapps with key attributes
    cols_show = ['name', 'governance_type', 'ownership_status',
                 'level_of_decentralisation', 'token_type_primary',
                 'market_cap', 'users', 'tvl', 'chains']
    available = [c for c in cols_show if c in df_pm.columns]
    print(df_pm[available].to_string(index=False))

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle(f'Prediction Markets Deep Dive (n={n})', fontsize=14, fontweight='bold')

    # 1. Individual DApps comparison (market cap)
    ax = axes[0, 0]
    df_pm_mcap = df_pm[df_pm['market_cap'] > 0].sort_values('market_cap', ascending=True)
    if len(df_pm_mcap) > 0:
        ax.barh(df_pm_mcap['name'], df_pm_mcap['market_cap'], color='steelblue')
        ax.set_xlabel('Market Cap (USD)')
        ax.xaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, _: f'${x/1e6:.0f}M'))
    ax.set_title('Prediction Market DApps – Market Cap', fontsize=11, fontweight='bold')

    # 2. Governance breakdown
    ax = axes[0, 1]
    gov_pm = df_pm['governance_type'].value_counts()
    gov_pm.plot(kind='pie', ax=ax, autopct='%1.0f%%', startangle=90)
    ax.set_ylabel('')
    ax.set_title('Governance Models', fontsize=11, fontweight='bold')

    # 3. Token types
    ax = axes[1, 0]
    tt_pm = df_pm['token_type_primary'].value_counts()
    tt_pm.plot(kind='bar', ax=ax, color='coral', edgecolor='black')
    ax.set_title('Token Types in Prediction Markets', fontsize=11, fontweight='bold')
    ax.set_ylabel('Count')
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')

    # 4. Chains used
    ax = axes[1, 1]
    all_chains = []
    for c in df_pm['chains'].dropna():
        all_chains.extend([ch.strip() for ch in str(c).split(',')])
    chain_counts = Counter(all_chains)
    chain_df = pd.DataFrame.from_dict(chain_counts, orient='index',
                                       columns=['count']).sort_values('count', ascending=True)
    chain_df.plot(kind='barh', ax=ax, legend=False, color='mediumpurple', edgecolor='black')
    ax.set_xlabel('Deployments')
    ax.set_title('Chains Used by Prediction Markets', fontsize=11, fontweight='bold')

    plt.tight_layout()
    out = OUTPUT_DIR / '11_prediction_markets_detail.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {out}")
    plt.close()


# ─────────────────────────────────────────────────────────────────
# Cross-sector comparison
# ─────────────────────────────────────────────────────────────────
def cross_sector_comparison(df):
    """Compare all identified sectors side by side."""
    print(f"\n{'='*60}")
    print("  CROSS-SECTOR COMPARISON")
    print(f"{'='*60}")

    sectors = {
        'DeFi': df['is_defi'],
        'Gaming': df['is_gaming'],
        'Social': df['is_social'],
        'Prediction Mkt': df['is_prediction_market'],
        'RWA': df['is_rwa'],
        'AI': df['is_ai'],
    }

    rows = []
    for name, mask in sectors.items():
        subset = df[mask]
        if len(subset) == 0:
            continue
        mkt = subset[subset['market_cap'] > 0]
        rows.append({
            'Sector': name,
            'Count': len(subset),
            'Has Token %': subset['has_token'].mean() * 100,
            'Median MCap': mkt['market_cap'].median() if len(mkt) > 0 else 0,
            'Total TVL': subset['tvl'].sum(),
            'Avg Gov Score': subset['governance_score'].mean(),
            'Multi-Chain %': subset['is_multi_chain'].mean() * 100,
            'Decentralized %': (subset['level_of_decentralisation'] == 'DECENTRALIZED').mean() * 100,
            'Gov Token %': subset['is_governance_token'].mean() * 100,
        })

    comp_df = pd.DataFrame(rows).set_index('Sector')
    print(comp_df.round(1))

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Cross-Sector Comparison', fontsize=14, fontweight='bold')

    sector_names = comp_df.index.tolist()
    x = np.arange(len(sector_names))

    # 1. DApp count per sector
    ax = axes[0, 0]
    ax.bar(x, comp_df['Count'], color='steelblue', edgecolor='black')
    ax.set_xticks(x)
    ax.set_xticklabels(sector_names, rotation=30, ha='right')
    ax.set_ylabel('Number of DApps')
    ax.set_title('DApp Count by Sector', fontsize=11, fontweight='bold')
    for i, v in enumerate(comp_df['Count']):
        ax.text(i, v + 1, str(v), ha='center', fontsize=9)

    # 2. Governance metrics
    ax = axes[0, 1]
    width = 0.3
    ax.bar(x - width, comp_df['Avg Gov Score'], width, label='Avg Gov Score', color='#3498db')
    ax.bar(x, comp_df['Decentralized %'] / 100, width, label='Decentralized %', color='#2ecc71')
    ax.bar(x + width, comp_df['Gov Token %'] / 100, width, label='Gov Token %', color='#e67e22')
    ax.set_xticks(x)
    ax.set_xticklabels(sector_names, rotation=30, ha='right')
    ax.set_ylabel('Score / Fraction')
    ax.set_title('Governance Comparison', fontsize=11, fontweight='bold')
    ax.legend(fontsize=8)

    # 3. Market metrics
    ax = axes[1, 0]
    ax.bar(x, comp_df['Total TVL'], color='coral', edgecolor='black')
    ax.set_xticks(x)
    ax.set_xticklabels(sector_names, rotation=30, ha='right')
    ax.set_ylabel('Total TVL (USD)')
    ax.set_title('Total TVL by Sector', fontsize=11, fontweight='bold')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(
        lambda y, _: f'${y/1e9:.1f}B' if y >= 1e9 else f'${y/1e6:.0f}M'))

    # 4. Token & multi-chain adoption
    ax = axes[1, 1]
    ax.bar(x - width/2, comp_df['Has Token %'], width, label='Has Token %', color='#9b59b6')
    ax.bar(x + width/2, comp_df['Multi-Chain %'], width, label='Multi-Chain %', color='#1abc9c')
    ax.set_xticks(x)
    ax.set_xticklabels(sector_names, rotation=30, ha='right')
    ax.set_ylabel('Percentage (%)')
    ax.set_title('Token & Multi-Chain Adoption', fontsize=11, fontweight='bold')
    ax.legend(fontsize=8)

    plt.tight_layout()
    out = OUTPUT_DIR / '11_cross_sector_comparison.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {out}")
    plt.close()

    # Save comparison table
    table_path = OUTPUT_DIR / '11_SECTOR_COMPARISON.txt'
    with open(table_path, 'w') as f:
        f.write("CROSS-SECTOR COMPARISON\n")
        f.write("=" * 70 + "\n\n")
        f.write(comp_df.to_string())
        f.write(f"\n\nDate: {pd.Timestamp.now().strftime('%Y-%m-%d')}\n")
    print(f"✓ Saved: {table_path}")


def main():
    print("\n" + "="*60)
    print("SECTOR DEEP DIVE ANALYSIS")
    print("="*60)

    df = load_prepared_data()

    # Individual sector dashboards
    _sector_dashboard(df[df['is_defi']], 'DeFi',
                      '11_defi_dashboard.png', df)
    _sector_dashboard(df[df['is_prediction_market']], 'Prediction Markets',
                      '11_prediction_markets_dashboard.png', df)
    _sector_dashboard(df[df['is_rwa']], 'RWA / Payments',
                      '11_rwa_dashboard.png', df)
    _sector_dashboard(df[df['is_ai']], 'AI DApps',
                      '11_ai_dashboard.png', df)
    _sector_dashboard(df[df['is_gaming']], 'Gaming',
                      '11_gaming_dashboard.png', df)
    _sector_dashboard(df[df['is_social']], 'Social',
                      '11_social_dashboard.png', df)

    # DeFi sub-category analysis
    analyze_defi_subcategories(df)

    # Prediction markets detail
    analyze_prediction_markets_detail(df)

    # Cross-sector comparison
    cross_sector_comparison(df)

    print("\n" + "="*60)
    print("SECTOR DEEP DIVE COMPLETE!")
    print("="*60)
    print("✓ All visualizations saved to:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
