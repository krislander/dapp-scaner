"""
DApp Ecosystem Analysis - Funding & Capital Dynamics
=====================================================
This script analyzes capital raised and funding efficiency.

Key Message Target: "Capital efficiency paradox" - relationship 
between funding and actual market success
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
    print("FUNDING & CAPITAL DYNAMICS ANALYSIS")
    print("="*60)
    
    df = pd.read_csv(DATA_PATH)
    print(f"✓ Loaded {len(df)} DApps")
    
    df_funded = df[df['raised_capital'] > 0].copy()
    print(f"\nAnalyzing {len(df_funded)} DApps with funding data...")
    
    print(f"\nFunding Statistics:")
    print(f"  Total Capital Raised: ${df_funded['raised_capital'].sum():,.0f}M")
    print(f"  Mean: ${df_funded['raised_capital'].mean():,.2f}M")
    print(f"  Median: ${df_funded['raised_capital'].median():,.2f}M")
    
    # Funding by category
    if 'dapp_category' in df_funded.columns:
        funding_by_cat = df_funded.groupby('dapp_category')['raised_capital'].agg(['sum', 'mean', 'count'])
        funding_by_cat = funding_by_cat.sort_values('sum', ascending=False).head(10)
        print(f"\nTop 10 Categories by Total Funding:")
        print(funding_by_cat)
    
    # Funding efficiency (ROI proxy)
    df_funded['funding_efficiency'] = np.where(
        df_funded['raised_capital'] > 0,
        df_funded['market_cap'] / (df_funded['raised_capital'] * 1e6),
        0
    )
    
    print(f"\nFunding Efficiency (Market Cap / Capital Raised):")
    eff_clean = df_funded[(df_funded['funding_efficiency'] > 0) & 
                          (df_funded['funding_efficiency'] < df_funded['funding_efficiency'].quantile(0.95))]
    print(f"  Median: {eff_clean['funding_efficiency'].median():.2f}x")
    
    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Funding & Capital Dynamics', fontsize=14, fontweight='bold')
    
    # Plot 1: Capital raised distribution
    ax1 = axes[0, 0]
    ax1.hist(df_funded['raised_capital'], bins=30, color='steelblue', edgecolor='black', alpha=0.7)
    ax1.set_xlabel('Capital Raised ($M)', fontsize=10)
    ax1.set_ylabel('Number of DApps', fontsize=10)
    ax1.set_title('Funding Distribution', fontsize=11, fontweight='bold')
    
    # Plot 2: Top funded DApps
    ax2 = axes[0, 1]
    top_10 = df_funded.nlargest(10, 'raised_capital')
    colors = plt.cm.viridis(np.linspace(0, 1, len(top_10)))
    ax2.barh(range(len(top_10)), top_10['raised_capital'], color=colors)
    ax2.set_yticks(range(len(top_10)))
    ax2.set_yticklabels(top_10['name'], fontsize=8)
    ax2.set_xlabel('Capital Raised ($M)', fontsize=10)
    ax2.set_title('Top 10 Funded DApps', fontsize=11, fontweight='bold')
    ax2.invert_yaxis()
    
    # Plot 3: Funding vs Market Cap
    ax3 = axes[1, 0]
    df_plot = df_funded[df_funded['market_cap'] > 0]
    scatter = ax3.scatter(df_plot['raised_capital'], df_plot['market_cap'],
                         alpha=0.5, s=50, c=df_plot['users'], cmap='viridis')
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.set_xlabel('Capital Raised ($M, log scale)', fontsize=10)
    ax3.set_ylabel('Market Cap (USD, log scale)', fontsize=10)
    ax3.set_title('Funding vs Market Success', fontsize=11, fontweight='bold')
    cbar = plt.colorbar(scatter, ax=ax3)
    cbar.set_label('Users', fontsize=9)
    
    # Plot 4: Funding by category
    ax4 = axes[1, 1]
    if 'funding_by_cat' in locals():
        top_cats = funding_by_cat.head(8)
        colors = plt.cm.plasma(np.linspace(0, 1, len(top_cats)))
        ax4.barh(range(len(top_cats)), top_cats['sum'], color=colors)
        ax4.set_yticks(range(len(top_cats)))
        ax4.set_yticklabels(top_cats.index, fontsize=9)
        ax4.set_xlabel('Total Capital Raised ($M)', fontsize=10)
        ax4.set_title('Funding by Category', fontsize=11, fontweight='bold')
        ax4.invert_yaxis()
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '07_funding_analysis.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()
    
    print("\n" + "="*60)
    print("FUNDING ANALYSIS COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    main()

