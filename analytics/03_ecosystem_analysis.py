"""
DApp Ecosystem Analysis - Ecosystem Structure & Chain Distribution
====================================================================
This script analyzes blockchain ecosystem structure, chain distribution,
and multi-chain trends across the DApp landscape.

Key Message Target: "Chain ecosystem specialization" - how different 
blockchains serve different DApp niches
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
import warnings

from config import DATA_PATH, OUTPUT_DIR

warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def load_prepared_data():
    """Load the prepared dataset."""
    print("Loading prepared data...")
    df = pd.read_csv(DATA_PATH)
    print(f"✓ Loaded {len(df)} DApps with {len(df.columns)} columns")
    return df

def parse_chains(df):
    """Parse chain information from comma-separated values."""
    print("\n" + "="*60)
    print("PARSING CHAIN INFORMATION")
    print("="*60)
    
    # Parse all chains
    all_chains = []
    for chains_str in df['chains'].dropna():
        chains = [c.strip() for c in str(chains_str).split(',') if c.strip()]
        all_chains.extend(chains)
    
    chain_counts = Counter(all_chains)
    chain_df = pd.DataFrame.from_dict(chain_counts, orient='index', columns=['count'])
    chain_df = chain_df.sort_values('count', ascending=False)
    
    print(f"\n✓ Found {len(chain_df)} unique blockchains")
    print(f"✓ Total chain deployments: {sum(chain_counts.values())}")
    print(f"\nTop 15 Chains:")
    print(chain_df.head(15))
    
    return chain_df

def analyze_chain_dominance(chain_df):
    """Analyze chain dominance and market share."""
    print("\n" + "="*60)
    print("CHAIN DOMINANCE ANALYSIS")
    print("="*60)
    
    total_deployments = chain_df['count'].sum()
    
    # Top chains market share
    top_10 = chain_df.head(10)
    top_10_share = top_10['count'].sum() / total_deployments * 100
    
    print(f"\nTop 10 chains represent {top_10_share:.1f}% of all deployments")
    print(f"\nMarket Share of Top Chains:")
    for idx, row in top_10.iterrows():
        pct = row['count'] / total_deployments * 100
        print(f"  {idx}: {row['count']} deployments ({pct:.1f}%)")
    
    # Visualize
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Blockchain Dominance Analysis', fontsize=14, fontweight='bold')
    
    # Bar chart - Top 15 chains
    ax1 = axes[0]
    top_15 = chain_df.head(15)
    colors = plt.cm.viridis(np.linspace(0, 1, len(top_15)))
    bars = ax1.barh(range(len(top_15)), top_15['count'], color=colors)
    ax1.set_yticks(range(len(top_15)))
    ax1.set_yticklabels(top_15.index)
    ax1.set_xlabel('Number of DApp Deployments', fontsize=10)
    ax1.set_title('Top 15 Blockchains by DApp Count', fontsize=12, fontweight='bold')
    ax1.invert_yaxis()
    
    # Add value labels
    for i, v in enumerate(top_15['count']):
        ax1.text(v + 1, i, str(v), va='center', fontsize=9)
    
    # Pie chart - Top 10 + Others
    ax2 = axes[1]
    top_10_data = chain_df.head(10).copy()
    others_count = chain_df.iloc[10:]['count'].sum()
    
    pie_data = list(top_10_data['count']) + [others_count]
    pie_labels = list(top_10_data.index) + ['Others']
    
    colors_pie = plt.cm.Set3(np.linspace(0, 1, len(pie_data)))
    ax2.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', startangle=90, colors=colors_pie)
    ax2.set_title('Market Share Distribution', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '03_chain_dominance.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()

def analyze_multichain_trends(df):
    """Analyze multi-chain deployment trends."""
    print("\n" + "="*60)
    print("MULTI-CHAIN TRENDS ANALYSIS")
    print("="*60)
    
    # Multi-chain statistics
    multichain_count = df['is_multi_chain'].sum()
    multichain_pct = multichain_count / len(df) * 100
    
    print(f"\nMulti-chain DApps: {multichain_count} ({multichain_pct:.1f}%)")
    print(f"Single-chain DApps: {len(df) - multichain_count} ({100-multichain_pct:.1f}%)")
    
    # Chain count distribution
    chain_count_dist = df['chain_count'].value_counts().sort_index()
    print(f"\nChain Count Distribution:")
    print(chain_count_dist.head(10))
    
    # Multi-chain by category
    if 'dapp_category' in df.columns:
        top_cats = df['dapp_category'].value_counts().head(10).index
        df_top = df[df['dapp_category'].isin(top_cats)]
        
        multichain_by_cat = df_top.groupby('dapp_category').agg({
            'is_multi_chain': ['sum', 'mean', 'count']
        })
        multichain_by_cat.columns = ['multichain_count', 'multichain_pct', 'total']
        multichain_by_cat['multichain_pct'] = multichain_by_cat['multichain_pct'] * 100
        multichain_by_cat = multichain_by_cat.sort_values('multichain_pct', ascending=False)
        
        print(f"\nMulti-chain Adoption by Category (Top 10):")
        print(multichain_by_cat)
    
    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Multi-Chain Deployment Trends', fontsize=14, fontweight='bold')
    
    # Plot 1: Single vs Multi-chain
    ax1 = axes[0, 0]
    sizes = [len(df) - multichain_count, multichain_count]
    labels = ['Single-Chain', 'Multi-Chain']
    colors_pie = ['#3498db', '#e74c3c']
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors_pie,
           textprops={'fontsize': 11})
    ax1.set_title('Single-Chain vs Multi-Chain DApps', fontsize=12, fontweight='bold')
    
    # Plot 2: Chain count distribution
    ax2 = axes[0, 1]
    chain_counts_plot = chain_count_dist.head(10)
    colors = plt.cm.plasma(np.linspace(0, 1, len(chain_counts_plot)))
    ax2.bar(range(len(chain_counts_plot)), chain_counts_plot.values, color=colors)
    ax2.set_xticks(range(len(chain_counts_plot)))
    ax2.set_xticklabels(chain_counts_plot.index)
    ax2.set_xlabel('Number of Chains', fontsize=10)
    ax2.set_ylabel('Number of DApps', fontsize=10)
    ax2.set_title('Distribution of Chain Count', fontsize=12, fontweight='bold')
    
    # Add value labels
    for i, v in enumerate(chain_counts_plot.values):
        ax2.text(i, v + 5, str(v), ha='center', va='bottom', fontsize=9)
    
    # Plot 3: Multi-chain by category
    ax3 = axes[1, 0]
    if 'multichain_by_cat' in locals():
        y_pos = range(len(multichain_by_cat))
        colors = plt.cm.viridis(multichain_by_cat['multichain_pct'].values / 100)
        ax3.barh(y_pos, multichain_by_cat['multichain_pct'], color=colors)
        ax3.set_yticks(y_pos)
        ax3.set_yticklabels(multichain_by_cat.index)
        ax3.set_xlabel('Multi-Chain Adoption Rate (%)', fontsize=10)
        ax3.set_title('Multi-Chain Adoption by Category', fontsize=12, fontweight='bold')
        ax3.invert_yaxis()
        
        # Add value labels
        for i, (idx, row) in enumerate(multichain_by_cat.iterrows()):
            ax3.text(row['multichain_pct'] + 1, i, 
                    f"{row['multichain_pct']:.1f}% ({int(row['multichain_count'])}/{int(row['total'])})",
                    va='center', fontsize=8)
    
    # Plot 4: Market metrics comparison
    ax4 = axes[1, 1]
    comparison_data = []
    for is_multi in [False, True]:
        subset = df[df['is_multi_chain'] == is_multi]
        comparison_data.append({
            'Type': 'Multi-Chain' if is_multi else 'Single-Chain',
            'Avg Market Cap': subset[subset['market_cap'] > 0]['market_cap'].mean(),
            'Avg Users': subset[subset['users'] > 0]['users'].mean(),
            'Avg TVL': subset[subset['tvl'] > 0]['tvl'].mean()
        })
    
    comp_df = pd.DataFrame(comparison_data).set_index('Type')
    comp_df_norm = comp_df / comp_df.loc['Single-Chain']  # Normalize to single-chain
    
    x = np.arange(len(comp_df_norm.columns))
    width = 0.35
    
    single_vals = [comp_df_norm.loc['Single-Chain', col] for col in comp_df_norm.columns]
    multi_vals = [comp_df_norm.loc['Multi-Chain', col] for col in comp_df_norm.columns]
    
    ax4.bar(x - width/2, single_vals, width, label='Single-Chain', color='#3498db')
    ax4.bar(x + width/2, multi_vals, width, label='Multi-Chain', color='#e74c3c')
    
    ax4.set_ylabel('Relative Value (Single-Chain = 1.0)', fontsize=10)
    ax4.set_title('Performance: Multi-Chain vs Single-Chain', fontsize=12, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(['Market Cap', 'Users', 'TVL'], fontsize=9)
    ax4.legend()
    ax4.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '03_multichain_trends.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()

def analyze_chain_specialization(df):
    """Analyze which chains specialize in which categories."""
    print("\n" + "="*60)
    print("CHAIN SPECIALIZATION ANALYSIS")
    print("="*60)
    
    # Create chain-category matrix
    chain_category_data = []
    
    for idx, row in df.iterrows():
        if pd.notna(row['chains']) and pd.notna(row['dapp_category']):
            chains = [c.strip() for c in str(row['chains']).split(',')]
            category = row['dapp_category']
            for chain in chains:
                chain_category_data.append({'chain': chain, 'category': category})
    
    cc_df = pd.DataFrame(chain_category_data)
    
    # Get top chains and categories
    top_chains = cc_df['chain'].value_counts().head(12).index
    top_categories = cc_df['category'].value_counts().head(10).index
    
    # Create cross-tabulation
    cc_matrix = pd.crosstab(
        cc_df[cc_df['chain'].isin(top_chains)]['chain'],
        cc_df[cc_df['category'].isin(top_categories)]['category']
    )
    
    print(f"\nChain-Category Matrix (Top 12 chains x Top 10 categories):")
    print(cc_matrix)
    
    # Calculate specialization index (normalized by row)
    cc_matrix_norm = cc_matrix.div(cc_matrix.sum(axis=1), axis=0) * 100
    
    # Find dominant category for each chain
    print(f"\nChain Specialization:")
    for chain in cc_matrix_norm.index:
        top_cat = cc_matrix_norm.loc[chain].idxmax()
        top_pct = cc_matrix_norm.loc[chain].max()
        total = cc_matrix.loc[chain].sum()
        print(f"  {chain}: {top_cat} ({top_pct:.1f}% of {int(total)} DApps)")
    
    # Visualize
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    fig.suptitle('Chain Specialization Analysis', fontsize=14, fontweight='bold')
    
    # Heatmap 1: Absolute counts
    ax1 = axes[0]
    sns.heatmap(cc_matrix.T, annot=True, fmt='d', cmap='YlOrRd', ax=ax1,
               cbar_kws={'label': 'Number of DApps'})
    ax1.set_title('DApp Distribution: Chains × Categories (Absolute)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Blockchain', fontsize=10)
    ax1.set_ylabel('Category', fontsize=10)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Heatmap 2: Percentage (specialization)
    ax2 = axes[1]
    sns.heatmap(cc_matrix_norm.T, annot=True, fmt='.1f', cmap='viridis', ax=ax2,
               cbar_kws={'label': 'Percentage'})
    ax2.set_title('Chain Specialization: % of DApps by Category', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Blockchain', fontsize=10)
    ax2.set_ylabel('Category', fontsize=10)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '03_chain_specialization.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()

def create_chain_treemap(df):
    """Create interactive treemap of chains and categories."""
    print("\n" + "="*60)
    print("CREATING CHAIN ECOSYSTEM TREEMAP")
    print("="*60)
    
    # Prepare data
    chain_category_data = []
    
    for idx, row in df.iterrows():
        if pd.notna(row['chains']) and pd.notna(row['dapp_category']):
            chains = [c.strip() for c in str(row['chains']).split(',')]
            category = row['dapp_category']
            name = row['name']
            users = row['users'] if pd.notna(row['users']) else 0
            
            for chain in chains:
                chain_category_data.append({
                    'chain': chain,
                    'category': category,
                    'dapp': name,
                    'users': users
                })
    
    cc_df = pd.DataFrame(chain_category_data)
    
    # Filter to top chains and categories
    top_chains = cc_df['chain'].value_counts().head(8).index
    cc_df_filtered = cc_df[cc_df['chain'].isin(top_chains)]
    
    # Create treemap
    fig = px.treemap(
        cc_df_filtered,
        path=['chain', 'category', 'dapp'],
        values='users',
        title='DApp Ecosystem Structure: Chains → Categories → DApps',
        height=800
    )
    
    fig.update_traces(textinfo='label+percent parent')
    
    output_path = OUTPUT_DIR / '03_chain_treemap.html'
    fig.write_html(output_path)
    print(f"✓ Saved interactive treemap: {output_path}")

def analyze_network_effects(df):
    """Analyze network effects and chain success metrics."""
    print("\n" + "="*60)
    print("CHAIN NETWORK EFFECTS ANALYSIS")
    print("="*60)
    
    # Aggregate metrics by chain
    chain_metrics = []
    
    for chain in df['chains'].dropna().str.split(',').explode().str.strip().unique():
        # Get all DApps on this chain
        chain_dapps = df[df['chains'].fillna('').str.contains(chain, case=False, na=False)]
        
        if len(chain_dapps) > 0:
            chain_metrics.append({
                'chain': chain,
                'dapp_count': len(chain_dapps),
                'total_users': chain_dapps['users'].sum(),
                'avg_users': chain_dapps[chain_dapps['users'] > 0]['users'].mean(),
                'total_tvl': chain_dapps['tvl'].sum(),
                'avg_market_cap': chain_dapps[chain_dapps['market_cap'] > 0]['market_cap'].mean(),
                'total_volume': chain_dapps['volume'].sum()
            })
    
    metrics_df = pd.DataFrame(chain_metrics)
    metrics_df = metrics_df.sort_values('dapp_count', ascending=False).head(15)
    
    print("\nTop 15 Chains by Network Metrics:")
    print(metrics_df[['chain', 'dapp_count', 'total_users', 'total_tvl']].to_string(index=False))
    
    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Chain Network Effects & Success Metrics', fontsize=14, fontweight='bold')
    
    # Plot 1: DApp count vs Total users (bubble = TVL)
    ax1 = axes[0, 0]
    scatter = ax1.scatter(metrics_df['dapp_count'], metrics_df['total_users'],
                         s=metrics_df['total_tvl']/1e7, alpha=0.6, c=range(len(metrics_df)),
                         cmap='viridis')
    ax1.set_xlabel('Number of DApps', fontsize=10)
    ax1.set_ylabel('Total Active Users', fontsize=10)
    ax1.set_title('Chain Popularity vs User Base\n(bubble size = TVL)', fontsize=11, fontweight='bold')
    ax1.set_yscale('log')
    
    # Add labels for top chains
    for idx, row in metrics_df.head(8).iterrows():
        ax1.annotate(row['chain'], (row['dapp_count'], row['total_users']),
                    fontsize=8, alpha=0.7)
    
    # Plot 2: DApp count vs Average market cap
    ax2 = axes[0, 1]
    metrics_clean = metrics_df.dropna(subset=['avg_market_cap'])
    ax2.scatter(metrics_clean['dapp_count'], metrics_clean['avg_market_cap'],
               s=100, alpha=0.6, c=range(len(metrics_clean)), cmap='plasma')
    ax2.set_xlabel('Number of DApps', fontsize=10)
    ax2.set_ylabel('Average Market Cap per DApp (USD)', fontsize=10)
    ax2.set_title('Chain Size vs DApp Quality', fontsize=11, fontweight='bold')
    ax2.set_yscale('log')
    
    # Add labels
    for idx, row in metrics_clean.head(6).iterrows():
        ax2.annotate(row['chain'], (row['dapp_count'], row['avg_market_cap']),
                    fontsize=8, alpha=0.7)
    
    # Plot 3: Total TVL by chain
    ax3 = axes[1, 0]
    metrics_tvl = metrics_df.nlargest(12, 'total_tvl')
    colors = plt.cm.Blues(np.linspace(0.4, 1, len(metrics_tvl)))
    ax3.barh(range(len(metrics_tvl)), metrics_tvl['total_tvl'], color=colors)
    ax3.set_yticks(range(len(metrics_tvl)))
    ax3.set_yticklabels(metrics_tvl['chain'])
    ax3.set_xlabel('Total TVL (USD)', fontsize=10)
    ax3.set_title('Total Value Locked by Chain', fontsize=11, fontweight='bold')
    ax3.invert_yaxis()
    
    # Plot 4: Total volume by chain
    ax4 = axes[1, 1]
    metrics_vol = metrics_df.nlargest(12, 'total_volume')
    colors = plt.cm.Greens(np.linspace(0.4, 1, len(metrics_vol)))
    ax4.barh(range(len(metrics_vol)), metrics_vol['total_volume'], color=colors)
    ax4.set_yticks(range(len(metrics_vol)))
    ax4.set_yticklabels(metrics_vol['chain'])
    ax4.set_xlabel('Total Trading Volume (USD)', fontsize=10)
    ax4.set_title('Total Volume by Chain', fontsize=11, fontweight='bold')
    ax4.invert_yaxis()
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '03_chain_network_effects.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()

def generate_ecosystem_insights(df, chain_df):
    """Generate key insights about ecosystem structure."""
    print("\n" + "="*60)
    print("KEY ECOSYSTEM INSIGHTS")
    print("="*60)
    
    # Insight 1: Chain concentration
    top_5_chains = chain_df.head(5)
    top_5_pct = top_5_chains['count'].sum() / chain_df['count'].sum() * 100
    
    print(f"\n1. CHAIN CONCENTRATION:")
    print(f"   - Top 5 chains: {', '.join(top_5_chains.index.tolist())}")
    print(f"   - Control {top_5_pct:.1f}% of all DApp deployments")
    
    # Insight 2: Multi-chain adoption
    multichain_pct = df['is_multi_chain'].mean() * 100
    avg_chains = df[df['is_multi_chain']]['chain_count'].mean()
    
    print(f"\n2. MULTI-CHAIN ADOPTION:")
    print(f"   - {multichain_pct:.1f}% of DApps are multi-chain")
    print(f"   - Multi-chain DApps deploy on avg {avg_chains:.1f} chains")
    
    # Insight 3: Chain leadership
    print(f"\n3. CHAIN LEADERSHIP:")
    print(f"   - #{1}: {top_5_chains.index[0]} with {top_5_chains.iloc[0]['count']} DApps")
    print(f"   - #{2}: {top_5_chains.index[1]} with {top_5_chains.iloc[1]['count']} DApps")
    print(f"   - #{3}: {top_5_chains.index[2]} with {top_5_chains.iloc[2]['count']} DApps")
    
    return {
        'top_5_pct': top_5_pct,
        'multichain_pct': multichain_pct,
        'top_chain': top_5_chains.index[0]
    }

def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("ECOSYSTEM STRUCTURE & CHAIN DISTRIBUTION ANALYSIS")
    print("="*60)
    
    # Load data
    df = load_prepared_data()
    
    # Run analyses
    chain_df = parse_chains(df)
    analyze_chain_dominance(chain_df)
    analyze_multichain_trends(df)
    analyze_chain_specialization(df)
    create_chain_treemap(df)
    analyze_network_effects(df)
    insights = generate_ecosystem_insights(df, chain_df)
    
    print("\n" + "="*60)
    print("ECOSYSTEM ANALYSIS COMPLETE!")
    print("="*60)
    print("\n✓ All visualizations saved to:", OUTPUT_DIR)
    
    return insights

if __name__ == "__main__":
    insights = main()

