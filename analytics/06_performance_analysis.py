"""
DApp Ecosystem Analysis - Performance Metrics & Efficiency
===========================================================
This script analyzes TVL, liquidity metrics, and efficiency ratios
across the DApp ecosystem.

Key Message Target: "Performance efficiency tiers" - identifying 
high-performing vs struggling DApps
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
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

def analyze_tvl_metrics(df):
    """Analyze Total Value Locked metrics."""
    print("\n" + "="*60)
    print("TVL ANALYSIS")
    print("="*60)
    
    df_tvl = df[df['tvl'] > 0].copy()
    print(f"\nAnalyzing {len(df_tvl)} DApps with TVL data...")
    
    # Statistics
    print(f"\nTVL Statistics:")
    print(f"  Total TVL: ${df_tvl['tvl'].sum():,.0f}")
    print(f"  Mean: ${df_tvl['tvl'].mean():,.0f}")
    print(f"  Median: ${df_tvl['tvl'].median():,.0f}")
    
    # Top DApps by TVL
    top_10_tvl = df_tvl.nlargest(10, 'tvl')
    print(f"\nTop 10 DApps by TVL:")
    for i, (idx, row) in enumerate(top_10_tvl.iterrows(), 1):
        print(f"  {i}. {row['name']}: ${row['tvl']:,.0f}")
    
    # TVL by category
    if 'dapp_category' in df_tvl.columns:
        tvl_by_cat = df_tvl.groupby('dapp_category')['tvl'].agg(['sum', 'mean', 'count'])
        tvl_by_cat = tvl_by_cat.sort_values('sum', ascending=False).head(10)
        print(f"\nTVL by Category (Top 10):")
        print(tvl_by_cat)
    
    # TVL efficiency
    df_tvl['tvl_per_user'] = np.where(df_tvl['users'] > 0, df_tvl['tvl'] / df_tvl['users'], 0)
    
    print(f"\nTVL Efficiency (TVL per User):")
    print(f"  Mean: ${df_tvl[df_tvl['tvl_per_user'] > 0]['tvl_per_user'].mean():,.2f}")
    print(f"  Median: ${df_tvl[df_tvl['tvl_per_user'] > 0]['tvl_per_user'].median():,.2f}")
    
    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('TVL Analysis & Distribution', fontsize=14, fontweight='bold')
    
    # Plot 1: TVL distribution
    ax1 = axes[0, 0]
    ax1.hist(df_tvl['tvl'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
    ax1.set_xscale('log')
    ax1.set_xlabel('TVL (USD, log scale)', fontsize=10)
    ax1.set_ylabel('Number of DApps', fontsize=10)
    ax1.set_title('TVL Distribution', fontsize=11, fontweight='bold')
    
    # Plot 2: Top 15 by TVL
    ax2 = axes[0, 1]
    top_15 = df_tvl.nlargest(15, 'tvl')
    colors = plt.cm.viridis(np.linspace(0, 1, len(top_15)))
    ax2.barh(range(len(top_15)), top_15['tvl'], color=colors)
    ax2.set_yticks(range(len(top_15)))
    ax2.set_yticklabels(top_15['name'], fontsize=8)
    ax2.set_xlabel('TVL (USD)', fontsize=10)
    ax2.set_title('Top 15 DApps by TVL', fontsize=11, fontweight='bold')
    ax2.invert_yaxis()
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e9:.1f}B'))
    
    # Plot 3: TVL vs Users
    ax3 = axes[1, 0]
    df_plot = df_tvl[(df_tvl['users'] > 0) & (df_tvl['market_cap'] > 0)]
    scatter = ax3.scatter(df_plot['users'], df_plot['tvl'],
                         alpha=0.5, s=50, c=df_plot['market_cap'], cmap='plasma',
                         norm=plt.Normalize(vmin=0, vmax=df_plot['market_cap'].quantile(0.95)))
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.set_xlabel('Active Users (log scale)', fontsize=10)
    ax3.set_ylabel('TVL (USD, log scale)', fontsize=10)
    ax3.set_title('TVL vs User Base', fontsize=11, fontweight='bold')
    cbar = plt.colorbar(scatter, ax=ax3)
    cbar.set_label('Market Cap', fontsize=9)
    
    # Plot 4: TVL by category
    ax4 = axes[1, 1]
    if 'tvl_by_cat' in locals():
        top_cats = tvl_by_cat.head(10)
        colors = plt.cm.plasma(np.linspace(0, 1, len(top_cats)))
        ax4.barh(range(len(top_cats)), top_cats['sum'], color=colors)
        ax4.set_yticks(range(len(top_cats)))
        ax4.set_yticklabels(top_cats.index, fontsize=9)
        ax4.set_xlabel('Total TVL (USD)', fontsize=10)
        ax4.set_title('TVL by Category', fontsize=11, fontweight='bold')
        ax4.invert_yaxis()
        ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e9:.1f}B'))
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '06_tvl_analysis.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()

def analyze_efficiency_ratios(df):
    """Analyze efficiency ratios across DApps."""
    print("\n" + "="*60)
    print("EFFICIENCY RATIOS ANALYSIS")
    print("="*60)
    
    df_eff = df[(df['users'] > 0)].copy()
    
    # Calculate efficiency metrics
    df_eff['tvl_per_user'] = np.where(df_eff['tvl'] > 0, df_eff['tvl'] / df_eff['users'], 0)
    df_eff['mcap_per_user'] = np.where(df_eff['market_cap'] > 0, df_eff['market_cap'] / df_eff['users'], 0)
    df_eff['tvl_per_tx'] = np.where((df_eff['tvl'] > 0) & (df_eff['transactions'] > 0), 
                                    df_eff['tvl'] / df_eff['transactions'], 0)
    
    print(f"\nEfficiency Metrics:")
    print(f"  TVL per User - Median: ${df_eff[df_eff['tvl_per_user'] > 0]['tvl_per_user'].median():,.2f}")
    print(f"  Volume per Transaction - Median: ${df_eff[df_eff['volume_per_user'] > 0]['volume_per_user'].median():,.2f}")
    print(f"  Market Cap per User - Median: ${df_eff[df_eff['mcap_per_user'] > 0]['mcap_per_user'].median():,.2f}")
    
    # Efficiency by category
    if 'dapp_category' in df_eff.columns:
        top_cats = df_eff['dapp_category'].value_counts().head(8).index
        eff_by_cat = df_eff[df_eff['dapp_category'].isin(top_cats)].groupby('dapp_category').agg({
            'tvl_per_user': 'median',
            'volume_per_user': 'median',
            'tx_per_user': 'median',
            'mcap_per_user': 'median'
        })
        
        print(f"\nMedian Efficiency by Category:")
        print(eff_by_cat)
    
    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Efficiency Ratios Analysis', fontsize=14, fontweight='bold')
    
    # Plot 1: TVL per user vs Market cap per user
    ax1 = axes[0, 0]
    df_plot1 = df_eff[(df_eff['tvl_per_user'] > 0) & (df_eff['mcap_per_user'] > 0)]
    df_plot1 = df_plot1[(df_plot1['tvl_per_user'] < df_plot1['tvl_per_user'].quantile(0.95)) &
                        (df_plot1['mcap_per_user'] < df_plot1['mcap_per_user'].quantile(0.95))]
    
    scatter = ax1.scatter(df_plot1['mcap_per_user'], df_plot1['tvl_per_user'],
                         alpha=0.5, s=50, c=df_plot1['governance_score'], cmap='viridis')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('Market Cap per User (USD, log scale)', fontsize=10)
    ax1.set_ylabel('TVL per User (USD, log scale)', fontsize=10)
    ax1.set_title('Capital Efficiency: TVL vs Market Cap per User', fontsize=11, fontweight='bold')
    cbar = plt.colorbar(scatter, ax=ax1)
    cbar.set_label('Governance Score', fontsize=9)
    
    # Plot 2: Efficiency frontier (Volume per user vs Tx per user)
    ax2 = axes[0, 1]
    df_plot2 = df_eff[(df_eff['volume_per_user'] > 0) & (df_eff['tx_per_user'] > 0)]
    df_plot2 = df_plot2[(df_plot2['volume_per_user'] < df_plot2['volume_per_user'].quantile(0.95)) &
                        (df_plot2['tx_per_user'] < df_plot2['tx_per_user'].quantile(0.95))]
    
    scatter2 = ax2.scatter(df_plot2['tx_per_user'], df_plot2['volume_per_user'],
                          alpha=0.5, s=50, c=df_plot2['users'], cmap='plasma',
                          norm=plt.Normalize(vmin=0, vmax=df_plot2['users'].quantile(0.95)))
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('Transactions per User (log scale)', fontsize=10)
    ax2.set_ylabel('Volume per User (USD, log scale)', fontsize=10)
    ax2.set_title('Efficiency Frontier: Activity vs Value', fontsize=11, fontweight='bold')
    cbar2 = plt.colorbar(scatter2, ax=ax2)
    cbar2.set_label('User Base', fontsize=9)
    
    # Plot 3: Efficiency by category (radar-like comparison)
    ax3 = axes[1, 0]
    if 'eff_by_cat' in locals() and 'top_cats' in locals():
        # Normalize for comparison
        eff_norm = eff_by_cat.copy()
        for col in eff_norm.columns:
            max_val = eff_norm[col].max()
            if max_val > 0:
                eff_norm[col] = eff_norm[col] / max_val
        
        x = np.arange(len(eff_norm.columns))
        width = 0.15
        
        for i, (idx, row) in enumerate(eff_norm.head(5).iterrows()):
            ax3.bar(x + i*width, row.values, width, label=idx, alpha=0.8)
        
        ax3.set_ylabel('Normalized Efficiency Score', fontsize=10)
        ax3.set_title('Efficiency Profile by Category (Top 5)', fontsize=11, fontweight='bold')
        ax3.set_xticks(x + width * 2)
        ax3.set_xticklabels(['TVL/User', 'Vol/User', 'Tx/User', 'MCap/User'], fontsize=9, rotation=45)
        ax3.legend(fontsize=8, loc='upper left')
        ax3.grid(True, alpha=0.3)
    
    # Plot 4: Liquidity efficiency (TVL/Market Cap)
    ax4 = axes[1, 1]
    df_liq = df_eff[(df_eff['liquidity_efficiency'] > 0) &
                    (df_eff['liquidity_efficiency'] < df_eff['liquidity_efficiency'].quantile(0.95))]
    
    ax4.hist(df_liq['liquidity_efficiency'], bins=50, color='coral', edgecolor='black', alpha=0.7)
    ax4.axvline(df_liq['liquidity_efficiency'].median(), color='red', linestyle='--',
               linewidth=2, label=f'Median: {df_liq["liquidity_efficiency"].median():.4f}')
    ax4.set_xlabel('Liquidity Efficiency (TVL / Market Cap)', fontsize=10)
    ax4.set_ylabel('Number of DApps', fontsize=10)
    ax4.set_title('Liquidity Efficiency Distribution', fontsize=11, fontweight='bold')
    ax4.legend()
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '06_efficiency_ratios.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()

def perform_performance_clustering(df):
    """Cluster DApps by performance metrics."""
    print("\n" + "="*60)
    print("PERFORMANCE CLUSTERING ANALYSIS")
    print("="*60)
    
    # Select DApps with complete performance data
    df_perf = df[(df['users'] > 0) & (df['market_cap'] > 0)].copy()
    
    # Select performance features
    features = ['users', 'market_cap', 'tvl', 'volume', 'transactions', 
                'governance_score', 'market_maturity']
    
    df_features = df_perf[features].copy()
    
    # Log transform and handle missing
    for col in features:
        if col not in ['governance_score', 'market_maturity']:
            df_features[f'{col}_log'] = np.log1p(df_features[col].fillna(0))
        else:
            df_features[f'{col}_log'] = df_features[col].fillna(0)
    
    # Standardize
    scaler = StandardScaler()
    feature_cols = [f'{col}_log' for col in features]
    X = scaler.fit_transform(df_features[feature_cols])
    
    # K-means clustering
    n_clusters = 4
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df_perf['perf_cluster'] = kmeans.fit_predict(X)
    
    print(f"\nClustered {len(df_perf)} DApps into {n_clusters} performance tiers...")
    
    # Analyze clusters
    cluster_names = ['Struggling', 'Emerging', 'Growing', 'Leading']
    
    for i in range(n_clusters):
        cluster_data = df_perf[df_perf['perf_cluster'] == i]
        print(f"\nCluster {i} - {cluster_names[i]} ({len(cluster_data)} DApps):")
        print(f"  Avg Users: {cluster_data['users'].mean():,.0f}")
        print(f"  Avg Market Cap: ${cluster_data['market_cap'].mean():,.0f}")
        print(f"  Avg TVL: ${cluster_data['tvl'].mean():,.0f}")
        print(f"  Avg Governance Score: {cluster_data['governance_score'].mean():.2f}")
        print(f"  Avg Market Maturity: {cluster_data['market_maturity'].mean():.2f}")
    
    # PCA for visualization
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    
    print(f"\nPCA Explained Variance: {pca.explained_variance_ratio_.sum():.2%}")
    
    # Visualize
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Performance Clustering Analysis', fontsize=14, fontweight='bold')
    
    # Plot 1: PCA visualization
    ax1 = axes[0]
    colors = plt.cm.Set3(np.linspace(0, 1, n_clusters))
    
    for i in range(n_clusters):
        cluster_mask = df_perf['perf_cluster'] == i
        ax1.scatter(X_pca[cluster_mask, 0], X_pca[cluster_mask, 1],
                   label=f'{cluster_names[i]} (n={cluster_mask.sum()})',
                   alpha=0.6, s=50, color=colors[i])
    
    ax1.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})', fontsize=10)
    ax1.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})', fontsize=10)
    ax1.set_title('Performance Clusters (PCA)', fontsize=11, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Cluster comparison (Market Cap vs Users)
    ax2 = axes[1]
    
    for i in range(n_clusters):
        cluster_data = df_perf[df_perf['perf_cluster'] == i]
        ax2.scatter(cluster_data['users'], cluster_data['market_cap'],
                   label=f'{cluster_names[i]} (n={len(cluster_data)})',
                   alpha=0.6, s=50, color=colors[i])
    
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('Active Users (log scale)', fontsize=10)
    ax2.set_ylabel('Market Cap (USD, log scale)', fontsize=10)
    ax2.set_title('Performance Tiers: Users vs Market Cap', fontsize=11, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '06_performance_clustering.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()

def generate_performance_insights(df):
    """Generate key insights about performance."""
    print("\n" + "="*60)
    print("KEY PERFORMANCE INSIGHTS")
    print("="*60)
    
    df_tvl = df[df['tvl'] > 0]
    df_eff = df[(df['users'] > 0) & (df['tvl'] > 0)].copy()
    
    # Calculate tvl_per_user
    df_eff['tvl_per_user'] = df_eff['tvl'] / df_eff['users']
    
    # Insight 1: TVL concentration
    total_tvl = df_tvl['tvl'].sum()
    top_10_tvl = df_tvl.nlargest(10, 'tvl')['tvl'].sum()
    top_10_pct = top_10_tvl / total_tvl * 100
    
    print(f"\n1. TVL CONCENTRATION:")
    print(f"   - Top 10 DApps control {top_10_pct:.1f}% of total TVL")
    print(f"   - Total TVL: ${total_tvl:,.0f}")
    
    # Insight 2: Efficiency variance
    median_tvl_per_user = df_eff['tvl_per_user'].median()
    
    print(f"\n2. CAPITAL EFFICIENCY:")
    print(f"   - Median TVL per user: ${median_tvl_per_user:,.2f}")
    print(f"   - Wide variance in capital deployment efficiency")
    
    return {
        'tvl_concentration': top_10_pct,
        'median_tvl_per_user': median_tvl_per_user
    }

def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("PERFORMANCE METRICS & EFFICIENCY ANALYSIS")
    print("="*60)
    
    # Load data
    df = load_prepared_data()
    
    # Run analyses
    analyze_tvl_metrics(df)
    analyze_efficiency_ratios(df)
    perform_performance_clustering(df)
    insights = generate_performance_insights(df)
    
    print("\n" + "="*60)
    print("PERFORMANCE ANALYSIS COMPLETE!")
    print("="*60)
    print("\n✓ All visualizations saved to:", OUTPUT_DIR)
    
    return insights

if __name__ == "__main__":
    insights = main()

