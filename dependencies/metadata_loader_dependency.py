# database/metadata_loader_dependency.py

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.database_dependency import database_dependency

from storage.metadata_loader import MetadataLoader


# =========================================================
# METADATA LOADER DEPENDENCY
# =========================================================
async def metadata_loader_dependency(
    db_session: AsyncSession = Depends (database_dependency)
) -> MetadataLoader:
    
    """
    Dependency provider for MetadataLoader.
    """
    
    return MetadataLoader(db_session = db_session)
    