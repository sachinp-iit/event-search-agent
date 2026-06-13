# dependency/database_dependency.py

from sqlalchemy.ext.asyncio import AsyncSession

from database.sql_server_client import get_db_session

from collections.abc import AsyncGenerator

# =========================================================
# DATABASE DEPENDENCY
# =========================================================
async def database_dependency() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides async SQL Server Session.
    """
    async for session in get_db_session():
        yield session