"""
DApp Ecosystem Analysis - Governance & Decentralization Analysis
=================================================================
This script analyzes governance models, ownership structures, and decentralization
levels across the DApp ecosystem.

Key Message Target: "Governance paradox in DApps" - relationship between claimed 
decentralization and actual control structures
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

def analyze_governance_distribution(df):
    """Analyze distribution of governance types."""
    print("\n" + "="*60)
    print("GOVERNANCE DISTRIBUTION ANALYSIS")
    print("="*60)
    
    # Overall distribution
    gov_counts = df['governance_type'].value_counts()
    own_counts = df['ownership_status'].value_counts()
    decent_counts = df['level_of_decentralisation'].value_counts()
    
    print("\nGovernance Types:")
    print(gov_counts)
    print(f"\nMost common: {gov_counts.index[0]} ({gov_counts.values[0]/len(df)*100:.1f}%)")
    
    print("\nOwnership Status:")
    print(own_counts)
    print(f"\nMost common: {own_counts.index[0]} ({own_counts.values[0]/len(df)*100:.1f}%)")
    
    print("\nDecentralization Levels:")
    print(decent_counts)
    print(f"\nMost common: {decent_counts.index[0]} ({decent_counts.values[0]/len(df)*100:.1f}%)")
    
    # Create visualization
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Governance, Ownership & Decentralization Distribution', 
                 fontsize=14, fontweight='bold')
    
    # Governance types
    colors1 = plt.cm.Set3(np.linspace(0, 1, len(gov_counts)))
    gov_counts.plot(kind='barh', ax=axes[0], color=colors1)
    axes[0].set_title('Governance Type', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Number of DApps')
    for i, v in enumerate(gov_counts.values):
        axes[0].text(v + 5, i, str(v), va='center')
    
    # Ownership status
    colors2 = plt.cm.Pastel1(np.linspace(0, 1, len(own_counts)))
    own_counts.plot(kind='barh', ax=axes[1], color=colors2)
    axes[1].set_title('Ownership Status', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Number of DApps')
    for i, v in enumerate(own_counts.values):
        axes[1].text(v + 5, i, str(v), va='center')
    
    # Decentralization levels
    colors3 = ['#d62728', '#ff7f0e', '#2ca02c']  # Red, Orange, Green
    decent_counts.plot(kind='barh', ax=axes[2], color=colors3)
    axes[2].set_title('Decentralization Level', fontsize=12, fontweight='bold')
    axes[2].set_xlabel('Number of DApps')
    for i, v in enumerate(decent_counts.values):
        axes[2].text(v + 5, i, str(v), va='center')
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '02_governance_distribution.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()

def analyze_governance_cross_tabulation(df):
    """Analyze relationships between governance dimensions."""
    print("\n" + "="*60)
    print("GOVERNANCE CROSS-TABULATION ANALYSIS")
    print("="*60)
    
    # Filter out nulls for cleaner analysis
    df_clean = df.dropna(subset=['governance_type', 'ownership_status', 'level_of_decentralisation'])
    
    print(f"\nAnalyzing {len(df_clean)} DApps with complete governance data...")
    
    # Governance vs Decentralization
    crosstab1 = pd.crosstab(df_clean['level_of_decentralisation'], 
                            df_clean['governance_type'], margins=True)
    print("\nGovernance Type vs Decentralization Level:")
    print(crosstab1)
    
    # Ownership vs Decentralization
    crosstab2 = pd.crosstab(df_clean['level_of_decentralisation'], 
                            df_clean['ownership_status'], margins=True)
    print("\nOwnership Status vs Decentralization Level:")
    print(crosstab2)
    
    # Create heatmap visualizations
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))
    fig.suptitle('Governance Cross-Tabulation Heatmaps', fontsize=14, fontweight='bold')
    
    # Heatmap 1: Governance vs Decentralization
    ct1_pct = pd.crosstab(df_clean['level_of_decentralisation'], 
                          df_clean['governance_type'], normalize='columns') * 100
    sns.heatmap(ct1_pct, annot=True, fmt='.1f', cmap='YlOrRd', ax=axes[0], 
                cbar_kws={'label': 'Percentage'})
    axes[0].set_title('Governance Type vs Decentralization\n(% within each governance type)', 
                     fontsize=11, fontweight='bold')
    axes[0].set_xlabel('Governance Type')
    axes[0].set_ylabel('Decentralization Level')
    plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Heatmap 2: Ownership vs Decentralization
    ct2_pct = pd.crosstab(df_clean['level_of_decentralisation'], 
                          df_clean['ownership_status'], normalize='columns') * 100
    sns.heatmap(ct2_pct, annot=True, fmt='.1f', cmap='YlGnBu', ax=axes[1],
                cbar_kws={'label': 'Percentage'})
    axes[1].set_title('Ownership Status vs Decentralization\n(% within each ownership type)', 
                     fontsize=11, fontweight='bold')
    axes[1].set_xlabel('Ownership Status')
    axes[1].set_ylabel('Decentralization Level')
    plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '02_governance_crosstab_heatmaps.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()

def analyze_governance_by_category(df):
    """Analyze governance patterns across DApp categories."""
    print("\n" + "="*60)
    print("GOVERNANCE BY CATEGORY ANALYSIS")
    print("="*60)
    
    df_clean = df.dropna(subset=['dapp_category', 'level_of_decentralisation'])
    
    # Top categories
    top_categories = df_clean['dapp_category'].value_counts().head(8).index
    df_top = df_clean[df_clean['dapp_category'].isin(top_categories)]
    
    print(f"\nAnalyzing top 8 categories...")
    
    # Governance score by category
    gov_by_cat = df_top.groupby('dapp_category')['governance_score'].agg(['mean', 'median', 'count'])
    gov_by_cat = gov_by_cat.sort_values('mean', ascending=False)
    
    print("\nGovernance Score by Category (mean):")
    print(gov_by_cat)
    
    # Decentralization distribution by category
    decent_by_cat = pd.crosstab(df_top['dapp_category'], 
                                 df_top['level_of_decentralisation'], 
                                 normalize='index') * 100
    
    print("\nDecentralization Distribution by Category (%):")
    print(decent_by_cat)
    
    # Create visualizations
    fig, axes = plt.subplots(2, 1, figsize=(14, 12))
    fig.suptitle('Governance Patterns by DApp Category', fontsize=14, fontweight='bold')
    
    # Plot 1: Governance score by category
    ax1 = axes[0]
    colors = plt.cm.viridis(np.linspace(0, 1, len(gov_by_cat)))
    bars = ax1.barh(range(len(gov_by_cat)), gov_by_cat['mean'], color=colors)
    ax1.set_yticks(range(len(gov_by_cat)))
    ax1.set_yticklabels(gov_by_cat.index)
    ax1.set_xlabel('Average Governance Score (0=Centralized, 1=Decentralized)', fontsize=10)
    ax1.set_title('Average Governance Score by Category', fontsize=12, fontweight='bold')
    ax1.invert_yaxis()
    
    # Add value labels and count
    for i, (idx, row) in enumerate(gov_by_cat.iterrows()):
        ax1.text(row['mean'] + 0.01, i, f"{row['mean']:.2f} (n={int(row['count'])})", 
                va='center', fontsize=9)
    
    # Plot 2: Stacked bar chart of decentralization by category
    ax2 = axes[1]
    decent_cols = ['CENTRALIZED', 'SEMI_DECENTRALIZED', 'DECENTRALIZED']
    decent_cols = [col for col in decent_cols if col in decent_by_cat.columns]
    
    decent_by_cat_sorted = decent_by_cat.loc[gov_by_cat.index, decent_cols]
    decent_by_cat_sorted.plot(kind='barh', stacked=True, ax=ax2,
                              color=['#d62728', '#ff7f0e', '#2ca02c'])
    ax2.set_xlabel('Percentage', fontsize=10)
    ax2.set_title('Decentralization Level Distribution by Category', 
                  fontsize=12, fontweight='bold')
    ax2.legend(title='Decentralization', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '02_governance_by_category.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()

def analyze_governance_market_correlation(df):
    """Analyze correlation between governance and market metrics."""
    print("\n" + "="*60)
    print("GOVERNANCE-MARKET CORRELATION ANALYSIS")
    print("="*60)
    
    # Filter DApps with governance data and market metrics
    df_analysis = df[
        (df['governance_score'].notna()) & 
        (df['market_cap'] > 0) | (df['users'] > 0) | (df['tvl'] > 0)
    ].copy()
    
    print(f"\nAnalyzing {len(df_analysis)} DApps with governance and market data...")
    
    # Group by decentralization level
    decent_groups = df_analysis.groupby('level_of_decentralisation').agg({
        'market_cap': ['mean', 'median', 'count'],
        'users': ['mean', 'median'],
        'tvl': ['mean', 'median'],
        'volume': ['mean', 'median']
    })
    
    print("\nMarket Metrics by Decentralization Level:")
    print(decent_groups)
    
    # Calculate correlations
    correlation_cols = ['governance_score', 'market_cap', 'users', 'tvl', 'volume', 
                       'transactions', 'volatility_index']
    df_corr = df_analysis[correlation_cols].copy()
    
    # Log transform for skewed metrics
    for col in ['market_cap', 'users', 'tvl', 'volume', 'transactions']:
        if col in df_corr.columns:
            df_corr[f'{col}_log'] = np.log1p(df_corr[col].fillna(0))
    
    corr_matrix = df_corr[[col for col in df_corr.columns if '_log' in col or col == 'governance_score']].corr()
    
    print("\nCorrelation with Governance Score:")
    print(corr_matrix['governance_score'].sort_values(ascending=False))
    
    # Create visualizations
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    fig.suptitle('Governance vs Market Performance', fontsize=14, fontweight='bold')
    
    # Plot 1: Market cap by decentralization (boxplot)
    ax1 = fig.add_subplot(gs[0, 0])
    df_plot1 = df_analysis[df_analysis['market_cap'] > 0]
    if len(df_plot1) > 0:
        order = ['CENTRALIZED', 'SEMI_DECENTRALIZED', 'DECENTRALIZED']
        order = [o for o in order if o in df_plot1['level_of_decentralisation'].values]
        sns.boxplot(data=df_plot1, y='level_of_decentralisation', x='market_cap',
                   order=order, ax=ax1, palette=['#d62728', '#ff7f0e', '#2ca02c'])
        ax1.set_xscale('log')
        ax1.set_xlabel('Market Cap (USD, log scale)', fontsize=10)
        ax1.set_ylabel('Decentralization Level', fontsize=10)
        ax1.set_title('Market Cap Distribution by Decentralization', fontsize=11, fontweight='bold')
    
    # Plot 2: Users by decentralization (boxplot)
    ax2 = fig.add_subplot(gs[0, 1])
    df_plot2 = df_analysis[df_analysis['users'] > 0]
    if len(df_plot2) > 0:
        order = ['CENTRALIZED', 'SEMI_DECENTRALIZED', 'DECENTRALIZED']
        order = [o for o in order if o in df_plot2['level_of_decentralisation'].values]
        sns.boxplot(data=df_plot2, y='level_of_decentralisation', x='users',
                   order=order, ax=ax2, palette=['#d62728', '#ff7f0e', '#2ca02c'])
        ax2.set_xscale('log')
        ax2.set_xlabel('Active Users (log scale)', fontsize=10)
        ax2.set_ylabel('Decentralization Level', fontsize=10)
        ax2.set_title('User Base Distribution by Decentralization', fontsize=11, fontweight='bold')
    
    # Plot 3: Governance score vs market cap scatter
    ax3 = fig.add_subplot(gs[1, 0])
    df_plot3 = df_analysis[(df_analysis['market_cap'] > 0) & (df_analysis['governance_score'].notna())]
    if len(df_plot3) > 0:
        scatter = ax3.scatter(df_plot3['governance_score'], df_plot3['market_cap'],
                            c=df_plot3['users'], s=50, alpha=0.6, cmap='viridis')
        ax3.set_yscale('log')
        ax3.set_xlabel('Governance Score (0=Centralized, 1=Decentralized)', fontsize=10)
        ax3.set_ylabel('Market Cap (USD, log scale)', fontsize=10)
        ax3.set_title('Governance Score vs Market Cap', fontsize=11, fontweight='bold')
        cbar = plt.colorbar(scatter, ax=ax3)
        cbar.set_label('Active Users', fontsize=9)
    
    # Plot 4: Correlation heatmap
    ax4 = fig.add_subplot(gs[1, 1])
    corr_subset = corr_matrix.loc[['governance_score'], 
                                   [col for col in corr_matrix.columns if col != 'governance_score']]
    sns.heatmap(corr_subset, annot=True, fmt='.3f', cmap='RdYlGn', center=0,
               ax=ax4, cbar_kws={'label': 'Correlation'}, vmin=-0.3, vmax=0.3)
    ax4.set_title('Governance Score Correlations', fontsize=11, fontweight='bold')
    ax4.set_ylabel('')
    
    output_path = OUTPUT_DIR / '02_governance_market_correlation.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()

def create_sankey_diagram(df):
    """Create Sankey diagram showing governance flow."""
    print("\n" + "="*60)
    print("CREATING GOVERNANCE FLOW SANKEY DIAGRAM")
    print("="*60)
    
    df_clean = df.dropna(subset=['governance_type', 'ownership_status', 'level_of_decentralisation'])
    
    # Prepare data for Sankey
    # Governance -> Ownership -> Decentralization
    
    # Create unique labels
    gov_types = df_clean['governance_type'].unique()
    own_types = df_clean['ownership_status'].unique()
    decent_types = df_clean['level_of_decentralisation'].unique()
    
    # Create label list and mapping
    labels = (list(gov_types) + 
              [f"{o}_own" for o in own_types] + 
              [f"{d}_decent" for d in decent_types])
    
    label_dict = {label: idx for idx, label in enumerate(labels)}
    
    # Count flows
    flows = []
    
    # Governance -> Ownership
    for gov in gov_types:
        for own in own_types:
            count = len(df_clean[(df_clean['governance_type'] == gov) & 
                                 (df_clean['ownership_status'] == own)])
            if count > 0:
                flows.append({
                    'source': label_dict[gov],
                    'target': label_dict[f"{own}_own"],
                    'value': count
                })
    
    # Ownership -> Decentralization
    for own in own_types:
        for decent in decent_types:
            count = len(df_clean[(df_clean['ownership_status'] == own) & 
                                 (df_clean['level_of_decentralisation'] == decent)])
            if count > 0:
                flows.append({
                    'source': label_dict[f"{own}_own"],
                    'target': label_dict[f"{decent}_decent"],
                    'value': count
                })
    
    # Create Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=[l.replace('_own', '').replace('_decent', '') for l in labels],
            color=['lightblue']*len(gov_types) + 
                  ['lightgreen']*len(own_types) + 
                  ['lightcoral']*len(decent_types)
        ),
        link=dict(
            source=[f['source'] for f in flows],
            target=[f['target'] for f in flows],
            value=[f['value'] for f in flows]
        )
    )])
    
    fig.update_layout(
        title_text="Governance Flow: Type → Ownership → Decentralization",
        font_size=12,
        height=800
    )
    
    output_path = OUTPUT_DIR / '02_governance_sankey.html'
    fig.write_html(output_path)
    print(f"✓ Saved interactive Sankey: {output_path}")

def analyze_governance_token_type(df):
    """Analyze how governance dimensions vary by token type."""
    print("\n" + "="*60)
    print("GOVERNANCE BY TOKEN TYPE ANALYSIS")
    print("="*60)

    df_tok = df[df['has_token']].dropna(
        subset=['governance_type', 'level_of_decentralisation'])

    if len(df_tok) < 10:
        print("  Insufficient data for token type governance analysis")
        return

    print(f"Analyzing {len(df_tok)} DApps with tokens and governance data")

    # Governance score by token type
    gov_by_tt = df_tok.groupby('token_type_primary').agg({
        'governance_score': ['mean', 'median', 'count']
    })
    gov_by_tt.columns = ['mean', 'median', 'count']
    gov_by_tt = gov_by_tt.sort_values('mean', ascending=False)
    print("\nGovernance Score by Token Type:")
    print(gov_by_tt)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Governance Patterns by Token Type', fontsize=14, fontweight='bold')

    # 1. Governance score by token type
    ax = axes[0]
    colors = plt.cm.viridis(np.linspace(0, 1, len(gov_by_tt)))
    ax.barh(range(len(gov_by_tt)), gov_by_tt['mean'], color=colors)
    ax.set_yticks(range(len(gov_by_tt)))
    ax.set_yticklabels(gov_by_tt.index)
    ax.set_xlabel('Average Governance Score')
    ax.set_title('Governance Score by Token Type', fontsize=12, fontweight='bold')
    ax.invert_yaxis()
    for i, (idx, row) in enumerate(gov_by_tt.iterrows()):
        ax.text(row['mean'] + 0.005, i,
                f"{row['mean']:.2f} (n={int(row['count'])})",
                va='center', fontsize=9)

    # 2. Decentralisation breakdown per token type
    ax = axes[1]
    ct = pd.crosstab(df_tok['token_type_primary'],
                     df_tok['level_of_decentralisation'],
                     normalize='index') * 100
    dec_order = ['CENTRALIZED', 'SEMI_DECENTRALIZED', 'DECENTRALIZED']
    dec_cols = [c for c in dec_order if c in ct.columns]
    ct[dec_cols].plot(kind='barh', stacked=True, ax=ax,
                     color=['#d62728', '#ff7f0e', '#2ca02c'])
    ax.set_xlabel('Percentage (%)')
    ax.set_title('Decentralisation by Token Type', fontsize=12, fontweight='bold')
    ax.legend(title='Level', fontsize=8, bbox_to_anchor=(1.05, 1))

    plt.tight_layout()
    output_path = OUTPUT_DIR / '02_governance_token_type.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()


def generate_governance_insights(df):
    """Generate key insights about governance."""
    print("\n" + "="*60)
    print("KEY GOVERNANCE INSIGHTS")
    print("="*60)
    
    df_clean = df.dropna(subset=['governance_type', 'ownership_status', 'level_of_decentralisation'])
    
    # Insight 1: The Centralization Reality
    centralized_pct = (df_clean['level_of_decentralisation'] == 'CENTRALIZED').mean() * 100
    semi_decent_pct = (df_clean['level_of_decentralisation'] == 'SEMI_DECENTRALIZED').mean() * 100
    truly_decent_pct = (df_clean['level_of_decentralisation'] == 'DECENTRALIZED').mean() * 100
    
    print(f"\n1. THE CENTRALIZATION REALITY:")
    print(f"   - Only {truly_decent_pct:.1f}% of DApps are truly decentralized")
    print(f"   - {centralized_pct:.1f}% remain centralized")
    print(f"   - {semi_decent_pct:.1f}% are semi-decentralized")
    
    # Insight 2: Company ownership dominance
    company_owned_pct = (df_clean['ownership_status'] == 'COMPANY_OWNED').mean() * 100
    dao_owned_pct = (df_clean['ownership_status'] == 'DAO_OWNED').mean() * 100
    
    print(f"\n2. OWNERSHIP CONCENTRATION:")
    print(f"   - {company_owned_pct:.1f}% are company-owned")
    print(f"   - Only {dao_owned_pct:.1f}% are DAO-owned")
    print(f"   - {company_owned_pct/dao_owned_pct:.1f}x more company-owned than DAO-owned")
    
    # Insight 3: Governance paradox
    team_controlled = (df_clean['governance_type'] == 'TEAM_CONTROLLED').sum()
    snapshot = (df_clean['governance_type'] == 'SNAPSHOT_OFFCHAIN').sum()
    onchain = (df_clean['governance_type'] == 'ONCHAIN_TOKEN_GOVERNANCE').sum()
    
    print(f"\n3. GOVERNANCE PARADOX:")
    print(f"   - {team_controlled} DApps are team-controlled")
    print(f"   - {snapshot} use off-chain voting (non-binding)")
    print(f"   - Only {onchain} have on-chain token governance")
    
    # Insight 4: Category variations
    top_cats = df_clean['dapp_category'].value_counts().head(3)
    for cat in top_cats.index:
        cat_data = df_clean[df_clean['dapp_category'] == cat]
        avg_score = cat_data['governance_score'].mean()
        print(f"\n4. {cat} Category:")
        print(f"   - Average governance score: {avg_score:.2f}")
        print(f"   - Decentralization: {cat_data['level_of_decentralisation'].value_counts().to_dict()}")
    
    return {
        'truly_decentralized_pct': truly_decent_pct,
        'company_owned_pct': company_owned_pct,
        'dao_owned_pct': dao_owned_pct,
        'team_controlled_count': team_controlled
    }

def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("GOVERNANCE & DECENTRALIZATION ANALYSIS")
    print("="*60)
    
    # Load data
    df = load_prepared_data()
    
    # Run analyses
    analyze_governance_distribution(df)
    analyze_governance_cross_tabulation(df)
    analyze_governance_by_category(df)
    analyze_governance_market_correlation(df)
    create_sankey_diagram(df)
    analyze_governance_token_type(df)
    insights = generate_governance_insights(df)
    
    print("\n" + "="*60)
    print("GOVERNANCE ANALYSIS COMPLETE!")
    print("="*60)
    print("\n✓ All visualizations saved to:", OUTPUT_DIR)
    
    return insights

if __name__ == "__main__":
    insights = main()

