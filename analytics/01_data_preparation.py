"""
DApp Ecosystem Analysis - Data Preparation & Quality Assessment
================================================================
This script loads, validates, and prepares the DApp dataset for analysis.
It creates derived features and generates a comprehensive data quality report.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

from config import RAW_DATA_PATH as DATA_PATH, OUTPUT_DIR

warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def load_data():
    """Load the DApp dataset from CSV."""
    print("Loading DApp dataset...")
    df = pd.read_csv(DATA_PATH)
    print(f"✓ Loaded {len(df)} DApps with {len(df.columns)} columns")
    return df

def assess_data_quality(df):
    """Generate comprehensive data quality report."""
    print("\n" + "="*60)
    print("DATA QUALITY ASSESSMENT")
    print("="*60)
    
    # Basic info
    print(f"\nDataset Shape: {df.shape}")
    print(f"Total DApps: {len(df)}")
    print(f"Total Variables: {len(df.columns)}")
    
    # Missing values analysis
    print("\n--- Missing Values Analysis ---")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        'Missing Count': missing,
        'Percentage': missing_pct
    })
    missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
    
    if len(missing_df) > 0:
        print(f"\nColumns with missing values ({len(missing_df)}):")
        print(missing_df.head(15))
    else:
        print("\nNo missing values found!")
    
    # Data types
    print("\n--- Data Type Distribution ---")
    print(df.dtypes.value_counts())
    
    # Numeric columns summary
    print("\n--- Numeric Columns Summary (Top 10) ---")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(f"Total numeric columns: {len(numeric_cols)}")
    print("\nSample statistics:")
    print(df[numeric_cols].describe().T[['count', 'mean', 'std', 'min', 'max']].head(10))
    
    # Categorical columns
    print("\n--- Categorical Variables ---")
    categorical_cols = ['governance_type', 'ownership_status', 'level_of_decentralisation', 
                       'dapp_sector', 'dapp_category']
    
    for col in categorical_cols:
        if col in df.columns:
            print(f"\n{col}:")
            print(df[col].value_counts().head(10))
    
    return missing_df

def create_derived_features(df):
    """Create derived features for analysis."""
    print("\n" + "="*60)
    print("CREATING DERIVED FEATURES")
    print("="*60)
    
    df_enriched = df.copy()
    
    # 1. Governance Score (composite metric)
    print("\n1. Creating governance_score...")
    governance_map = {
        'NONE': 0,
        'TEAM_CONTROLLED': 1,
        'SNAPSHOT_OFFCHAIN': 2,
        'HYBRID': 3,
        'MULTISIG_WITH_COMMUNITY_INPUT': 4,
        'ONCHAIN_TOKEN_GOVERNANCE': 5,
        'DAO_WITH_TIMELOCK': 6
    }
    
    ownership_map = {
        'COMPANY_OWNED': 0,
        'FOUNDATION_OWNED': 1,
        'MIXED': 2,
        'DAO_OWNED': 3
    }
    
    decentralization_map = {
        'CENTRALIZED': 0,
        'SEMI_DECENTRALIZED': 1,
        'DECENTRALIZED': 2
    }
    
    df_enriched['gov_numeric'] = df_enriched['governance_type'].map(governance_map)
    df_enriched['own_numeric'] = df_enriched['ownership_status'].map(ownership_map)
    df_enriched['decent_numeric'] = df_enriched['level_of_decentralisation'].map(decentralization_map)
    
    # Composite governance score (0-1 normalized)
    df_enriched['governance_score'] = (
        (df_enriched['gov_numeric'].fillna(0) / 6 * 0.4) +
        (df_enriched['own_numeric'].fillna(0) / 3 * 0.3) +
        (df_enriched['decent_numeric'].fillna(0) / 2 * 0.3)
    )
    print(f"   ✓ Governance score range: {df_enriched['governance_score'].min():.2f} - {df_enriched['governance_score'].max():.2f}")
    
    # 2. Chain count
    print("\n2. Parsing chain information...")
    df_enriched['chain_count'] = df_enriched['chains'].fillna('').apply(
        lambda x: len([c.strip() for c in str(x).split(',') if c.strip()])
    )
    df_enriched['is_multi_chain'] = df_enriched['chain_count'] > 1
    print(f"   ✓ Multi-chain DApps: {df_enriched['is_multi_chain'].sum()} ({df_enriched['is_multi_chain'].mean()*100:.1f}%)")
    
    # 3. Market maturity score
    print("\n3. Calculating market maturity...")
    # Normalize key metrics
    df_enriched['market_cap_norm'] = np.log1p(df_enriched['market_cap'].fillna(0))
    df_enriched['users_norm'] = np.log1p(df_enriched['users'].fillna(0))
    df_enriched['tvl_norm'] = np.log1p(df_enriched['tvl'].fillna(0))
    
    # Composite maturity score
    df_enriched['market_maturity'] = (
        df_enriched['market_cap_norm'] / df_enriched['market_cap_norm'].max() * 0.4 +
        df_enriched['users_norm'] / df_enriched['users_norm'].max() * 0.3 +
        df_enriched['tvl_norm'] / df_enriched['tvl_norm'].max() * 0.3
    )
    print(f"   ✓ Market maturity range: {df_enriched['market_maturity'].min():.2f} - {df_enriched['market_maturity'].max():.2f}")
    
    # 4. Volatility index
    print("\n4. Computing volatility index...")
    volatility_cols = ['percent_change_1h', 'percent_change_24h', 'percent_change_7d', 
                      'percent_change_30d', 'percent_change_60d', 'percent_change_90d']
    
    df_enriched['volatility_index'] = df_enriched[volatility_cols].fillna(0).abs().mean(axis=1)
    print(f"   ✓ Volatility index range: {df_enriched['volatility_index'].min():.2f} - {df_enriched['volatility_index'].max():.2f}")
    
    # 5. Liquidity efficiency
    print("\n5. Calculating liquidity efficiency...")
    df_enriched['liquidity_efficiency'] = np.where(
        df_enriched['market_cap'] > 0,
        df_enriched['tvl'] / df_enriched['market_cap'],
        0
    )
    print(f"   ✓ Liquidity efficiency (TVL/Market Cap) median: {df_enriched['liquidity_efficiency'].median():.4f}")
    
    # 6. User engagement metrics
    print("\n6. Creating engagement metrics...")
    df_enriched['tx_per_user'] = np.where(
        df_enriched['users'] > 0,
        df_enriched['transactions'] / df_enriched['users'],
        0
    )
    
    df_enriched['volume_per_user'] = np.where(
        df_enriched['users'] > 0,
        df_enriched['volume'] / df_enriched['users'],
        0
    )
    
    df_enriched['market_cap_per_user'] = np.where(
        df_enriched['users'] > 0,
        df_enriched['market_cap'] / df_enriched['users'],
        0
    )
    
    print(f"   ✓ Median transactions per user: {df_enriched['tx_per_user'].median():.2f}")
    print(f"   ✓ Median volume per user: ${df_enriched['volume_per_user'].median():.2f}")
    
    # 7. Has token flag
    print("\n7. Token identification...")
    df_enriched['has_token'] = df_enriched['token_symbol'].notna() & (df_enriched['token_symbol'] != '')
    print(f"   ✓ DApps with tokens: {df_enriched['has_token'].sum()} ({df_enriched['has_token'].mean()*100:.1f}%)")
    
    print(f"\n✓ Total features created: {len(df_enriched.columns) - len(df.columns)}")
    
    return df_enriched

def visualize_data_quality(df, missing_df):
    """Create visualizations for data quality assessment."""
    print("\n" + "="*60)
    print("GENERATING DATA QUALITY VISUALIZATIONS")
    print("="*60)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Data Quality Assessment Dashboard', fontsize=16, fontweight='bold')
    
    # 1. Missing values heatmap (top columns)
    ax1 = axes[0, 0]
    if len(missing_df) > 0:
        top_missing = missing_df.head(15)
        colors = plt.cm.Reds(top_missing['Percentage'].values / 100)
        ax1.barh(range(len(top_missing)), top_missing['Percentage'], color=colors)
        ax1.set_yticks(range(len(top_missing)))
        ax1.set_yticklabels(top_missing.index, fontsize=9)
        ax1.set_xlabel('Missing Data (%)', fontsize=10)
        ax1.set_title('Top 15 Columns with Missing Values', fontsize=11, fontweight='bold')
        ax1.invert_yaxis()
        
        # Add value labels
        for i, v in enumerate(top_missing['Percentage']):
            ax1.text(v + 0.5, i, f'{v:.1f}%', va='center', fontsize=8)
    else:
        ax1.text(0.5, 0.5, 'No Missing Values!', ha='center', va='center', 
                fontsize=14, transform=ax1.transAxes)
        ax1.axis('off')
    
    # 2. Data type distribution
    ax2 = axes[0, 1]
    dtype_counts = df.dtypes.value_counts()
    colors_pie = sns.color_palette("husl", len(dtype_counts))
    ax2.pie(dtype_counts.values, labels=dtype_counts.index, autopct='%1.1f%%',
            startangle=90, colors=colors_pie)
    ax2.set_title('Data Type Distribution', fontsize=11, fontweight='bold')
    
    # 3. Numeric columns distribution (sample)
    ax3 = axes[1, 0]
    numeric_sample = ['market_cap', 'users', 'tvl', 'volume', 'transactions']
    available_cols = [col for col in numeric_sample if col in df.columns]
    
    if available_cols:
        data_for_box = []
        labels_for_box = []
        for col in available_cols:
            vals = df[col].replace([np.inf, -np.inf], np.nan).dropna()
            if len(vals) > 0 and vals.max() > 0:
                data_for_box.append(np.log10(vals[vals > 0]))
                labels_for_box.append(col)
        
        if data_for_box:
            bp = ax3.boxplot(data_for_box, labels=labels_for_box, patch_artist=True)
            for patch in bp['boxes']:
                patch.set_facecolor('lightblue')
            ax3.set_ylabel('Log10 Scale', fontsize=10)
            ax3.set_title('Key Metrics Distribution (Log Scale)', fontsize=11, fontweight='bold')
            ax3.tick_params(axis='x', rotation=45)
            plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # 4. Category distribution
    ax4 = axes[1, 1]
    if 'dapp_category' in df.columns:
        top_categories = df['dapp_category'].value_counts().head(10)
        colors_bar = plt.cm.viridis(np.linspace(0, 1, len(top_categories)))
        ax4.barh(range(len(top_categories)), top_categories.values, color=colors_bar)
        ax4.set_yticks(range(len(top_categories)))
        ax4.set_yticklabels(top_categories.index, fontsize=9)
        ax4.set_xlabel('Number of DApps', fontsize=10)
        ax4.set_title('Top 10 DApp Categories', fontsize=11, fontweight='bold')
        ax4.invert_yaxis()
        
        # Add value labels
        for i, v in enumerate(top_categories.values):
            ax4.text(v + 0.5, i, str(v), va='center', fontsize=8)
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / '01_data_quality_dashboard.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()

def save_prepared_data(df):
    """Save the prepared dataset."""
    output_path = OUTPUT_DIR / 'prepared_data.csv'
    df.to_csv(output_path, index=False)
    print(f"\n✓ Prepared dataset saved: {output_path}")
    print(f"  Shape: {df.shape}")
    return output_path

def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("DApp ECOSYSTEM ANALYSIS - DATA PREPARATION")
    print("="*60)
    
    # Load data
    df = load_data()
    
    # Assess quality
    missing_df = assess_data_quality(df)
    
    # Create derived features
    df_enriched = create_derived_features(df)
    
    # Visualize quality
    visualize_data_quality(df, missing_df)
    
    # Save prepared data
    prepared_path = save_prepared_data(df_enriched)
    
    print("\n" + "="*60)
    print("DATA PREPARATION COMPLETE!")
    print("="*60)
    print(f"\n✓ Original columns: {len(df.columns)}")
    print(f"✓ Enriched columns: {len(df_enriched.columns)}")
    print(f"✓ New features: {len(df_enriched.columns) - len(df.columns)}")
    print(f"✓ Output file: {prepared_path}")
    
    return df_enriched

if __name__ == "__main__":
    df_prepared = main()

