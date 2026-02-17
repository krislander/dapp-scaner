"""
DApp Ecosystem Analysis - User Adoption & Engagement Analysis
==============================================================
This script analyzes user adoption patterns, engagement metrics,
and transaction behaviors across the DApp ecosystem.

Key Message Target: "User engagement archetypes" - different patterns 
of how users interact with DApp categories
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
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

def analyze_user_distribution(df):
    """Analyze user base distribution across DApps."""
    print("\n" + "="*60)
    print("USER DISTRIBUTION ANALYSIS")
    print("="*60)
    
    df_users = df[df['users'] > 0].copy()
    print(f"\nAnalyzing {len(df_users)} DApps with user data...")
    
    # Statistics
    print(f"\nUser Statistics:")
    print(f"  Total Users: {df_users['users'].sum():,.0f}")
    print(f"  Mean: {df_users['users'].mean():,.0f}")
    print(f"  Median: {df_users['users'].median():,.0f}")
    print(f"  Std Dev: {df_users['users'].std():,.0f}")
    
    # User concentration
    df_sorted = df_users.sort_values('users', ascending=False)
    total_users = df_sorted['users'].sum()
    
    top_10_users = df_sorted.head(10)['users'].sum()
    top_10_pct = top_10_users / total_users * 100
    
    top_50_users = df_sorted.head(50)['users'].sum()
    top_50_pct = top_50_users / total_users * 100
    
    print(f"\nUser Concentration:")
    print(f"  Top 10 DApps: {top_10_users:,.0f} users ({top_10_pct:.1f}% of total)")
    print(f"  Top 50 DApps: {top_50_users:,.0f} users ({top_50_pct:.1f}% of total)")
    
    # Top 10 by users
    top_10 = df_sorted.head(10)
    print(f"\nTop 10 DApps by Active Users:")
    for i, (idx, row) in enumerate(top_10.iterrows(), 1):
        print(f"  {i}. {row['name']}: {row['users']:,.0f} users")
    
    # Users by category
    if 'dapp_category' in df_users.columns:
        users_by_cat = df_users.groupby('dapp_category')['users'].agg(['sum', 'mean', 'count'])
        users_by_cat = users_by_cat.sort_values('sum', ascending=False).head(10)
        
        print(f"\nTop 10 Categories by Total Users:")
        print(users_by_cat)
    
    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('User Adoption & Distribution Analysis', fontsize=14, fontweight='bold')
    
    # Plot 1: User distribution (log scale)
    ax1 = axes[0, 0]
    ax1.hist(df_users['users'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
    ax1.set_xscale('log')
    ax1.set_xlabel('Active Users (log scale)', fontsize=10)
    ax1.set_ylabel('Number of DApps', fontsize=10)
    ax1.set_title('User Base Distribution (Log Scale)', fontsize=11, fontweight='bold')
    ax1.axvline(df_users['users'].median(), color='red', linestyle='--', 
               linewidth=2, label=f'Median: {df_users["users"].median():,.0f}')
    ax1.legend()
    
    # Plot 2: Cumulative user concentration
    ax2 = axes[0, 1]
    df_sorted['cumulative_pct'] = df_sorted['users'].cumsum() / total_users * 100
    df_sorted['rank_pct'] = np.arange(1, len(df_sorted) + 1) / len(df_sorted) * 100
    
    ax2.plot(df_sorted['rank_pct'], df_sorted['cumulative_pct'], linewidth=2, color='darkgreen')
    ax2.plot([0, 100], [0, 100], '--', color='gray', alpha=0.5, label='Perfect Equality')
    ax2.fill_between(df_sorted['rank_pct'], 0, df_sorted['cumulative_pct'], alpha=0.3, color='green')
    ax2.set_xlabel('DApps Ranked by Users (%)', fontsize=10)
    ax2.set_ylabel('Cumulative Users (%)', fontsize=10)
    ax2.set_title('Lorenz Curve: User Concentration', fontsize=11, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Top 15 DApps by users
    ax3 = axes[1, 0]
    top_15 = df_sorted.head(15)
    colors = plt.cm.viridis(np.linspace(0, 1, len(top_15)))
    ax3.barh(range(len(top_15)), top_15['users'], color=colors)
    ax3.set_yticks(range(len(top_15)))
    ax3.set_yticklabels(top_15['name'], fontsize=8)
    ax3.set_xlabel('Active Users', fontsize=10)
    ax3.set_title('Top 15 DApps by User Base', fontsize=11, fontweight='bold')
    ax3.invert_yaxis()
    ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
    
    # Plot 4: Users by category
    ax4 = axes[1, 1]
    if 'users_by_cat' in locals():
        top_cats = users_by_cat.head(10)
        colors = plt.cm.plasma(np.linspace(0, 1, len(top_cats)))
        ax4.barh(range(len(top_cats)), top_cats['sum'], color=colors)
        ax4.set_yticks(range(len(top_cats)))
        ax4.set_yticklabels(top_cats.index, fontsize=9)
        ax4.set_xlabel('Total Active Users', fontsize=10)
        ax4.set_title('Total Users by Category (Top 10)', fontsize=11, fontweight='bold')
        ax4.invert_yaxis()
        ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '05_user_distribution.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()
    
    return top_10_pct

def analyze_engagement_patterns(df):
    """Analyze user engagement patterns."""
    print("\n" + "="*60)
    print("ENGAGEMENT PATTERNS ANALYSIS")
    print("="*60)
    
    df_engagement = df[(df['users'] > 0) & (df['transactions'] > 0)].copy()
    print(f"\nAnalyzing {len(df_engagement)} DApps with engagement data...")
    
    # Transactions per user
    print(f"\nTransactions per User:")
    print(f"  Mean: {df_engagement['tx_per_user'].mean():.2f}")
    print(f"  Median: {df_engagement['tx_per_user'].median():.2f}")
    
    # Volume per user
    df_vol_per_user = df_engagement[df_engagement['volume_per_user'] > 0]
    print(f"\nVolume per User:")
    print(f"  Mean: ${df_vol_per_user['volume_per_user'].mean():,.2f}")
    print(f"  Median: ${df_vol_per_user['volume_per_user'].median():.2f}")
    
    # Engagement categories
    df_engagement['engagement_type'] = 'Low'
    df_engagement.loc[df_engagement['tx_per_user'] > df_engagement['tx_per_user'].median(), 'engagement_type'] = 'High'
    
    print(f"\nEngagement Distribution:")
    print(df_engagement['engagement_type'].value_counts())
    
    # Engagement by category
    if 'dapp_category' in df_engagement.columns:
        top_cats = df_engagement['dapp_category'].value_counts().head(8).index
        engagement_by_cat = df_engagement[df_engagement['dapp_category'].isin(top_cats)].groupby('dapp_category').agg({
            'tx_per_user': ['mean', 'median'],
            'volume_per_user': ['mean', 'median'],
            'users': 'mean'
        })
        
        print(f"\nEngagement Metrics by Category:")
        print(engagement_by_cat)
    
    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('User Engagement Patterns', fontsize=14, fontweight='bold')
    
    # Plot 1: Users vs Transactions scatter
    ax1 = axes[0, 0]
    scatter1 = ax1.scatter(df_engagement['users'], df_engagement['transactions'],
                          alpha=0.5, s=50, c=df_engagement['volume'], cmap='viridis',
                          norm=plt.Normalize(vmin=0, vmax=df_engagement['volume'].quantile(0.95)))
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('Active Users (log scale)', fontsize=10)
    ax1.set_ylabel('Transactions (log scale)', fontsize=10)
    ax1.set_title('Users vs Transactions', fontsize=11, fontweight='bold')
    cbar1 = plt.colorbar(scatter1, ax=ax1)
    cbar1.set_label('Trading Volume', fontsize=9)
    
    # Add diagonal line for reference
    x_range = [df_engagement['users'].min(), df_engagement['users'].max()]
    ax1.plot(x_range, x_range, 'r--', alpha=0.5, label='1 tx per user')
    ax1.legend()
    
    # Plot 2: Transactions per user distribution
    ax2 = axes[0, 1]
    tx_per_user_clean = df_engagement[df_engagement['tx_per_user'] < df_engagement['tx_per_user'].quantile(0.95)]
    ax2.hist(tx_per_user_clean['tx_per_user'], bins=50, color='orange', edgecolor='black', alpha=0.7)
    ax2.axvline(tx_per_user_clean['tx_per_user'].median(), color='red', linestyle='--',
               linewidth=2, label=f'Median: {tx_per_user_clean["tx_per_user"].median():.2f}')
    ax2.set_xlabel('Transactions per User', fontsize=10)
    ax2.set_ylabel('Number of DApps', fontsize=10)
    ax2.set_title('Transaction Intensity Distribution', fontsize=11, fontweight='bold')
    ax2.legend()
    
    # Plot 3: Users vs Volume per User
    ax3 = axes[1, 0]
    df_vol_clean = df_engagement[(df_engagement['volume_per_user'] > 0) &
                                  (df_engagement['volume_per_user'] < df_engagement['volume_per_user'].quantile(0.95))]
    
    scatter2 = ax3.scatter(df_vol_clean['users'], df_vol_clean['volume_per_user'],
                          alpha=0.5, s=50, c=df_vol_clean['tx_per_user'], cmap='plasma')
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.set_xlabel('Active Users (log scale)', fontsize=10)
    ax3.set_ylabel('Volume per User (USD, log scale)', fontsize=10)
    ax3.set_title('User Base vs Economic Activity per User', fontsize=11, fontweight='bold')
    cbar2 = plt.colorbar(scatter2, ax=ax3)
    cbar2.set_label('Tx per User', fontsize=9)
    
    # Plot 4: Engagement by category
    ax4 = axes[1, 1]
    if 'engagement_by_cat' in locals() and 'top_cats' in locals():
        cat_tx = df_engagement[df_engagement['dapp_category'].isin(top_cats)].groupby('dapp_category')['tx_per_user'].median()
        cat_tx = cat_tx.sort_values(ascending=True)
        
        colors = plt.cm.coolwarm(np.linspace(0, 1, len(cat_tx)))
        ax4.barh(range(len(cat_tx)), cat_tx.values, color=colors)
        ax4.set_yticks(range(len(cat_tx)))
        ax4.set_yticklabels(cat_tx.index, fontsize=9)
        ax4.set_xlabel('Median Transactions per User', fontsize=10)
        ax4.set_title('Engagement Intensity by Category', fontsize=11, fontweight='bold')
        ax4.invert_yaxis()
        
        # Add value labels
        for i, v in enumerate(cat_tx.values):
            ax4.text(v + 0.5, i, f'{v:.1f}', va='center', fontsize=8)
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '05_engagement_patterns.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()

def analyze_category_engagement(df):
    """Deep dive into engagement patterns by category."""
    print("\n" + "="*60)
    print("CATEGORY-SPECIFIC ENGAGEMENT ANALYSIS")
    print("="*60)
    
    df_analysis = df[(df['users'] > 0) & (df['dapp_category'].notna())].copy()
    
    # Focus on top categories
    top_cats = df_analysis['dapp_category'].value_counts().head(6).index
    df_top = df_analysis[df_analysis['dapp_category'].isin(top_cats)]
    
    print(f"\nComparing engagement across {len(top_cats)} major categories...")
    
    # Create comparison metrics
    comparison = df_top.groupby('dapp_category').agg({
        'users': ['sum', 'mean', 'median'],
        'transactions': ['sum', 'mean', 'median'],
        'volume': ['sum', 'mean', 'median'],
        'tx_per_user': ['mean', 'median'],
        'volume_per_user': ['mean', 'median']
    })
    
    print(f"\nCategory Engagement Comparison:")
    print(comparison)
    
    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Category-Specific Engagement Patterns', fontsize=14, fontweight='bold')
    
    # Plot 1: Box plot - Users by category
    ax1 = axes[0, 0]
    df_top_plot1 = df_top[df_top['users'] > 0]
    box_data1 = [df_top_plot1[df_top_plot1['dapp_category'] == cat]['users'].values 
                 for cat in top_cats]
    bp1 = ax1.boxplot(box_data1, labels=top_cats, patch_artist=True)
    for patch in bp1['boxes']:
        patch.set_facecolor('lightblue')
    ax1.set_yscale('log')
    ax1.set_ylabel('Active Users (log scale)', fontsize=10)
    ax1.set_title('User Base Distribution by Category', fontsize=11, fontweight='bold')
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=8)
    
    # Plot 2: Box plot - Transactions per user by category
    ax2 = axes[0, 1]
    df_top_plot2 = df_top[df_top['tx_per_user'] > 0]
    box_data2 = [df_top_plot2[df_top_plot2['dapp_category'] == cat]['tx_per_user'].values 
                 for cat in top_cats]
    bp2 = ax2.boxplot(box_data2, labels=top_cats, patch_artist=True)
    for patch in bp2['boxes']:
        patch.set_facecolor('lightcoral')
    ax2.set_yscale('log')
    ax2.set_ylabel('Transactions per User (log scale)', fontsize=10)
    ax2.set_title('Transaction Intensity by Category', fontsize=11, fontweight='bold')
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=8)
    
    # Plot 3: Scatter - Category comparison (Users vs Volume per User)
    ax3 = axes[1, 0]
    for cat in top_cats:
        cat_data = df_top[(df_top['dapp_category'] == cat) & (df_top['volume_per_user'] > 0)]
        ax3.scatter(cat_data['users'], cat_data['volume_per_user'],
                   label=cat, alpha=0.6, s=60)
    
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.set_xlabel('Active Users (log scale)', fontsize=10)
    ax3.set_ylabel('Volume per User (USD, log scale)', fontsize=10)
    ax3.set_title('User Scale vs Economic Value', fontsize=11, fontweight='bold')
    ax3.legend(fontsize=8, loc='best')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Engagement quadrant by category
    ax4 = axes[1, 1]
    cat_summary = df_top.groupby('dapp_category').agg({
        'users': 'median',
        'tx_per_user': 'median'
    })
    
    ax4.scatter(cat_summary['users'], cat_summary['tx_per_user'], s=200, alpha=0.6)
    
    # Add category labels
    for idx, row in cat_summary.iterrows():
        ax4.annotate(idx, (row['users'], row['tx_per_user']),
                    fontsize=9, ha='center', va='center')
    
    # Add quadrant lines
    median_users = cat_summary['users'].median()
    median_tx = cat_summary['tx_per_user'].median()
    ax4.axhline(median_tx, color='gray', linestyle='--', alpha=0.5)
    ax4.axvline(median_users, color='gray', linestyle='--', alpha=0.5)
    
    # Add quadrant labels
    ax4.text(median_users * 10, median_tx * 10, 'High Users\nHigh Engagement',
            fontsize=9, alpha=0.7, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    ax4.text(median_users * 0.1, median_tx * 10, 'Low Users\nHigh Engagement',
            fontsize=9, alpha=0.7, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    ax4.set_xscale('log')
    ax4.set_yscale('log')
    ax4.set_xlabel('Median Active Users (log scale)', fontsize=10)
    ax4.set_ylabel('Median Tx per User (log scale)', fontsize=10)
    ax4.set_title('Engagement Archetype by Category', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '05_category_engagement.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()

def perform_engagement_clustering(df):
    """Cluster DApps by engagement patterns."""
    print("\n" + "="*60)
    print("ENGAGEMENT CLUSTERING ANALYSIS")
    print("="*60)
    
    # Prepare data for clustering
    df_cluster = df[(df['users'] > 0) & (df['transactions'] > 0) & (df['volume'] > 0)].copy()
    
    # Select features
    features = ['users', 'transactions', 'volume', 'tx_per_user', 'volume_per_user']
    df_features = df_cluster[features].copy()
    
    # Log transform
    for col in features:
        df_features[f'{col}_log'] = np.log1p(df_features[col])
    
    # Standardize
    scaler = StandardScaler()
    feature_cols = [f'{col}_log' for col in features]
    X = scaler.fit_transform(df_features[feature_cols])
    
    # K-means clustering
    n_clusters = 4
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df_cluster['cluster'] = kmeans.fit_predict(X)
    
    print(f"\nClustered {len(df_cluster)} DApps into {n_clusters} engagement groups...")
    
    # Analyze clusters
    for i in range(n_clusters):
        cluster_data = df_cluster[df_cluster['cluster'] == i]
        print(f"\nCluster {i} ({len(cluster_data)} DApps):")
        print(f"  Avg Users: {cluster_data['users'].mean():,.0f}")
        print(f"  Avg Transactions: {cluster_data['transactions'].mean():,.0f}")
        print(f"  Avg Volume: ${cluster_data['volume'].mean():,.0f}")
        print(f"  Avg Tx/User: {cluster_data['tx_per_user'].mean():.2f}")
        
        # Top categories in cluster
        if 'dapp_category' in cluster_data.columns:
            top_cats = cluster_data['dapp_category'].value_counts().head(3)
            print(f"  Top Categories: {', '.join([f'{cat} ({count})' for cat, count in top_cats.items()])}")
    
    # Visualize
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Engagement Clustering Analysis', fontsize=14, fontweight='bold')
    
    # Plot 1: Cluster scatter (Users vs Tx per User)
    ax1 = axes[0]
    colors = plt.cm.Set3(np.linspace(0, 1, n_clusters))
    
    for i in range(n_clusters):
        cluster_data = df_cluster[df_cluster['cluster'] == i]
        ax1.scatter(cluster_data['users'], cluster_data['tx_per_user'],
                   label=f'Cluster {i} (n={len(cluster_data)})',
                   alpha=0.6, s=50, color=colors[i])
    
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('Active Users (log scale)', fontsize=10)
    ax1.set_ylabel('Transactions per User (log scale)', fontsize=10)
    ax1.set_title('Engagement Clusters: Users vs Tx Intensity', fontsize=11, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Cluster scatter (Volume vs Volume per User)
    ax2 = axes[1]
    
    for i in range(n_clusters):
        cluster_data = df_cluster[df_cluster['cluster'] == i]
        ax2.scatter(cluster_data['volume'], cluster_data['volume_per_user'],
                   label=f'Cluster {i} (n={len(cluster_data)})',
                   alpha=0.6, s=50, color=colors[i])
    
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('Total Volume (USD, log scale)', fontsize=10)
    ax2.set_ylabel('Volume per User (USD, log scale)', fontsize=10)
    ax2.set_title('Engagement Clusters: Volume Scale vs Efficiency', fontsize=11, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '05_engagement_clustering.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()

def generate_adoption_insights(df, top_10_user_pct):
    """Generate key insights about user adoption."""
    print("\n" + "="*60)
    print("KEY ADOPTION INSIGHTS")
    print("="*60)
    
    df_users = df[df['users'] > 0]
    
    # Insight 1: User concentration
    print(f"\n1. USER CONCENTRATION:")
    print(f"   - Top 10 DApps attract {top_10_user_pct:.1f}% of all users")
    print(f"   - Similar concentration as market cap")
    
    # Insight 2: Engagement dichotomy
    df_engagement = df[(df['users'] > 0) & (df['transactions'] > 0)]
    median_tx_per_user = df_engagement['tx_per_user'].median()
    
    print(f"\n2. ENGAGEMENT PATTERNS:")
    print(f"   - Median transactions per user: {median_tx_per_user:.2f}")
    print(f"   - Wide variance in engagement intensity")
    
    # Insight 3: Category differences
    if 'dapp_category' in df.columns:
        gaming = df[df['dapp_category'] == 'NFT Gaming']
        dex = df[df['dapp_category'] == 'DEX']
        
        if len(gaming) > 0 and len(dex) > 0:
            gaming_users = gaming['users'].sum()
            dex_users = dex['users'].sum()
            gaming_vol = gaming[gaming['volume'] > 0]['volume'].sum()
            dex_vol = dex[dex['volume'] > 0]['volume'].sum()
            
            print(f"\n3. CATEGORY COMPARISON (Gaming vs DEX):")
            print(f"   Gaming - Users: {gaming_users:,.0f}, Volume: ${gaming_vol:,.0f}")
            print(f"   DEX - Users: {dex_users:,.0f}, Volume: ${dex_vol:,.0f}")
            if gaming_vol > 0 and dex_vol > 0:
                print(f"   - Gaming has {gaming_users/dex_users:.1f}x more users but {dex_vol/gaming_vol:.1f}x less volume")
    
    return {
        'user_concentration': top_10_user_pct,
        'median_tx_per_user': median_tx_per_user
    }

def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("USER ADOPTION & ENGAGEMENT ANALYSIS")
    print("="*60)
    
    # Load data
    df = load_prepared_data()
    
    # Run analyses
    top_10_pct = analyze_user_distribution(df)
    analyze_engagement_patterns(df)
    analyze_category_engagement(df)
    perform_engagement_clustering(df)
    insights = generate_adoption_insights(df, top_10_pct)
    
    print("\n" + "="*60)
    print("ADOPTION ANALYSIS COMPLETE!")
    print("="*60)
    print("\n✓ All visualizations saved to:", OUTPUT_DIR)
    
    return insights

if __name__ == "__main__":
    insights = main()

