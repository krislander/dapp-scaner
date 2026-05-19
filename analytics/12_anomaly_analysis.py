"""
DApp Ecosystem Analysis - Anomaly & Contradiction Detection
=============================================================
Identifies strange, contradictory, or noteworthy results that
challenge assumptions about the sector. These findings elevate the
discussion section of the thesis.

Focus areas:
  1. Governance paradoxes (e.g. "decentralized" but company-owned)
  2. Token type mismatches (governance token but no community governance)
  3. Valuation anomalies (unfunded > funded, low-user > high-user)
  4. Performance outliers (extremely high/low efficiency)
  5. Cross-dimensional contradictions
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


def load_prepared_data():
    df = pd.read_csv(DATA_PATH)
    print(f"✓ Loaded {len(df)} DApps with {len(df.columns)} columns")
    return df


# ─────────────────────────────────────────────────────────────────
def detect_governance_paradoxes(df):
    """Find DApps where governance labels contradict each other."""
    print("\n" + "="*60)
    print("GOVERNANCE PARADOXES")
    print("="*60)

    anomalies = {}

    # 1. Labelled DECENTRALIZED but COMPANY_OWNED
    mask1 = ((df['level_of_decentralisation'] == 'DECENTRALIZED') &
             (df['ownership_status'] == 'COMPANY_OWNED'))
    a1 = df[mask1]
    anomalies['decent_but_company'] = a1
    print(f"\n1. 'Decentralized' but Company-Owned: {len(a1)} DApps")
    if len(a1) > 0:
        for _, r in a1.head(10).iterrows():
            print(f"   - {r['name']} (Gov: {r['governance_type']}, "
                  f"Token: {r.get('token_type_primary','?')})")

    # 2. Governance token but TEAM_CONTROLLED
    mask2 = ((df.get('is_governance_token', pd.Series(dtype=bool))) &
             (df['governance_type'] == 'TEAM_CONTROLLED'))
    a2 = df[mask2]
    anomalies['gov_token_team_controlled'] = a2
    print(f"\n2. Governance token but Team-Controlled: {len(a2)} DApps")
    if len(a2) > 0:
        for _, r in a2.head(10).iterrows():
            print(f"   - {r['name']} (Decent: {r['level_of_decentralisation']}, "
                  f"Own: {r['ownership_status']})")

    # 3. DAO_OWNED but governance_type == NONE
    mask3 = ((df['ownership_status'] == 'DAO_OWNED') &
             (df['governance_type'] == 'NONE'))
    a3 = df[mask3]
    anomalies['dao_owned_no_governance'] = a3
    print(f"\n3. DAO-Owned but No Governance: {len(a3)} DApps")

    # 4. CENTRALIZED with ONCHAIN_TOKEN_GOVERNANCE
    mask4 = ((df['level_of_decentralisation'] == 'CENTRALIZED') &
             (df['governance_type'] == 'ONCHAIN_TOKEN_GOVERNANCE'))
    a4 = df[mask4]
    anomalies['centralized_onchain_gov'] = a4
    print(f"\n4. Centralized with On-Chain Governance: {len(a4)} DApps")
    if len(a4) > 0:
        for _, r in a4.head(5).iterrows():
            print(f"   - {r['name']} (Own: {r['ownership_status']})")

    return anomalies


def detect_valuation_anomalies(df):
    """Find DApps with unexpected valuation patterns."""
    print("\n" + "="*60)
    print("VALUATION ANOMALIES")
    print("="*60)

    anomalies = {}

    # 1. High market cap, very few users
    df_mkt = df[(df['market_cap'] > 0) & (df['users'] > 0)].copy()
    df_mkt['mcap_per_user'] = df_mkt['market_cap'] / df_mkt['users']
    threshold_high = df_mkt['mcap_per_user'].quantile(0.95)
    a1 = df_mkt[df_mkt['mcap_per_user'] > threshold_high].nlargest(15, 'mcap_per_user')
    anomalies['high_mcap_low_users'] = a1
    print(f"\n1. Highest Market-Cap-per-User (top 15):")
    for _, r in a1.iterrows():
        print(f"   - {r['name']}: MCap ${r['market_cap']:,.0f}, "
              f"Users {r['users']:,.0f}, MCap/User ${r['mcap_per_user']:,.0f}")

    # 2. Unfunded DApps outperforming funded ones
    df_funded = df[(df['raised_capital'] > 0) & (df['market_cap'] > 0)]
    df_unfunded = df[(df['raised_capital'].fillna(0) == 0) & (df['market_cap'] > 0)]
    funded_median = df_funded['market_cap'].median()
    unfunded_above = df_unfunded[df_unfunded['market_cap'] > funded_median]
    anomalies['unfunded_outperformers'] = unfunded_above
    print(f"\n2. Unfunded DApps above funded median MCap (${funded_median:,.0f}):")
    print(f"   {len(unfunded_above)} unfunded DApps outperform funded median")
    for _, r in unfunded_above.nlargest(10, 'market_cap').iterrows():
        print(f"   - {r['name']}: MCap ${r['market_cap']:,.0f}")

    # 3. TVL much larger than market cap (unusual leverage)
    df_tvl = df[(df['tvl'] > 0) & (df['market_cap'] > 0)].copy()
    df_tvl['tvl_mcap_ratio'] = df_tvl['tvl'] / df_tvl['market_cap']
    high_leverage = df_tvl[df_tvl['tvl_mcap_ratio'] > 10].nlargest(10, 'tvl_mcap_ratio')
    anomalies['extreme_tvl_leverage'] = high_leverage
    print(f"\n3. TVL > 10x Market Cap (extreme leverage):")
    for _, r in high_leverage.iterrows():
        print(f"   - {r['name']}: TVL/MCap = {r['tvl_mcap_ratio']:.1f}x")

    return anomalies


def detect_performance_outliers(df):
    """Statistical outliers in performance metrics."""
    print("\n" + "="*60)
    print("PERFORMANCE OUTLIERS")
    print("="*60)

    df_perf = df[(df['users'] > 0) & (df['transactions'] > 0)].copy()
    df_perf['tx_per_user'] = df_perf['transactions'] / df_perf['users']

    # Extremely high tx per user (bots? wash trading?)
    threshold = df_perf['tx_per_user'].quantile(0.99)
    high_tx = df_perf[df_perf['tx_per_user'] > threshold].nlargest(10, 'tx_per_user')
    print(f"\n1. Extremely High Tx/User (>99th percentile = {threshold:.0f}):")
    for _, r in high_tx.iterrows():
        print(f"   - {r['name']}: {r['tx_per_user']:.0f} tx/user "
              f"(Cat: {r['dapp_category']})")

    # High volume, very few transactions (whale activity?)
    df_vol = df[(df['volume'] > 0) & (df['transactions'] > 0)].copy()
    df_vol['vol_per_tx'] = df_vol['volume'] / df_vol['transactions']
    whale_threshold = df_vol['vol_per_tx'].quantile(0.99)
    whale_activity = df_vol[df_vol['vol_per_tx'] > whale_threshold].nlargest(10, 'vol_per_tx')
    print(f"\n2. Highest Volume per Transaction (whale activity?):")
    for _, r in whale_activity.iterrows():
        print(f"   - {r['name']}: ${r['vol_per_tx']:,.0f}/tx "
              f"(Cat: {r['dapp_category']})")

    # Zero-TVL DApps with high users (non-financial utility)
    high_users_no_tvl = df[(df['users'] > df['users'].quantile(0.75)) &
                           (df['tvl'].fillna(0) == 0)]
    print(f"\n3. High Users (>75th pct) but Zero TVL: {len(high_users_no_tvl)} DApps")
    for _, r in high_users_no_tvl.nlargest(10, 'users').iterrows():
        print(f"   - {r['name']}: {r['users']:,.0f} users "
              f"(Cat: {r['dapp_category']}, Sector: {r['dapp_sector']})")

    return {
        'high_tx_per_user': high_tx,
        'whale_activity': whale_activity,
        'high_users_no_tvl': high_users_no_tvl
    }


def visualize_anomalies(df, gov_anomalies, val_anomalies):
    """Visualise key anomaly findings."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Anomaly & Contradiction Analysis', fontsize=14, fontweight='bold')

    # 1. Governance paradox counts
    ax = axes[0, 0]
    paradox_names = [
        'Decent. + Company-Owned',
        'Gov Token + Team-Controlled',
        'DAO-Owned + No Governance',
        'Centralized + On-Chain Gov'
    ]
    paradox_counts = [
        len(gov_anomalies['decent_but_company']),
        len(gov_anomalies['gov_token_team_controlled']),
        len(gov_anomalies['dao_owned_no_governance']),
        len(gov_anomalies['centralized_onchain_gov']),
    ]
    colors = ['#e74c3c', '#e67e22', '#f39c12', '#d35400']
    ax.barh(paradox_names, paradox_counts, color=colors, edgecolor='black')
    ax.set_xlabel('Number of DApps')
    ax.set_title('Governance Contradictions Found', fontsize=11, fontweight='bold')
    for i, v in enumerate(paradox_counts):
        ax.text(v + 0.3, i, str(v), va='center', fontsize=10, fontweight='bold')

    # 2. MCap/User distribution highlighting anomalies
    ax = axes[0, 1]
    df_mkt = df[(df['market_cap'] > 0) & (df['users'] > 0)].copy()
    df_mkt['mcap_per_user'] = df_mkt['market_cap'] / df_mkt['users']
    threshold = df_mkt['mcap_per_user'].quantile(0.95)
    normal = df_mkt[df_mkt['mcap_per_user'] <= threshold]
    outlier = df_mkt[df_mkt['mcap_per_user'] > threshold]
    ax.scatter(normal['users'], normal['market_cap'], alpha=0.3, s=30,
               color='steelblue', label='Normal')
    ax.scatter(outlier['users'], outlier['market_cap'], alpha=0.7, s=60,
               color='red', label='Anomalous MCap/User', zorder=5)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Users (log)')
    ax.set_ylabel('Market Cap (log)')
    ax.set_title('Valuation Anomalies: MCap vs Users', fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)

    # 3. Funded vs Unfunded performance
    ax = axes[1, 0]
    df_funded = df[(df['raised_capital'] > 0) & (df['market_cap'] > 0)]
    df_unfunded = df[(df['raised_capital'].fillna(0) == 0) & (df['market_cap'] > 0)]
    ax.hist(np.log10(df_funded['market_cap']), bins=30, alpha=0.6,
            label=f'Funded (n={len(df_funded)})', color='steelblue')
    ax.hist(np.log10(df_unfunded['market_cap']), bins=30, alpha=0.6,
            label=f'Unfunded (n={len(df_unfunded)})', color='coral')
    ax.axvline(np.log10(df_funded['market_cap'].median()), color='blue',
               linestyle='--', label='Funded Median')
    ax.axvline(np.log10(df_unfunded['market_cap'].median()), color='red',
               linestyle='--', label='Unfunded Median')
    ax.set_xlabel('Log10(Market Cap)')
    ax.set_ylabel('Count')
    ax.set_title('Funded vs Unfunded Market Cap Distribution',
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=8)

    # 4. TVL/MCap ratio extremes
    ax = axes[1, 1]
    df_tvl = df[(df['tvl'] > 0) & (df['market_cap'] > 0)].copy()
    df_tvl['tvl_mcap_ratio'] = df_tvl['tvl'] / df_tvl['market_cap']
    ratio_clean = df_tvl[df_tvl['tvl_mcap_ratio'] < df_tvl['tvl_mcap_ratio'].quantile(0.98)]
    ax.hist(ratio_clean['tvl_mcap_ratio'], bins=50, color='mediumpurple',
            edgecolor='black', alpha=0.7)
    ax.axvline(1.0, color='red', linestyle='--', linewidth=2, label='TVL = MCap')
    ax.set_xlabel('TVL / Market Cap Ratio')
    ax.set_ylabel('Count')
    ax.set_title('TVL-to-Market-Cap Ratio Distribution', fontsize=11, fontweight='bold')
    ax.legend()

    plt.tight_layout()
    out = OUTPUT_DIR / '12_anomaly_dashboard.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {out}")
    plt.close()


def save_anomaly_report(gov_anomalies, val_anomalies, perf_outliers):
    """Save a text report of all anomalies for thesis discussion."""
    report_path = OUTPUT_DIR / '12_ANOMALY_REPORT.txt'
    with open(report_path, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("  ANOMALY & CONTRADICTION REPORT\n")
        f.write("  For thesis discussion section\n")
        f.write("=" * 70 + "\n\n")

        f.write("1. GOVERNANCE PARADOXES\n")
        f.write("-" * 40 + "\n")
        for key, label in [
            ('decent_but_company', 'Decentralized but Company-Owned'),
            ('gov_token_team_controlled', 'Governance Token but Team-Controlled'),
            ('dao_owned_no_governance', 'DAO-Owned but No Governance'),
            ('centralized_onchain_gov', 'Centralized with On-Chain Governance'),
        ]:
            subset = gov_anomalies[key]
            f.write(f"\n  {label}: {len(subset)} DApps\n")
            for _, r in subset.head(10).iterrows():
                f.write(f"    - {r['name']} (Gov: {r['governance_type']}, "
                        f"Own: {r['ownership_status']}, "
                        f"Dec: {r['level_of_decentralisation']})\n")

        f.write("\n\n2. VALUATION ANOMALIES\n")
        f.write("-" * 40 + "\n")
        a1 = val_anomalies['high_mcap_low_users']
        f.write(f"\n  Highest MCap-per-User (top 15):\n")
        for _, r in a1.iterrows():
            f.write(f"    - {r['name']}: MCap ${r['market_cap']:,.0f}, "
                    f"Users {r['users']:,.0f}\n")

        f.write(f"\n  Unfunded outperformers: "
                f"{len(val_anomalies['unfunded_outperformers'])} DApps\n")
        for _, r in val_anomalies['unfunded_outperformers'].nlargest(
                10, 'market_cap').iterrows():
            f.write(f"    - {r['name']}: MCap ${r['market_cap']:,.0f}\n")

        f.write(f"\n  Extreme TVL leverage (TVL > 10x MCap):\n")
        for _, r in val_anomalies['extreme_tvl_leverage'].iterrows():
            f.write(f"    - {r['name']}: TVL/MCap = "
                    f"{r['tvl_mcap_ratio']:.1f}x\n")

        f.write("\n\n3. PERFORMANCE OUTLIERS\n")
        f.write("-" * 40 + "\n")
        f.write(f"\n  Extremely high tx/user:\n")
        for _, r in perf_outliers['high_tx_per_user'].iterrows():
            f.write(f"    - {r['name']}: {r['tx_per_user']:.0f} tx/user\n")
        f.write(f"\n  High users, zero TVL: "
                f"{len(perf_outliers['high_users_no_tvl'])} DApps\n")

        f.write(f"\n\nDate: {pd.Timestamp.now().strftime('%Y-%m-%d')}\n")
        f.write("=" * 70 + "\n")

    print(f"✓ Saved anomaly report: {report_path}")


def main():
    print("\n" + "="*60)
    print("ANOMALY & CONTRADICTION ANALYSIS")
    print("="*60)

    df = load_prepared_data()

    gov_anomalies = detect_governance_paradoxes(df)
    val_anomalies = detect_valuation_anomalies(df)
    perf_outliers = detect_performance_outliers(df)
    visualize_anomalies(df, gov_anomalies, val_anomalies)
    save_anomaly_report(gov_anomalies, val_anomalies, perf_outliers)

    print("\n" + "="*60)
    print("ANOMALY ANALYSIS COMPLETE!")
    print("="*60)
    print("✓ All outputs saved to:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
