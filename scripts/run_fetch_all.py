from dapp_scraper.scrapers.defillama  import fetch_defillama
from dapp_scraper.scrapers.dappradar  import fetch_dappradar
from dapp_scraper.store               import store_records

def main():
    dl = fetch_defillama(limit=100)
    dr = fetch_dappradar(limit=100)
    # (optionally) dd = fetch_deepdao(limit=100)

    store_records(dl)
    store_records(dr)
    # store_records(dd)

    print(f"✅ Fetched & stored: "
          f"{len(dl)} from DeFiLlama, "
          f"{len(dr)} from DappRadar.")
          # f", {len(dd)} from DeepDAO.")

if __name__ == "__main__":
    main()
