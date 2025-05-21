#!/usr/bin/env python3
from data_fetcher.db import create_tables

def main():
    create_tables()
    print("✅ Database schema initialized.")

if __name__ == "__main__":
    main()
