#!/usr/bin/env python3
from data_fetcher.db import store
from data_fetcher.fetchers.website_a import fetch_defillama
from data_fetcher.fetchers.website_b import fetch_dappradar
from data_fetcher.utils import fetch_deepdao

def main():
    # fetch top 100 from each source
    dl = fetch_defillama(limit=100)
    dr = fetch_dappradar(limit=100)
    dd = fetch_deepdao(limit=100)

    # store into DB
    store(dl)
    store(dr)
    store(dd)

    print(f"✅ Fetched & stored: "
          f"{len(dl)} from DeFiLlama, "
          f"{len(dr)} from DappRadar, "
          f"{len(dd)} from DeepDAO.")

if __name__ == "__main__":
    main()
