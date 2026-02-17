"""
DApp Ecosystem Analysis - Market Dynamics & Token Economics
============================================================
This script analyzes market capitalization, token economics, price volatility,
and trading patterns across the DApp ecosystem.

Key Message Target: "Market concentration and volatility patterns" - 
wealth distribution in DApp economy
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
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

def analyze_market_cap_distribution(df):
    """Analyze market capitalization distribution and concentration."""
    print("\n" + "="*60)
    print("MARKET CAP DISTRIBUTION ANALYSIS")
    print("="*60)
    
    df_market = df[df['market_cap'] > 0].copy()
    print(f"\nAnalyzing {len(df_market)} DApps with market cap data...")
    
    # Basic statistics
    print(f"\nMarket Cap Statistics:")
    print(f"  Total Market Cap: ${df_market['market_cap'].sum():,.0f}")
    print(f"  Mean: ${df_market['market_cap'].mean():,.0f}")
    print(f"  Median: ${df_market['market_cap'].median():,.0f}")
    print(f"  Std Dev: ${df_market['market_cap'].std():,.0f}")
    
    # Concentration analysis
    df_sorted = df_market.sort_values('market_cap', ascending=False)
    total_mcap = df_sorted['market_cap'].sum()
    
    top_10_sum = df_sorted.head(10)['market_cap'].sum()
    top_10_pct = top_10_sum / total_mcap * 100
    
    top_50_sum = df_sorted.head(50)['market_cap'].sum()
    top_50_pct = top_50_sum / total_mcap * 100
    
    top_100_sum = df_sorted.head(100)['market_cap'].sum()
    top_100_pct = top_100_sum / total_mcap * 100
    
    print(f"\nMarket Concentration:")
    print(f"  Top 10 DApps: ${top_10_sum:,.0f} ({top_10_pct:.1f}% of total)")
    print(f"  Top 50 DApps: ${top_50_sum:,.0f} ({top_50_pct:.1f}% of total)")
    print(f"  Top 100 DApps: ${top_100_sum:,.0f} ({top_100_pct:.1f}% of total)")
    
    top_10_mcap = df_sorted.head(10)
    print(f"\nTop 10 DApps by Market Cap:")
    for i, (idx, row) in enumerate(top_10_mcap.iterrows(), 1):
        print(f"  {i}. {row['name']}: ${row['market_cap']:,.0f}")
    
    # Power law analysis
    # Fit power law distribution
    log_mcap = np.log10(df_market['market_cap'])
    log_rank = np.log10(np.arange(1, len(df_market) + 1))
    slope, intercept, r_value, p_value, std_err = stats.linregress(log_rank, log_mcap[::-1].values)
    
    print(f"\nPower Law Analysis:")
    print(f"  Slope: {slope:.2f}")
    print(f"  R²: {r_value**2:.3f}")
    print(f"  Distribution follows power law (typical of wealth concentration)")
    
    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Market Capitalization Distribution & Concentration', fontsize=14, fontweight='bold')
    
    # Plot 1: Distribution (log scale)
    ax1 = axes[0, 0]
    ax1.hist(df_market['market_cap'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
    ax1.set_xscale('log')
    ax1.set_xlabel('Market Cap (USD, log scale)', fontsize=10)
    ax1.set_ylabel('Number of DApps', fontsize=10)
    ax1.set_title('Market Cap Distribution (Log Scale)', fontsize=11, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Cumulative concentration
    ax2 = axes[0, 1]
    df_sorted['cumulative_pct'] = df_sorted['market_cap'].cumsum() / total_mcap * 100
    df_sorted['rank_pct'] = np.arange(1, len(df_sorted) + 1) / len(df_sorted) * 100
    
    ax2.plot(df_sorted['rank_pct'], df_sorted['cumulative_pct'], linewidth=2, color='darkred')
    ax2.plot([0, 100], [0, 100], '--', color='gray', alpha=0.5, label='Perfect Equality')
    ax2.fill_between(df_sorted['rank_pct'], 0, df_sorted['cumulative_pct'], alpha=0.3, color='red')
    ax2.set_xlabel('DApps Ranked by Market Cap (%)', fontsize=10)
    ax2.set_ylabel('Cumulative Market Cap (%)', fontsize=10)
    ax2.set_title('Lorenz Curve: Market Cap Concentration', fontsize=11, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Top 20 DApps
    ax3 = axes[1, 0]
    top_20 = top_10_mcap.head(20)
    colors = plt.cm.viridis(np.linspace(0, 1, len(top_20)))
    ax3.barh(range(len(top_20)), top_20['market_cap'], color=colors)
    ax3.set_yticks(range(len(top_20)))
    ax3.set_yticklabels(top_20['name'], fontsize=8)
    ax3.set_xlabel('Market Cap (USD)', fontsize=10)
    ax3.set_title('Top 20 DApps by Market Capitalization', fontsize=11, fontweight='bold')
    ax3.invert_yaxis()
    
    # Format x-axis
    ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e9:.1f}B'))
    
    # Plot 4: Power law fit
    ax4 = axes[1, 1]
    df_sorted_indexed = df_sorted.reset_index(drop=True)
    ranks = np.arange(1, len(df_sorted_indexed) + 1)
    
    ax4.scatter(ranks, df_sorted_indexed['market_cap'], alpha=0.5, s=20, label='Actual')
    
    # Plot power law fit
    fitted_values = 10**(intercept + slope * np.log10(ranks))
    ax4.plot(ranks, fitted_values, 'r--', linewidth=2, label=f'Power Law Fit (α={-slope:.2f})')
    
    ax4.set_xscale('log')
    ax4.set_yscale('log')
    ax4.set_xlabel('Rank (log scale)', fontsize=10)
    ax4.set_ylabel('Market Cap (USD, log scale)', fontsize=10)
    ax4.set_title('Power Law Distribution', fontsize=11, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '04_market_cap_distribution.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()
    
    return top_10_pct

def analyze_price_volatility(df):
    """Analyze price volatility patterns."""
    print("\n" + "="*60)
    print("PRICE VOLATILITY ANALYSIS")
    print("="*60)
    
    volatility_cols = ['percent_change_1h', 'percent_change_24h', 'percent_change_7d',
                       'percent_change_30d', 'percent_change_60d', 'percent_change_90d']
    
    df_vol = df[df[volatility_cols].notna().any(axis=1)].copy()
    print(f"\nAnalyzing {len(df_vol)} DApps with price change data...")
    
    # Calculate absolute volatility
    for col in volatility_cols:
        df_vol[f'{col}_abs'] = df_vol[col].abs()
    
    # Average volatility by timeframe
    avg_volatility = {}
    for col in volatility_cols:
        avg = df_vol[f'{col}_abs'].mean()
        avg_volatility[col] = avg
        print(f"  Avg {col.replace('percent_change_', '')}: {avg:.2f}%")
    
    # Volatility by category
    if 'dapp_category' in df_vol.columns:
        top_cats = df_vol['dapp_category'].value_counts().head(8).index
        vol_by_cat = df_vol[df_vol['dapp_category'].isin(top_cats)].groupby('dapp_category')[
            'volatility_index'].agg(['mean', 'median']).sort_values('mean', ascending=False)
        
        print(f"\nVolatility Index by Category:")
        print(vol_by_cat)
    
    # Volatility by governance
    if 'level_of_decentralisation' in df_vol.columns:
        vol_by_decent = df_vol.groupby('level_of_decentralisation')['volatility_index'].agg(['mean', 'median'])
        print(f"\nVolatility by Decentralization:")
        print(vol_by_decent)
    
    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Price Volatility Analysis', fontsize=14, fontweight='bold')
    
    # Plot 1: Volatility by timeframe
    ax1 = axes[0, 0]
    timeframes = ['1h', '24h', '7d', '30d', '60d', '90d']
    volatilities = [avg_volatility[f'percent_change_{tf}'] for tf in timeframes]
    colors = plt.cm.Reds(np.linspace(0.3, 1, len(timeframes)))
    
    ax1.bar(range(len(timeframes)), volatilities, color=colors, edgecolor='black')
    ax1.set_xticks(range(len(timeframes)))
    ax1.set_xticklabels(timeframes)
    ax1.set_ylabel('Average Absolute Price Change (%)', fontsize=10)
    ax1.set_xlabel('Timeframe', fontsize=10)
    ax1.set_title('Average Volatility by Timeframe', fontsize=11, fontweight='bold')
    
    # Add value labels
    for i, v in enumerate(volatilities):
        ax1.text(i, v + 0.5, f'{v:.1f}%', ha='center', va='bottom', fontsize=9)
    
    # Plot 2: Volatility heatmap by category
    ax2 = axes[0, 1]
    if 'vol_by_cat' in locals():
        # Create heatmap data
        vol_heat_data = []
        for cat in vol_by_cat.index:
            cat_data = df_vol[df_vol['dapp_category'] == cat]
            row = []
            for col in volatility_cols:
                avg = cat_data[f'{col}_abs'].mean()
                row.append(avg)
            vol_heat_data.append(row)
        
        vol_heat_df = pd.DataFrame(vol_heat_data, 
                                   index=vol_by_cat.index,
                                   columns=['1h', '24h', '7d', '30d', '60d', '90d'])
        
        sns.heatmap(vol_heat_df, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax2,
                   cbar_kws={'label': 'Avg Volatility (%)'})
        ax2.set_title('Volatility Heatmap by Category', fontsize=11, fontweight='bold')
        ax2.set_xlabel('Timeframe', fontsize=10)
        ax2.set_ylabel('Category', fontsize=10)
    
    # Plot 3: Volatility distribution
    ax3 = axes[1, 0]
    vol_index_clean = df_vol[df_vol['volatility_index'] < df_vol['volatility_index'].quantile(0.95)]
    ax3.hist(vol_index_clean['volatility_index'], bins=50, color='coral', edgecolor='black', alpha=0.7)
    ax3.set_xlabel('Volatility Index', fontsize=10)
    ax3.set_ylabel('Number of DApps', fontsize=10)
    ax3.set_title('Volatility Index Distribution (95th percentile)', fontsize=11, fontweight='bold')
    ax3.axvline(vol_index_clean['volatility_index'].median(), color='red', 
               linestyle='--', linewidth=2, label=f'Median: {vol_index_clean["volatility_index"].median():.2f}')
    ax3.legend()
    
    # Plot 4: Volatility vs Market Cap
    ax4 = axes[1, 1]
    df_vol_clean = df_vol[(df_vol['market_cap'] > 0) & 
                          (df_vol['volatility_index'] < df_vol['volatility_index'].quantile(0.95))]
    
    scatter = ax4.scatter(df_vol_clean['market_cap'], df_vol_clean['volatility_index'],
                         alpha=0.5, s=50, c=df_vol_clean['governance_score'], cmap='viridis')
    ax4.set_xscale('log')
    ax4.set_xlabel('Market Cap (USD, log scale)', fontsize=10)
    ax4.set_ylabel('Volatility Index', fontsize=10)
    ax4.set_title('Volatility vs Market Cap', fontsize=11, fontweight='bold')
    cbar = plt.colorbar(scatter, ax=ax4)
    cbar.set_label('Governance Score', fontsize=9)
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '04_price_volatility.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()

def analyze_supply_dynamics(df):
    """Analyze token supply dynamics."""
    print("\n" + "="*60)
    print("TOKEN SUPPLY DYNAMICS ANALYSIS")
    print("="*60)
    
    df_supply = df[(df['circulating_supply'] > 0) & (df['total_supply'] > 0)].copy()
    print(f"\nAnalyzing {len(df_supply)} DApps with supply data...")
    
    # Calculate supply ratio
    df_supply['supply_ratio'] = df_supply['circulating_supply'] / df_supply['total_supply']
    
    print(f"\nSupply Ratio Statistics:")
    print(f"  Mean: {df_supply['supply_ratio'].mean():.2%}")
    print(f"  Median: {df_supply['supply_ratio'].median():.2%}")
    
    # Categorize
    df_supply['supply_category'] = pd.cut(df_supply['supply_ratio'],
                                          bins=[0, 0.25, 0.5, 0.75, 1.0],
                                          labels=['Very Low (0-25%)', 'Low (25-50%)', 
                                                 'High (50-75%)', 'Very High (75-100%)'])
    
    print(f"\nSupply Distribution:")
    print(df_supply['supply_category'].value_counts())
    
    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Token Supply Dynamics', fontsize=14, fontweight='bold')
    
    # Plot 1: Supply ratio distribution
    ax1 = axes[0, 0]
    ax1.hist(df_supply['supply_ratio'], bins=50, color='skyblue', edgecolor='black', alpha=0.7)
    ax1.axvline(df_supply['supply_ratio'].median(), color='red', linestyle='--', 
               linewidth=2, label=f'Median: {df_supply["supply_ratio"].median():.2%}')
    ax1.set_xlabel('Circulating / Total Supply Ratio', fontsize=10)
    ax1.set_ylabel('Number of DApps', fontsize=10)
    ax1.set_title('Supply Ratio Distribution', fontsize=11, fontweight='bold')
    ax1.legend()
    
    # Plot 2: Supply categories
    ax2 = axes[0, 1]
    supply_counts = df_supply['supply_category'].value_counts()
    colors = plt.cm.Blues(np.linspace(0.4, 1, len(supply_counts)))
    ax2.pie(supply_counts.values, labels=supply_counts.index, autopct='%1.1f%%',
           startangle=90, colors=colors)
    ax2.set_title('Supply Category Distribution', fontsize=11, fontweight='bold')
    
    # Plot 3: Supply ratio vs Market cap
    ax3 = axes[1, 0]
    df_plot = df_supply[df_supply['market_cap'] > 0]
    scatter = ax3.scatter(df_plot['supply_ratio'], df_plot['market_cap'],
                         alpha=0.5, s=50, c=df_plot['price'], cmap='plasma', norm=plt.Normalize(vmin=0, vmax=10))
    ax3.set_yscale('log')
    ax3.set_xlabel('Circulating / Total Supply Ratio', fontsize=10)
    ax3.set_ylabel('Market Cap (USD, log scale)', fontsize=10)
    ax3.set_title('Supply Ratio vs Market Cap', fontsize=11, fontweight='bold')
    cbar = plt.colorbar(scatter, ax=ax3)
    cbar.set_label('Price (USD)', fontsize=9)
    
    # Plot 4: Fully diluted vs circulating market cap
    ax4 = axes[1, 1]
    df_supply['fdv'] = df_supply['price'] * df_supply['total_supply']
    df_plot2 = df_supply[(df_supply['market_cap'] > 0) & (df_supply['fdv'] > 0)]
    
    ax4.scatter(df_plot2['market_cap'], df_plot2['fdv'], alpha=0.5, s=50, color='green')
    ax4.plot([df_plot2['market_cap'].min(), df_plot2['market_cap'].max()],
            [df_plot2['market_cap'].min(), df_plot2['market_cap'].max()],
            'r--', linewidth=2, label='1:1 Line')
    ax4.set_xscale('log')
    ax4.set_yscale('log')
    ax4.set_xlabel('Market Cap (USD, log scale)', fontsize=10)
    ax4.set_ylabel('Fully Diluted Valuation (USD, log scale)', fontsize=10)
    ax4.set_title('Market Cap vs Fully Diluted Valuation', fontsize=11, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '04_supply_dynamics.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()

def analyze_volume_metrics(df):
    """Analyze trading volume and liquidity metrics."""
    print("\n" + "="*60)
    print("VOLUME & LIQUIDITY ANALYSIS")
    print("="*60)
    
    df_vol = df[(df['volume'] > 0) & (df['market_cap'] > 0)].copy()
    print(f"\nAnalyzing {len(df_vol)} DApps with volume data...")
    
    # Volume to Market Cap ratio
    df_vol['vol_to_mcap'] = df_vol['volume'] / df_vol['market_cap']
    
    print(f"\nVolume/Market Cap Ratio:")
    print(f"  Mean: {df_vol['vol_to_mcap'].mean():.2f}")
    print(f"  Median: {df_vol['vol_to_mcap'].median():.2f}")
    
    # Categorize trading activity
    df_vol['trading_activity'] = pd.cut(df_vol['vol_to_mcap'],
                                        bins=[0, 0.1, 1, 10, np.inf],
                                        labels=['Low', 'Medium', 'High', 'Very High'])
    
    print(f"\nTrading Activity Distribution:")
    print(df_vol['trading_activity'].value_counts())
    
    # Top volume DApps
    top_volume = df_vol.nlargest(10, 'volume')
    print(f"\nTop 10 DApps by Trading Volume:")
    for i, (idx, row) in enumerate(top_volume.iterrows(), 1):
        print(f"  {i}. {row['name']}: ${row['volume']:,.0f}")
    
    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Trading Volume & Liquidity Analysis', fontsize=14, fontweight='bold')
    
    # Plot 1: Volume vs Market Cap quadrant
    ax1 = axes[0, 0]
    median_vol = df_vol['volume'].median()
    median_mcap = df_vol['market_cap'].median()
    
    scatter = ax1.scatter(df_vol['market_cap'], df_vol['volume'],
                         alpha=0.5, s=50, c=df_vol['users'], cmap='viridis',
                         norm=plt.Normalize(vmin=0, vmax=df_vol['users'].quantile(0.95)))
    
    ax1.axhline(median_vol, color='red', linestyle='--', alpha=0.5)
    ax1.axvline(median_mcap, color='red', linestyle='--', alpha=0.5)
    
    # Add quadrant labels
    ax1.text(median_mcap * 1.5, median_vol * 50, 'High Vol\nHigh MCap', 
            fontsize=9, alpha=0.7, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    ax1.text(median_mcap * 0.1, median_vol * 50, 'High Vol\nLow MCap', 
            fontsize=9, alpha=0.7, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('Market Cap (USD, log scale)', fontsize=10)
    ax1.set_ylabel('Trading Volume (USD, log scale)', fontsize=10)
    ax1.set_title('Volume vs Market Cap Quadrant Analysis', fontsize=11, fontweight='bold')
    cbar = plt.colorbar(scatter, ax=ax1)
    cbar.set_label('Active Users', fontsize=9)
    
    # Plot 2: Volume/Market Cap ratio distribution
    ax2 = axes[0, 1]
    vol_ratio_clean = df_vol[df_vol['vol_to_mcap'] < df_vol['vol_to_mcap'].quantile(0.95)]
    ax2.hist(vol_ratio_clean['vol_to_mcap'], bins=50, color='orange', edgecolor='black', alpha=0.7)
    ax2.axvline(vol_ratio_clean['vol_to_mcap'].median(), color='red', linestyle='--',
               linewidth=2, label=f'Median: {vol_ratio_clean["vol_to_mcap"].median():.2f}')
    ax2.set_xlabel('Volume / Market Cap Ratio', fontsize=10)
    ax2.set_ylabel('Number of DApps', fontsize=10)
    ax2.set_title('Trading Activity Distribution', fontsize=11, fontweight='bold')
    ax2.legend()
    
    # Plot 3: Top 15 by volume
    ax3 = axes[1, 0]
    top_15_vol = df_vol.nlargest(15, 'volume')
    colors = plt.cm.plasma(np.linspace(0, 1, len(top_15_vol)))
    ax3.barh(range(len(top_15_vol)), top_15_vol['volume'], color=colors)
    ax3.set_yticks(range(len(top_15_vol)))
    ax3.set_yticklabels(top_15_vol['name'], fontsize=8)
    ax3.set_xlabel('Trading Volume (USD)', fontsize=10)
    ax3.set_title('Top 15 DApps by Trading Volume', fontsize=11, fontweight='bold')
    ax3.invert_yaxis()
    ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e9:.1f}B'))
    
    # Plot 4: Trading activity by category
    ax4 = axes[1, 1]
    if 'dapp_category' in df_vol.columns:
        top_cats = df_vol['dapp_category'].value_counts().head(8).index
        activity_by_cat = pd.crosstab(
            df_vol[df_vol['dapp_category'].isin(top_cats)]['dapp_category'],
            df_vol[df_vol['dapp_category'].isin(top_cats)]['trading_activity'],
            normalize='index'
        ) * 100
        
        activity_by_cat.plot(kind='barh', stacked=True, ax=ax4,
                            color=['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4'])
        ax4.set_xlabel('Percentage', fontsize=10)
        ax4.set_title('Trading Activity by Category', fontsize=11, fontweight='bold')
        ax4.legend(title='Activity', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '04_volume_liquidity.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()

def generate_market_insights(df, top_10_pct):
    """Generate key insights about market dynamics."""
    print("\n" + "="*60)
    print("KEY MARKET INSIGHTS")
    print("="*60)
    
    df_market = df[df['market_cap'] > 0]
    
    # Insight 1: Market concentration
    print(f"\n1. MARKET CONCENTRATION:")
    print(f"   - Top 10 DApps control {top_10_pct:.1f}% of total market cap")
    print(f"   - Severe wealth concentration in DApp economy")
    
    # Insight 2: Token availability
    has_token_pct = df['has_token'].mean() * 100
    print(f"\n2. TOKEN ADOPTION:")
    print(f"   - {has_token_pct:.1f}% of DApps have tokens")
    print(f"   - {100-has_token_pct:.1f}% operate without native tokens")
    
    # Insight 3: Volatility patterns
    avg_vol_30d = df['percent_change_30d'].abs().mean()
    print(f"\n3. VOLATILITY:")
    print(f"   - Average 30-day price volatility: {avg_vol_30d:.1f}%")
    print(f"   - High volatility indicates speculative market")
    
    # Insight 4: Supply concentration
    df_supply = df[(df['circulating_supply'] > 0) & (df['total_supply'] > 0)]
    avg_supply_ratio = (df_supply['circulating_supply'] / df_supply['total_supply']).mean()
    print(f"\n4. TOKEN SUPPLY:")
    print(f"   - Average circulating supply: {avg_supply_ratio:.1%} of total")
    print(f"   - Significant unlocked supply overhang")
    
    return {
        'top_10_concentration': top_10_pct,
        'token_adoption': has_token_pct,
        'avg_volatility_30d': avg_vol_30d
    }

def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("MARKET DYNAMICS & TOKEN ECONOMICS ANALYSIS")
    print("="*60)
    
    # Load data
    df = load_prepared_data()
    
    # Run analyses
    top_10_pct = analyze_market_cap_distribution(df)
    analyze_price_volatility(df)
    analyze_supply_dynamics(df)
    analyze_volume_metrics(df)
    insights = generate_market_insights(df, top_10_pct)
    
    print("\n" + "="*60)
    print("MARKET ANALYSIS COMPLETE!")
    print("="*60)
    print("\n✓ All visualizations saved to:", OUTPUT_DIR)
    
    return insights

if __name__ == "__main__":
    insights = main()

