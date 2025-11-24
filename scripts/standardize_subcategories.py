"""
Script to standardize sub_category values in the pilot dataset.
Handles typos, casing issues, and creates logical groupings.
Can also update the database with standardized values.
"""

import csv
import sys
import os
from collections import Counter
from configparser import ConfigParser
import psycopg2

# Load database config
_cfg = ConfigParser()
_cfg.read(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini'))
DB_NAME = _cfg["database"]["name"]
SUPERUSER = _cfg["database"]["user"]
PASSWORD = _cfg["database"]["password"]
HOST = _cfg["database"]["host"]
PORT = _cfg["database"]["port"]

def get_conn():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=SUPERUSER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )

# Define canonical sub-categories with standardization rules
STANDARDIZATION_MAP = {
    # ========== EXCHANGES ==========
    'exchanges': {
        # AMM DEX variants
        'AMM DEX': ['AMM DEX', 'AMM DEX & Liquidity pools', 'Immutable AMM DEX', 'SEI native AMM DEX'],
        'Concentrated Liquidity AMM': ['Concentrated-liquidity AMM DEX', 'Concentrated liquidity AMM'],
        'AMM DEX + Launchpad': ['AMM DEX + launchpad', 'AMM DEX + NFT marketplace', 'AMM DEX + NFT markeplace'],
        'DEX Aggregator': ['DEX aggregator', 'DEX/CEX aggregator', 'DEX aggregator / RFQ router', 'AMM aggregator', 'Cross-chain aggregator'],
        'Cross-chain DEX': ['Cross-chain DEX', 'Cross-chain DEX + bridge', 'Cross-chain swap aggregator'],
        'Perpetuals DEX': ['Perpetuals DEX', 'Perps DEX', 'Perps/DEX', 'Perps/order-book + DEX', 'Perps DEX + DAO', 'Perpertuals/futures DEX', 'DEX/perps'],
        'Order-book DEX': ['Order-book DEX'],
        'Stablecoin AMM': ['Stable-swap AMM', 'Stablecoin/FX AMM'],
        'PMM DEX': ['PMM-based AMM DEX'],
        'Portfolio AMM': ['Portfolio AMM / pools'],
        'NFT AMM': ['NFT AMM + liquidity mining', 'Fractionalized NFT AMM'],
        'DEX + Farming': ['DEX + farming', 'DEX + launchpad', 'Yield/DeFi trading suite'],
        'DEX Suite': ['DEX + NFT suite', 'XRPL/XAHAU DEX suite', 'DeFi tools hub'],
        'Trading Bot': ['Trading bot platform', 'Telegram Trading bot'],
        'Automated Vaults': ['Automated vaults + lending', 'Smart vaults/leverage'],
        'General DEX': ['DEX'],
    },
    
    # ========== DEFI ==========
    'defi': {
        # Lending & Borrowing
        'Money Market': ['Money market lending/borrowing', 'Lending/borrowing', 'Lending protocol', 'Lending', 'Lending optimizer', 'Liquidity hook/money-market'],
        'Credit & RWA Lending': ['Credit/RWA lending'],
        
        # Staking & Restaking
        'Liquid Staking': ['Liquid staking', 'Liquid staking / MEV'],
        'Restaking Protocol': ['Restaking protocol', 'Restaking DAO / treasury'],
        'Validator Staking': ['Validator staking'],
        'Token Staking': ['Token staking/yield', 'Staking'],
        
        # Bridges
        'Bridge': ['Bridge', 'Bridge/swap dashboard', 'Off-ramp/on-ramp & bridge', 'Cross-chain liquidity bridge', 'Cross-chain bridge / AMM', 'Cross-chain liquidity (DeBridge)'],
        'Modular Liquidity Layer': ['Modular liquidity layer (bridge/rollups)'],
        
        # Yield & Farming
        'Yield Optimizer': ['Yield optimizer', 'Yield farm suite', 'Yield tokenization / fixed rate AMM', 'Yield tool'],
        
        # Launchpads
        'Token Launchpad': ['Token launchpad', 'Token/Meme coin launchpad', 'Memecoin launchpad', 'IDO launchpad', 'AI token launchpad', 'No-code token launchpad', 'AI, no-code token launch'],
        
        # RWA
        'RWA Trading': ['RWA trading', 'RWA real-estate tokenization', 'RWA/NFT marketplace'],
        
        # Payments & Banking
        'Payments': ['Payments', 'Payments/liquidity network', 'Web3 bank'],
        
        # AI + DeFi
        'AI DeFi': ['AI + DeFi tooling', 'AI DeFi agents', 'AI agent platform'],
        
        # Other DeFi
        'Delta-neutral Stablecoin': ['Delta hegged dollar currency'],
        'Paymaster': ['Paymaster/gas abstraction for zkSync'],
        'Token Toolkit': ['Token toolkit', 'Tokenized rewards', 'Burn automation'],
        'Social Token Bridge': ['Social token / MPC bridge'],
        'DeFi Hub': ['DeFi hub', 'DeFi'],
        'Account Abstraction': ['Account/chain abstraction'],
    },
    
    # ========== GAMBLING ==========
    'gambling': {
        'Casino': ['GambleFi', 'Casino GambleFi', 'Casino aggergator', 'Casino coin flip', 'GambleFi coin flip', 'GambleFi roulette', 'GambleFi mini games', 'NFT casino', 'wheel spin GambleFi'],
        'Sportsbook': ['GambleFi Sportsbook', 'GambleFi sportsbook', 'On-chain Sportsbook', 'Decentralized sports betting protocol', 'GambleFi betting protocol'],
        'Prediction Market': ['Prediction market', 'Prediction + GambleFi', 'Predictions + GambleFi', 'Prediction + P2E'],
        'Lottery': ['Lottery/Raffles', 'Loot/raffles', 'Sweepstakes/competition gambleFi'],
        'GambleFi + P2E': ['GambleFi + P2E', 'GambleFi, P2E', 'PvP GambleFi'],
        'GambleFi + NFT': ['GambleFi + NFT'],
        'GambleFi Hybrid': ['GambleFi + staking', 'GambleFi + Betting DAO', 'GambleFi + meme project', 'GameFi + GambleFi', 'GameFi + Gambling', 'GameFi/GambleFi', 'memecoin + GambleFi', 'High-risk GambleFi + predictions'],
    },
    
    # ========== GAMES ==========
    'games': {
        'MMO': ['MMO + P2E', 'MMO + DAO GameFi', 'MMO sandbox GameFi', 'MMORPG GameFi', 'MMO RPG (GameFi / Metaverse)'],
        'RPG': ['Action RPG P2E', 'Idle/RPG P2E', 'P2E RPG', 'GameFi DEX + RPG'],
        'Arcade': ['Arcade P2E', 'Arcade P2E (Sei)', 'Arcade game hub P2E', 'Mobile P2E arcade'],
        'Strategy': ['Strategy GameFi'],
        'Racing': ['Racing GameFi'],
        'Shooter': ['Online shooter (Web 2.5)'],
        'Match-3': ['Match-3 P2E', 'Match-3 NFT GameFi'],
        'Farming': ['Farming GameFi', 'Farming MMO'],
        'Open World': ['Open-world GameFi'],
        'Quiz': ['On-chain quiz game'],
        'Telegram Game': ['Telegram P2E', 'Telegram match + mining', 'Telegram runner game'],
        'Clicker': ['P2E clicker', 'Clicker mini-app'],
        'Move-to-Earn': ['Move-to-earn', 'Move-2-Earn fitness app'],
        'P2E': ['P2E', 'Ummutable P2E', 'AI P2E', 'GameFi, P2E'],
        'GameFi Platform': ['GameFi', 'GameFi + marketplace', 'GameFi marketplace', 'L2-powered GameFi', 'GameFi Proof-of-play', 'GameFi + launchpad', 'Game/NFT ecosystem', 'Game marketplace', 'Game/content marketplace'],
        'GameFi + DeFi': ['GameFi + DeFi', 'GameFi + trading suite', 'GameFi + yield + staking', 'GameFi + Staking'],
        'GameFi Staking Hub': ['GameFi staking hub'],
        'Mobile Game': ['Mobile NFT game', 'Mobile Web3 game studio'],
        'Metaverse': ['Metaverse + GameFi', 'Metaverse mining + DAOs', 'Metaverse P2E'],
        'Game Hub': ['Web3 game hub', 'Web3 game studio'],
        'Wallet Quest': ['Wallet quest/campaign game', 'Quest platform + farming'],
        'Miniapp Game': ['Marketplace mini-app'],
    },
    
    # ========== MARKETPLACES ==========
    'marketplaces': {
        'NFT Marketplace': ['NFT marketplace', 'NFT markeplace', 'NFT marketplace + protocol', 'NFT minting + marketplace', 'NFT launchpad + marketplace', 'NFT marketplace + launchpad', 'SocialFi/NFT marketplace'],
        'NFT + Art Marketplace': ['NFT & Art marketplace', 'Art/NFT marketplace', 'AI art marketplace', 'Generative Art marketplace'],
        'NFT Launchpad': ['NFT launchpad/mint tool', 'NFT launchpad/promos', 'NFT minting + L2 protocol', 'Omnichain minting'],
        'NFT + Gaming': ['NFT GameFi + marketplace', 'P2E + marketplace', 'RWA/NFT marketplace'],
        'Creator Marketplace': ['Creator minting marketplace'],
        'Game Marketplace': ['Game marketplace', 'Game/content marketplace', 'Game + Metaverse marketplace', 'Fantasy Marketplace'],
        'Metaverse Marketplace': ['Metaverse + marketplace'],
        'Name Service': ['Name Service', 'Name service', 'Domain Name service (ENS)'],
        'Marketplace + Launchpad': ['Marketplace + launchpad'],
        'InfoFi Marketplace': ['InfoFi marketplace'],
        'NFT + DAO': ['NFT marketplace + DAO'],
        'Wallet Marketplace': ['Wallet + marketplace'],
        'NFT Casino': ['NFT casino'],
    },
    
    # ========== SOCIAL ==========
    'social': {
        'SocialFi Platform': ['SocialFi', 'Social Protocol', 'Open social protocol', 'SocialFi + creator platform', 'Network/creator tokenization (SocialFi)'],
        'SocialFi + Gaming': ['SocialFi + GameFi', 'SocialFi + Game', 'Quest + SocialFi + GameFi', 'SocialFi P2E', 'P2E + SocialFi', 'NFT P2E'],
        'SocialFi + Staking': ['SocialFi + Staking', 'SocialFi + staking', 'Creator staking + SocialFi'],
        'SocialFi Mint/Earn': ['SocialFi Mint-to-earn', 'Read-to-earn/content app'],
        'Quest Platform': ['Quest-to-earn SocialFi', 'Quest/Airdrop farming', 'Onboarding/drops tool', 'quests/games + telegram bot', 'Predictions + Quests/Airdrops', 'campaign/airdrops'],
        'Metaverse Social': ['Metaverse SocialFi', 'Metaverse + marketplace'],
        'Social Photo App': ['SocialFi photo app'],
        'Privacy Social': ['Privacy social app', 'Decentralized chat (ICP)'],
        'Social Blog': ['Social/blog platform'],
        'Social + NFT': ['Social + NFT hub'],
        'Education': ['Education SocialFi', 'Dev/Knowledge DAO'],
        'Messaging': ['On-chain messaging / SocialFi', 'Omnichain messaging'],
        'Move-to-Earn': ['Move-to-earn', 'DePIN Drive-to-earn'],
        'AI Social': ['AI social app', 'AI + SocialFi', 'AI content/SocialFi platform'],
        'Social Launchpad': ['SocialFi launchpad', 'DAO/community launchpad'],
        'ID Service': ['ID security protocol'],
        'Trading Card Game': ['Wax TCG SocialFi'],
        'Music NFTs': ['music NFTs & airdrops'],
        'Survey': ['Survey/data aggregator'],
        'ReFi': ['ReFi carbon protocol'],
        'Rewards Platform': ['Rewards + Marketplace', 'Rewards/mystery boxes'],
        'Wallet + DeFi': ['Wallet + DeFi'],
        'Social + App Suite': ['SocialFi + app suite'],
        'Prediction + P2E': ['Prediction + P2E'],
    },
    
    # ========== COLLECTIBLES ==========
    'collectibles': {
        'GameFi': ['GameFi', 'GameFi + marketplace', 'GameFi + trading suite'],
        'P2E': ['P2E', 'P2E RPG'],
        'NFT Marketplace': ['NFT marketplace'],
        'NFT Staking': ['NFT staking/yield'],
        'NFT + P2E': ['NFT + P2E'],
        'NFT + DEX': ['NFT + DEX suite'],
        'Token Launchpad': ['Token launchpad'],
        'DePIN': ['DePIN + GameFi', 'EV-charging DePIN'],
        'Metaverse': ['Metaverse P2E'],
        'AI Gaming': ['AI companion/dating GameFi', 'AI music agent'],
        'Art Marketplace': ['Art/NFT marketplace'],
        'RWA': ['RWA real-estate tokenization'],
        'Communication': ['Web3 mail / decentralized communication'],
        'Meme Token': ['Meme AI Token'],
        'NFT Launchpad': ['NFT launchpad/mint tool'],
        'Quest + NFT': ['Quests/NFT Marketplace'],
        'No-code NFT': ['No-code NFT suite'],
        'Marketplace Miniapp': ['Marketplace mini-app'],
        'Game Ecosystem': ['Game/NFT ecosystem'],
    },
    
    # ========== HIGH-RISK ==========
    'high-risk': {
        'High-risk ROI Scheme': ['High-risk ROI scheme', 'High-risk ROI mining', 'High-risk "mining" ROI', 'High-risk ROI/DEX', 'Bank ROI site', 'high-risk scheme'],
        'High-risk Yield': ['High-risk Yield', 'High-risk yield', 'High-risk Yield scheme', 'High-risk yield automation protocol', 'High-APR yield farm', 'High-yield staking site'],
        'High-risk Staking': ['High-risk staking', 'High-risk staking + yield'],
        'High-risk GambleFi': ['High-risk GambleFi + predictions'],
        'High-risk DeFi': ['High risk Defi', 'DeFi', 'DeFi + staking'],
        'High-risk Launchpad': ['NFT launchpad/promos', 'No-code token launchpad'],
        'High-risk Campaigns': ['High-risk campaign hub', 'campaign/airdrops'],
        'High-risk Gaming': ['GameFi', 'GambleFi', 'GameFi + yield + staking', 'P2E + NFT'],
        'High-risk Network': ['High-risk wallet/network app'],
        'Meme Token': ['Meme token', 'meme coin', 'meme project', 'meme app', 'meme coin/airdrops', 'meme/NFT site'],
        'Lottery': ['Loot/raffles'],
        'Yield Tool': ['Yield tool'],
        'DeFi Portal': ['DeFi/meme portal'],
    },
    
    # ========== OTHER ==========
    'other': {
        # AI Categories
        'AI Agent Platform': ['AI agent platform', 'Ai agent infra/protocol', 'AI trading agents', 'Ai orchestration + token'],
        'AI Compute': ['AI compute marketplace', 'AI/GPU node marketplace', 'P2P AI compute network'],
        'AI Launchpad': ['AI launchpad / staking hub', 'AI token launchpad', 'AI tools + launchpad', 'AI, no-code token launch'],
        'AI Staking': ['AI staking/yield'],
        'AI Gaming': ['AI + GameFi', 'AI P2E'],
        'AI Social': ['AI + SocialFi', 'AI content/SocialFi platform', 'AI social app', 'AI art marketplace'],
        'AI DeFi': ['AI + DeFi tooling', 'AI DeFi agents'],
        'AI Research': ['AI research platform', 'AI data labeling marketplace'],
        'AI Meme': ['AI meme token', 'Meme AI Token'],
        'AI Music': ['AI music agent'],
        
        # DePIN
        'DePIN': ['DePIN', 'DePIN/eSIM marketplace', 'DEPIN Wi-Fi rewards app', 'DePIN Drive-to-earn', 'EV-charging DePIN'],
        
        # DeSci
        'DeSci': ['DeSci PoW GameFi'],
        
        # Payments
        'Payments': ['Payments', 'Web3 card/finance app'],
        
        # Name Services
        'Name Service': ['Name Service', 'Name service', 'Domain Name service (ENS)'],
        
        # Staking
        'Staking': ['Staking', 'L2 staking/validator'],
        
        # Analytics
        'Analytics': ['on-chain analytics', 'analytics/terminal'],
        
        # Utilities
        'DEX Aggregator': ['DEX aggregator'],
        'Token Launchpad': ['Token launchpad', 'IDO launchpad'],
        'Solana Utility': ['Solana utility kit'],
        'Automation': ['Burn automation'],
        'Miniapp': ['Clicker mini-app'],
        'Tokenized BTC': ['Tokenized BTC hashrate'],
        'Omnichain': ['Omnichain messaging', 'Omnichain minting'],
        'Rewards': ['Rewards/mystery boxes', 'Tokenized rewards'],
        'DAO Tools': ['Dev/Knowledge DAO'],
        'Wearables': ['Wearables/Token app'],
        'Account Abstraction': ['Account/chain abstraction'],
        
        # Mixed/Unclear
        'GameFi': ['GameFi', 'GameFi, P2E'],
        'SocialFi': ['SocialFi', 'Metaverse SocialFi', 'SocialFi + GameFi'],
        'SocialFi Launchpad': ['SocialFi launchpad'],
        'Metaverse': ['Metaverse SocialFi'],
    },
}

def get_canonical_subcategory(main_category, sub_category):
    """Get the canonical (standardized) sub-category value"""
    if not sub_category:
        return ''
    
    main_cat = main_category.lower() if main_category else 'other'
    
    # Get the standardization map for this main category
    if main_cat not in STANDARDIZATION_MAP:
        main_cat = 'other'
    
    category_map = STANDARDIZATION_MAP[main_cat]
    
    # Find which canonical category this sub_category belongs to
    for canonical, variants in category_map.items():
        if sub_category in variants:
            return canonical
    
    # If no match found, return the original (cleaned up)
    return sub_category.strip()

def standardize_subcategories(input_csv, output_csv):
    """Standardize all sub_category values in the CSV"""
    
    print("🔄 Standardizing sub-categories...")
    print("=" * 80)
    
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        headers = reader.fieldnames
    
    # Track changes
    changes = []
    unchanged = 0
    
    for row in rows:
        original = row.get('sub_category', '').strip()
        main_category = row.get('dapp_category', '').strip()
        
        if original:
            canonical = get_canonical_subcategory(main_category, original)
            
            if canonical != original:
                changes.append({
                    'name': row['name'],
                    'category': main_category,
                    'original': original,
                    'canonical': canonical
                })
                row['sub_category'] = canonical
            else:
                unchanged += 1
    
    # Write standardized data
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"\n✅ Standardization complete!")
    print(f"  • Total sub-categories processed: {len([r for r in rows if r.get('sub_category')])}")
    print(f"  • Changed: {len(changes)}")
    print(f"  • Unchanged: {unchanged}")
    
    # Show sample changes
    if changes:
        print(f"\n📝 Sample changes (first 20):")
        for change in changes[:20]:
            print(f"  • {change['name']} ({change['category']})")
            print(f"    {change['original']} → {change['canonical']}")
    
    # Count new unique sub-categories
    new_subcats = Counter([row['sub_category'] for row in rows if row.get('sub_category')])
    print(f"\n📊 After standardization:")
    print(f"  • Unique sub-categories: {len(new_subcats)} (was 320)")
    
    print(f"\n💾 Standardized data saved to: {output_csv}")
    
    return len(changes), rows

def update_database_subcategories(standardized_rows):
    """Update sub_category values in the database"""
    
    print("\n" + "=" * 80)
    print("🔄 Updating database with standardized sub-categories...")
    print("=" * 80)
    
    conn = get_conn()
    cur = conn.cursor()
    
    stats = {
        'updated': 0,
        'not_found': 0,
        'skipped_empty': 0,
        'errors': 0
    }
    
    not_found_dapps = []
    error_dapps = []
    
    for idx, row in enumerate(standardized_rows, 1):
        dapp_name = row.get('name', '').strip()
        sub_category = row.get('sub_category', '').strip()
        
        if not dapp_name:
            continue
        
        if not sub_category:
            stats['skipped_empty'] += 1
            continue
        
        try:
            # Check if dapp exists
            cur.execute("SELECT id, sub_category FROM dapps WHERE name = %s", (dapp_name,))
            result = cur.fetchone()
            
            if not result:
                not_found_dapps.append(dapp_name)
                stats['not_found'] += 1
                continue
            
            dapp_id, current_sub_category = result
            
            # Update sub_category
            cur.execute(
                """
                UPDATE dapps 
                SET sub_category = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (sub_category, dapp_id)
            )
            
            stats['updated'] += 1
            
            if idx % 50 == 0:
                print(f"   ⏳ Processed {idx}/{len(standardized_rows)} rows...")
                conn.commit()
        
        except Exception as e:
            stats['errors'] += 1
            error_dapps.append((dapp_name, str(e)))
            print(f"   ❌ Error updating {dapp_name}: {e}")
    
    # Commit final changes
    conn.commit()
    
    print("\n" + "=" * 80)
    print("✅ Database update complete!")
    print("=" * 80)
    print(f"\n📊 Statistics:")
    print(f"  • Total rows processed: {len(standardized_rows)}")
    print(f"  • Successfully updated: {stats['updated']}")
    print(f"  • Skipped (no sub_category): {stats['skipped_empty']}")
    print(f"  • Not found in DB: {stats['not_found']}")
    print(f"  • Errors: {stats['errors']}")
    
    if not_found_dapps and len(not_found_dapps) <= 10:
        print(f"\n⚠️  DApps not found in database:")
        for dapp in not_found_dapps[:10]:
            print(f"    - {dapp}")
        if len(not_found_dapps) > 10:
            print(f"    ... and {len(not_found_dapps) - 10} more")
    
    if error_dapps and len(error_dapps) <= 5:
        print(f"\n❌ DApps with errors:")
        for dapp, error in error_dapps[:5]:
            print(f"    - {dapp}: {error}")
    
    cur.close()
    conn.close()
    
    return stats

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Standardize sub-categories in CSV and optionally update database')
    parser.add_argument(
        'input_file',
        nargs='?',
        default='/Users/kristian.kirilov/Downloads/pilot_dataset - pilot_dataset (1).csv',
        help='Input CSV file path'
    )
    parser.add_argument(
        'output_file',
        nargs='?',
        default='pilot_dataset_standardized.csv',
        help='Output CSV file path'
    )
    parser.add_argument(
        '--update-db',
        action='store_true',
        help='Update the database with standardized sub-categories'
    )
    parser.add_argument(
        '--db-only',
        action='store_true',
        help='Only update database without creating CSV (requires existing standardized CSV as input)'
    )
    
    args = parser.parse_args()
    
    if args.db_only:
        # Read standardized data and update DB
        print("📖 Reading standardized data from input file...")
        with open(args.input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        update_database_subcategories(rows)
    else:
        # Standardize and optionally update DB
        changes_count, standardized_rows = standardize_subcategories(args.input_file, args.output_file)
        
        if args.update_db:
            update_database_subcategories(standardized_rows)
        else:
            print("\n💡 Tip: Use --update-db flag to update the database with standardized values")
            print(f"   Example: python {sys.argv[0]} --update-db")

