# database/sql_server_client.py

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

from config.settings import settings

from collections.abc import AsyncGenerator


# =========================================================
# SQL SERVER ENGINE
# =========================================================

_engine = create_async_engine (
    settings.SQL_SERVER_CONNECTION_STRING,
    pool_pre_ping = True,
    pool_size = 10,
    max_overflow = 20
)


# =========================================================
# SESSION FACTORY
# =========================================================
_session_factory = async_sessionmaker (
    bind = _engine,
    expire_on_commit = False,
    class_ = AsyncSession
)


# =========================================================
# SESSION PROVIDER
# =========================================================
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async SQL Server session provider.
    """
    
    async with _session_factory() as session:
        yield session