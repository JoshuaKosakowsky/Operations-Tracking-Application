"""One relational schema, using SQLite locally and PostgreSQL on the host."""

from sqlalchemy import (
    Column, Float, Integer, MetaData, String, Table, Text, create_engine,
)
from sqlalchemy.pool import StaticPool

metadata = MetaData()
jobs = Table(
    "jobs", metadata,
    Column("id", String(36), primary_key=True),
    Column("day", String(10), nullable=False, index=True),
    Column("time", String(5), nullable=False),
    Column("title", String(120), nullable=False),
    Column("customer", String(100), nullable=False),
    Column("site", String(200), nullable=False),
    Column("crew", String(80), nullable=False),
    Column("status", String(20), nullable=False),
    Column("travel_minutes", Integer, nullable=False),
    Column("site_minutes", Integer, nullable=False),
    Column("miles", Float, nullable=False),
    Column("modules", Integer, nullable=False),
    Column("notes", Text, nullable=False),
    Column("version", Integer, nullable=False),
    Column("updated_at", String(40), nullable=False),
)
sessions = Table(
    "sessions", metadata,
    Column("token_hash", String(64), primary_key=True),
    Column("expires", Float, nullable=False),
    Column("code_hash", String(64), nullable=False),
)
limits = Table(
    "limits", metadata,
    Column("bucket", String(100), primary_key=True),
    Column("count", Integer, nullable=False),
    Column("expires", Float, nullable=False),
)


def connect(url):
    options = {"pool_pre_ping": True, "hide_parameters": True}
    if url.startswith("sqlite:"):
        options["connect_args"] = {"check_same_thread": False, "timeout": 10}
        if url.endswith(":memory:"):
            options["poolclass"] = StaticPool
    else:
        options.update(pool_size=3, max_overflow=2, pool_timeout=10)
        options["connect_args"] = {"connect_timeout": 10}
    return create_engine(url, **options)
