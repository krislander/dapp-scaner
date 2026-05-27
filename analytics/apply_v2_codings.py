"""
apply_v2_codings.py
====================
Manual coding for the 68 strict-sample DApps for the 5 new v2_ columns.
Each coding was derived from dapp_sector / dapp_category / sub_category / tags /
description + public knowledge of the project as of Nov 2025 dataset snapshot.

Coding rubric references:
  - DATABASE_COLUMNS.md (allowed enum values)
  - docs/appendices/variable-codebook.md (how-to-code rules)
"""

import pandas as pd
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent

# ── 1. Manual coding table ────────────────────────────────────────────────────
# fmt: off
CODINGS = {
    "1inch Network": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=DEX, tags: binance-labs-portfolio, blockchain-capital-portfolio; DEX aggregator + swap protocol",
        "v2_coding_confidence": "HIGH",
    },
    "Aave V3": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "INTEREST_YIELD",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "INTEREST_MARGIN",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=Lending; flagship DeFi lending protocol with interest-rate model",
        "v2_coding_confidence": "HIGH",
    },
    "Across": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=Bridge/Router; cross-chain bridge charging relay fees; raised=357",
        "v2_coding_confidence": "HIGH",
    },
    "Aerodrome": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=exchanges, cat=DEX, base-ecosystem; ve(3,3) AMM on Base; no VC raise recorded",
        "v2_coding_confidence": "HIGH",
    },
    "Alien Worlds": {
        "v2_ecosystem_focus": "GAMING",
        "v2_sustainment_model": "TOKENOMICS",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "NONE_UNSET",
        "v2_funding_type": "TOKEN_SALE",
        "v2_ecosystem_focus_basis": "dapp_sector=games, tags: play-to-earn, gaming; TLM emission-driven; Binance Launchpool launch",
        "v2_coding_confidence": "MEDIUM",
    },
    "Alliance Games": {
        "v2_ecosystem_focus": "GAMING",
        "v2_sustainment_model": "TOKENOMICS",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "NONE_UNSET",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=games, cat=NFT Gaming, tags: animoca-brands-portfolio, play-to-earn; COA token economy",
        "v2_coding_confidence": "MEDIUM",
    },
    "Anome": {
        "v2_ecosystem_focus": "GAMING",
        "v2_sustainment_model": "TOKENOMICS",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "NONE_UNSET",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=games, sub_category includes Play 2 Earn; ANOME token; limited public info on VC",
        "v2_coding_confidence": "LOW",
    },
    "ApeBond": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=exchanges, cat=DEX, tags: DeFi, launchpad; bonding/bonding-fee protocol; no VC raise",
        "v2_coding_confidence": "MEDIUM",
    },
    "Arena of Faith": {
        "v2_ecosystem_focus": "GAMING",
        "v2_sustainment_model": "TOKENOMICS",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "NONE_UNSET",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=games, cat=NFT Gaming, sub=Play 2 Earn; AOF token; limited public funding info",
        "v2_coding_confidence": "LOW",
    },
    "Axie Infinity": {
        "v2_ecosystem_focus": "GAMING",
        "v2_sustainment_model": "MARKETPLACE_TAKE_RATE",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TAKE_RATE",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=games, tags: play-to-earn, animoca-brands-portfolio, Binance Launchpad; NFT marketplace take rate is primary revenue",
        "v2_coding_confidence": "HIGH",
    },
    "Backroom": {
        "v2_ecosystem_focus": "SOCIAL",
        "v2_sustainment_model": "MARKETPLACE_TAKE_RATE",
        "v2_go_to_market": "C2C",
        "v2_main_revenue_generator": "TAKE_RATE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=marketplaces, sub=Marketplace+Social, tags: Virtuals Protocol Ecosystem; social knowledge marketplace",
        "v2_coding_confidence": "LOW",
    },
    "Banana Gun": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=Social Network, tags: telegram-bot; Telegram trading bot charging swap fees",
        "v2_coding_confidence": "HIGH",
    },
    "Blur": {
        "v2_ecosystem_focus": "NFT",
        "v2_sustainment_model": "MARKETPLACE_TAKE_RATE",
        "v2_go_to_market": "C2C",
        "v2_main_revenue_generator": "TAKE_RATE",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=marketplaces, cat=Lending+NFT marketplace, tags: Paradigm Portfolio, NFT Marketplace; NFT trading platform",
        "v2_coding_confidence": "HIGH",
    },
    "ChainGPT": {
        "v2_ecosystem_focus": "AI",
        "v2_sustainment_model": "SUBSCRIPTION",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "USAGE_METERING",
        "v2_funding_type": "TOKEN_SALE",
        "v2_ecosystem_focus_basis": "dapp_sector=other, sub=AI Agent Platform, tags: ai-big-data; AI services platform (smart contract audits, NFT generator); CGPT token IDO",
        "v2_coding_confidence": "MEDIUM",
    },
    "ChainOpera AI": {
        "v2_ecosystem_focus": "AI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "USAGE_METERING",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=other, cat=Infrastructure, sub=AI DeFi, tags: ai-big-data, ai-applications; early-stage AI DeFi platform",
        "v2_coding_confidence": "LOW",
    },
    "DLN": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=Bridge/Router; deBridge limit-order cross-chain DEX; raised=38.5",
        "v2_coding_confidence": "HIGH",
    },
    "DeDust": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=exchanges, cat=DEX, sub=AMM DEX; TON-chain AMM; no VC raise on record",
        "v2_coding_confidence": "MEDIUM",
    },
    "DeFi Kingdoms": {
        "v2_ecosystem_focus": "GAMING",
        "v2_sustainment_model": "TOKENOMICS",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=games, tags: play-to-earn, gaming, metaverse; gamified DEX; JEWEL emission-funded; community built",
        "v2_coding_confidence": "MEDIUM",
    },
    "Dmail Network": {
        "v2_ecosystem_focus": "SOCIAL",
        "v2_sustainment_model": "SUBSCRIPTION",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "SUBSCRIPTION",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=collectibles, sub=NFT Marketplace+Social+Privacy; Web3 email/communication platform; premium subscription model",
        "v2_coding_confidence": "MEDIUM",
    },
    "DragonSwap": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=exchanges, cat=DEX, sub=AMM DEX, tags: Sei Network Ecosystem; Sei-chain AMM; no VC raise",
        "v2_coding_confidence": "MEDIUM",
    },
    "Dypius": {
        "v2_ecosystem_focus": "GAMING",
        "v2_sustainment_model": "TOKENOMICS",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "NONE_UNSET",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=games, cat=NFT Gaming, tags: gaming, metaverse; DYP token-driven gaming/metaverse ecosystem",
        "v2_coding_confidence": "LOW",
    },
    "Ethereum Name Service": {
        "v2_ecosystem_focus": "INFRA",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "LISTING_FEES",
        "v2_funding_type": "GRANT_FOUNDATION",
        "v2_ecosystem_focus_basis": "dapp_sector=other, cat=Privacy/Security, sub=Identity+DAO Tooling, tags: web3, Name Service; ENS domain registration; Ethereum Foundation grant-originated",
        "v2_coding_confidence": "HIGH",
    },
    "Etherex": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=DEX, tags: Linea Ecosystem; small DEX on Linea; limited public info",
        "v2_coding_confidence": "LOW",
    },
    "FishWar": {
        "v2_ecosystem_focus": "GAMING",
        "v2_sustainment_model": "TOKENOMICS",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "NONE_UNSET",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=games, cat=NFT Gaming, tags: On-chain Gaming, Sei Network Ecosystem; FISHW token P2E game",
        "v2_coding_confidence": "LOW",
    },
    "GoodDollar": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "DONATIONS_GRANTS",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "NONE_UNSET",
        "v2_funding_type": "GRANT_FOUNDATION",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=Wallet, sub=Wallet+DAO Tooling; UBI protocol grant-funded by eToro/GoodDollar Foundation; raised=7",
        "v2_coding_confidence": "MEDIUM",
    },
    "Helio": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=other, cat=Payments/RWA, tags: Solana Ecosystem; Solana payment infrastructure enabling merchants/developers",
        "v2_coding_confidence": "MEDIUM",
    },
    "Helix": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=DEX, sub=Perpetuals+AMM DEX; perpetuals DEX; Base meme ecosystem; no VC raise",
        "v2_coding_confidence": "LOW",
    },
    "Jito": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=Derivatives, sub=Liquid Staking+Staking; Solana liquid staking + MEV; top-tier crypto VCs (a16z-backed)",
        "v2_coding_confidence": "HIGH",
    },
    "KGeN": {
        "v2_ecosystem_focus": "GAMING",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=games, sub=Identity+NFT Marketplace; gamer ID & rewards platform; raised=13.5",
        "v2_coding_confidence": "MEDIUM",
    },
    "Karat Galaxy": {
        "v2_ecosystem_focus": "GAMING",
        "v2_sustainment_model": "TOKENOMICS",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "NONE_UNSET",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=games, cat=NFT Gaming, sub=Play 2 Earn+Staking; KARAT token P2E; no VC on record",
        "v2_coding_confidence": "LOW",
    },
    "Layer3": {
        "v2_ecosystem_focus": "SOCIAL",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2B2C",
        "v2_main_revenue_generator": "LISTING_FEES",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=social, cat=Social Network, sub=Social+Identity+DAO Tooling, tags: Quest-to-Earn; campaign/quest platform; projects pay listing fees",
        "v2_coding_confidence": "MEDIUM",
    },
    "Lingo": {
        "v2_ecosystem_focus": "GAMING",
        "v2_sustainment_model": "TOKENOMICS",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "NONE_UNSET",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=games, cat=Payments/RWA, sub=Tokenized rewards+Play 2 Earn; LINGO reward token; no VC raise",
        "v2_coding_confidence": "LOW",
    },
    "MEET48": {
        "v2_ecosystem_focus": "SOCIAL",
        "v2_sustainment_model": "MARKETPLACE_TAKE_RATE",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TAKE_RATE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=other, cat=Metaverse, sub=Social+Metaverse, tags: music, entertainment; K-pop idol NFT/social platform; digital content marketplace",
        "v2_coding_confidence": "LOW",
    },
    "Magic Eden": {
        "v2_ecosystem_focus": "NFT",
        "v2_sustainment_model": "MARKETPLACE_TAKE_RATE",
        "v2_go_to_market": "C2C",
        "v2_main_revenue_generator": "TAKE_RATE",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=marketplaces, cat=NFT marketplace, tags: Paradigm Portfolio, Sequoia Capital Portfolio; leading NFT marketplace",
        "v2_coding_confidence": "HIGH",
    },
    "Maple": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "INTEREST_YIELD",
        "v2_go_to_market": "B2B",
        "v2_main_revenue_generator": "INTEREST_MARGIN",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=Lending, sub=Lending+RWA, tags: real-world-assets-protocols; institutional undercollateralised lending; raised=123.9; Framework+Circle Ventures",
        "v2_coding_confidence": "HIGH",
    },
    "Mento": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "SPREAD",
        "v2_funding_type": "GRANT_FOUNDATION",
        "v2_ecosystem_focus_basis": "dapp_sector=exchanges, cat=DEX, sub=Stablecoin+AMM DEX, tags: Celo Ecosystem; stablecoin exchange protocol; raised=70 from Celo Foundation ecosystem",
        "v2_coding_confidence": "MEDIUM",
    },
    "Merchant Moe": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=exchanges, cat=DEX, sub=AMM DEX+Farming, tags: mantle-ecosystem; Mantle-native AMM DEX",
        "v2_coding_confidence": "MEDIUM",
    },
    "Mitosis": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "PERFORMANCE_FEE",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=DAO Tooling, sub=Yield Optimizer+Farming; modular yield protocol; VC-backed (BNB ecosystem raise)",
        "v2_coding_confidence": "MEDIUM",
    },
    "Moonwell": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "INTEREST_YIELD",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "INTEREST_MARGIN",
        "v2_funding_type": "GRANT_FOUNDATION",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=Lending, sub=Lending+Yield Optimizer; lending protocol on Moonbeam+Base; raised=70 via Polkadot/Moonbeam ecosystem",
        "v2_coding_confidence": "MEDIUM",
    },
    "Morpho": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "INTEREST_YIELD",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "INTEREST_MARGIN",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=Lending, tags: Coinbase Ventures, Pantera, Fenbushi; peer-to-peer lending optimiser",
        "v2_coding_confidence": "HIGH",
    },
    "ODOS": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "SPREAD",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=exchanges, cat=DEX, sub=DEX Aggregator, tags: cross-chain-dex-aggregator; positive slippage / surplus capture as revenue",
        "v2_coding_confidence": "MEDIUM",
    },
    "OpenOcean": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=DEX, sub=Aggregator; full-aggregation DEX; raised=14; Binance Labs portfolio",
        "v2_coding_confidence": "MEDIUM",
    },
    "Overtime": {
        "v2_ecosystem_focus": "PREDICTION_MARKETS",
        "v2_sustainment_model": "SPREAD_ARB",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "SPREAD",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=gambling, cat=Casino, sub=Prediction Market, tags: Prediction Markets, Sportsbooks; on-chain sportsbook earning spread",
        "v2_coding_confidence": "HIGH",
    },
    "ParaSwap": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "SPREAD",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=exchanges, cat=DEX, sub=DEX Aggregator, tags: Spartan Group; positive slippage aggregator",
        "v2_coding_confidence": "MEDIUM",
    },
    "Pendle": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=Derivatives, sub=Yield Optimizer+Derivatives, tags: Spartan Group; yield tokenisation protocol; raised=25.9",
        "v2_coding_confidence": "HIGH",
    },
    "Pixels": {
        "v2_ecosystem_focus": "GAMING",
        "v2_sustainment_model": "MARKETPLACE_TAKE_RATE",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TAKE_RATE",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=games, cat=NFT Gaming, tags: Animoca Brands Portfolio, Binance Launchpool, Ronin Ecosystem; farm game with NFT marketplace",
        "v2_coding_confidence": "HIGH",
    },
    "Pump.fun": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=DEX, sub=Token Launchpad+AMM DEX; Solana meme token launchpad; 1% creation fee + swap fees",
        "v2_coding_confidence": "HIGH",
    },
    "QuickSwap": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=exchanges, cat=DEX, sub=AMM DEX+Perpetuals, tags: polygon-ecosystem; leading Polygon DEX; community fork, no VC",
        "v2_coding_confidence": "HIGH",
    },
    "RavenQuest": {
        "v2_ecosystem_focus": "GAMING",
        "v2_sustainment_model": "MARKETPLACE_TAKE_RATE",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TAKE_RATE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=games, cat=NFT Gaming, tags: MMO, RPG, Immutable zkEVM; in-game item marketplace",
        "v2_coding_confidence": "LOW",
    },
    "Raydium": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=exchanges, cat=DEX, sub=AMM DEX+Token Launchpad, tags: solana-ecosystem, amm; leading Solana AMM; no VC raise recorded",
        "v2_coding_confidence": "HIGH",
    },
    "Rhea Finance": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=DEX, sub=AMM DEX+Yield Optimizer; NEAR-native DEX; raised=68.6; Dragonfly+OKX Ventures",
        "v2_coding_confidence": "MEDIUM",
    },
    "Rubic": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=DEX, sub=Aggregator; cross-chain swap aggregator; no VC raise on record",
        "v2_coding_confidence": "MEDIUM",
    },
    "SecondLive": {
        "v2_ecosystem_focus": "SOCIAL",
        "v2_sustainment_model": "MARKETPLACE_TAKE_RATE",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TAKE_RATE",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=other, cat=NFT marketplace, sub=Metaverse+Social, tags: binance-labs-portfolio; metaverse social platform",
        "v2_coding_confidence": "MEDIUM",
    },
    "Stargate": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=Bridge/Router, sub=Bridge+Farming; LayerZero bridge protocol; no VC raise (community launch)",
        "v2_coding_confidence": "HIGH",
    },
    "SuperWalk": {
        "v2_ecosystem_focus": "GAMING",
        "v2_sustainment_model": "TOKENOMICS",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "NONE_UNSET",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=games, cat=NFT marketplace, sub=Play 2 Earn, tags: Move to Earn; GRND token walk-to-earn; no VC raise",
        "v2_coding_confidence": "MEDIUM",
    },
    "SushiSwap": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=exchanges, cat=DEX, sub=AMM DEX+Farming, tags: amm, yield-farming; community-forked Uniswap DEX; DAO-governed",
        "v2_coding_confidence": "HIGH",
    },
    "SynFutures": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=DEX, sub=Perpetuals+Derivatives; on-chain perps DEX; raised=261.8; Polychain+Dragonfly+Pantera",
        "v2_coding_confidence": "HIGH",
    },
    "The Arena": {
        "v2_ecosystem_focus": "SOCIAL",
        "v2_sustainment_model": "MARKETPLACE_TAKE_RATE",
        "v2_go_to_market": "C2C",
        "v2_main_revenue_generator": "TAKE_RATE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=social, cat=SocialFi, sub=SocialFi, tags: Avalanche Ecosystem; social key trading platform (friend.tech model)",
        "v2_coding_confidence": "HIGH",
    },
    "VVS Finance": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TX_FEE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=exchanges, cat=DEX, sub=AMM DEX+Farming, tags: cronos-ecosystem; leading Cronos AMM DEX",
        "v2_coding_confidence": "HIGH",
    },
    "Velo": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "INTEREST_YIELD",
        "v2_go_to_market": "B2B",
        "v2_main_revenue_generator": "INTEREST_MARGIN",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=Payments/RWA, sub=Payments+Staking; B2B stablecoin credit/settlement network; no VC raise",
        "v2_coding_confidence": "MEDIUM",
    },
    "Velora": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "FEES",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "SPREAD",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=exchanges, cat=DEX, sub=DEX Aggregator, tags: Spartan Group; rebranded ParaSwap with intent-based routing",
        "v2_coding_confidence": "MEDIUM",
    },
    "Virtuals Protocol": {
        "v2_ecosystem_focus": "AI",
        "v2_sustainment_model": "MARKETPLACE_TAKE_RATE",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TAKE_RATE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=Metaverse, sub=AI Agent Platform, tags: ai-agents, ai-agent-launchpad; AI agent launch + trading marketplace",
        "v2_coding_confidence": "HIGH",
    },
    "WiFi Map": {
        "v2_ecosystem_focus": "DEPIN",
        "v2_sustainment_model": "TOKENOMICS",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "ADS",
        "v2_funding_type": "VC_TRADITIONAL",
        "v2_ecosystem_focus_basis": "dapp_sector=other, cat=Payments/RWA, sub=Tokenized rewards, tags: depin, iot; crowd-sourced WiFi map app; ad-funded; traditional app company turned DePIN",
        "v2_coding_confidence": "MEDIUM",
    },
    "World of Dypians": {
        "v2_ecosystem_focus": "GAMING",
        "v2_sustainment_model": "MARKETPLACE_TAKE_RATE",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TAKE_RATE",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=games, cat=NFT marketplace, sub=Metaverse+NFT Marketplace, tags: RPG, MMO; blockchain MMO with NFT marketplace",
        "v2_coding_confidence": "LOW",
    },
    "WorldShards": {
        "v2_ecosystem_focus": "GAMING",
        "v2_sustainment_model": "TOKENOMICS",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "NONE_UNSET",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=games, cat=Payments/RWA, sub=Play 2 Earn, tags: RPG, Gaming; SHARDS token; no VC raise",
        "v2_coding_confidence": "LOW",
    },
    "XPIN Network": {
        "v2_ecosystem_focus": "DEPIN",
        "v2_sustainment_model": "TOKENOMICS",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "NONE_UNSET",
        "v2_funding_type": "BOOTSTRAPPED",
        "v2_ecosystem_focus_basis": "dapp_sector=other, cat=DAO Tooling, tags: iot, depin; IoT/DePIN infrastructure token project; no VC raise",
        "v2_coding_confidence": "LOW",
    },
    "ZeroLend": {
        "v2_ecosystem_focus": "DEFI",
        "v2_sustainment_model": "INTEREST_YIELD",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "INTEREST_MARGIN",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=defi, cat=Lending, sub=Lending+Yield Optimizer, tags: Linea Ecosystem, Account Abstraction; lending protocol; raised=15",
        "v2_coding_confidence": "MEDIUM",
    },
    "Zora": {
        "v2_ecosystem_focus": "NFT",
        "v2_sustainment_model": "MARKETPLACE_TAKE_RATE",
        "v2_go_to_market": "B2C",
        "v2_main_revenue_generator": "TAKE_RATE",
        "v2_funding_type": "VC_CRYPTO_NATIVE",
        "v2_ecosystem_focus_basis": "dapp_sector=marketplaces, cat=NFT marketplace, sub=Infrastructure+Marketplace, tags: Coinbase Ventures Portfolio, Zora Ecosystem; NFT minting protocol",
        "v2_coding_confidence": "HIGH",
    },
}
# fmt: on


def apply_codings(df: pd.DataFrame, codings: dict) -> pd.DataFrame:
    """Apply the manual codings to rows whose name matches CODINGS keys."""
    coding_cols = [
        "v2_ecosystem_focus", "v2_sustainment_model", "v2_go_to_market",
        "v2_main_revenue_generator", "v2_funding_type",
        "v2_ecosystem_focus_basis", "v2_coding_confidence",
    ]
    # Ensure target columns are object dtype so string assignment works
    for col in coding_cols:
        if col in df.columns:
            df[col] = df[col].astype(object)
    coded, skipped = 0, []
    for name, vals in codings.items():
        mask = df["name"] == name
        if mask.sum() == 0:
            skipped.append(name)
            continue
        for col, val in vals.items():
            df.loc[mask, col] = val
        coded += 1
    if skipped:
        print(f"WARNING – {len(skipped)} names not found in dataset: {skipped}")
    print(f"Coded {coded}/{len(codings)} DApps.")
    return df


def main():
    input_path  = ROOT / "DAPP_Dataset_Nov_2025 - Final_ENRICHED.xlsx"
    output_path = ROOT / "DAPP_Dataset_Nov_2025 - Final_ENRICHED_v2coded.xlsx"
    log_path    = ROOT / "analytics" / "v2_coding_log.md"

    xls = pd.ExcelFile(input_path)
    sheets = {name: pd.read_excel(input_path, sheet_name=name) for name in xls.sheet_names}
    sheet_name = xls.sheet_names[0]
    df = sheets[sheet_name]

    df = apply_codings(df, CODINGS)
    sheets[sheet_name] = df

    with pd.ExcelWriter(output_path, engine="openpyxl") as w:
        for name, sdf in sheets.items():
            sdf.to_excel(w, sheet_name=name, index=False)
    print(f"Saved enriched workbook → {output_path}")

    # ── Verification ──────────────────────────────────────────────────────────
    with open("analytics_merged/outputs/cohort_manifest.json") as f:
        manifest = json.load(f)
    strict_names = []
    for s in manifest["primary_slices"]:
        strict_names.extend(s["selected_names"])

    strict_df = df[df["name"].isin(strict_names)]
    check_cols = ["v2_ecosystem_focus", "v2_sustainment_model", "v2_go_to_market",
                  "v2_main_revenue_generator", "v2_funding_type",
                  "v2_ecosystem_focus_basis", "v2_coding_confidence"]
    print("\n=== Completeness check for strict sample ===")
    for col in check_cols:
        n_null = strict_df[col].isna().sum()
        print(f"  {col}: {len(strict_df) - n_null}/{len(strict_df)} populated (null={n_null})")

    # ── Coding log ────────────────────────────────────────────────────────────
    lines = ["# V2 Coding Log — Strict Sample (N=68)\n",
             f"Generated: {pd.Timestamp.today().date()}\n",
             "Source references: dapp_sector / dapp_category / sub_category / tags from DappRadar+CMC+CoinGecko+DeFiLlama; "
             "public protocol documentation; DeFiLlama funding data; CoinGecko investor tags.\n\n",
             "| DApp | ecosystem_focus | sustainment_model | go_to_market | main_revenue_generator | funding_type | confidence |\n",
             "|------|-----------------|-------------------|--------------|------------------------|--------------|------------|\n"]
    for name, c in sorted(CODINGS.items()):
        lines.append(
            f"| {name} | {c['v2_ecosystem_focus']} | {c['v2_sustainment_model']} | "
            f"{c['v2_go_to_market']} | {c['v2_main_revenue_generator']} | "
            f"{c['v2_funding_type']} | {c['v2_coding_confidence']} |\n"
        )
    lines.append("\n## Basis notes per DApp\n\n")
    for name, c in sorted(CODINGS.items()):
        lines.append(f"**{name}**: {c['v2_ecosystem_focus_basis']}\n\n")

    log_path.write_text("".join(lines))
    print(f"Coding log written → {log_path}")


if __name__ == "__main__":
    main()
