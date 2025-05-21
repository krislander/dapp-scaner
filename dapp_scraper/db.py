from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, Numeric,
    TIMESTAMP, create_engine
)
from sqlalchemy.sql import func

from data_fetcher.utils import get_database_url

# read DB URL from config
DB_URL = get_database_url()
engine = create_engine(DB_URL, echo=False)
meta = MetaData()

# table definition
dapps = Table(
    "dapps", meta,
    Column("id",         Integer,   primary_key=True),
    Column("source",     String(50), nullable=False),
    Column("name",       String(255),nullable=False),
    Column("slug",       String(255),nullable=False),
    Column("category",   String(100)),
    Column("tvl",        Numeric,    default=0),
    Column("users",      Integer,    default=0),
    Column("fetched_at", TIMESTAMP,  server_default=func.now())
)

def create_tables():
    """Create tables in the database (if not exist)."""
    meta.create_all(engine)

def store(records):
    """Insert a list of dicts into the dapps table."""
    from sqlalchemy import insert
    from sqlalchemy.exc import IntegrityError
    from datetime import datetime

    with engine.begin() as conn:
        for rec in records:
            stmt = insert(dapps).values(**rec, fetched_at=datetime.utcnow())
            try:
                conn.execute(stmt)
            except IntegrityError:
                # skip duplicates or violations
                continue
