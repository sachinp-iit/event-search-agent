# schemas/knowledge_graph_schema.py

from pydantic import BaseModel, Field

# =========================================================
# KNOWLEDGE GRAPH SCHEMA
# =========================================================

# Knowledge Graph Entity Schema 
class EntitySchema(BaseModel):
    """
    Represents an extract entity
    """
    
    name: str = Field(description="Entity name.")
    
    type: str = Field(description="Entity Type.")
    
    
# Knowledge Graph Relationship Schema
class RelationshipSchema(BaseModel):
    """
    Represents a relationship between two entities.
    """
    
    source: str = Field(description="Source entity.")
    
    target: str = Field(description="Target entity.")
    
    relation: str = Field(description="Relationship between the entities.")
    
    
# Knowledge Graph Schema
class KnowledgeGraphSchema(BaseModel):
    """
    Structured knowledge graph extracted from conversation.
    """
    
    entities: list[EntitySchema] = Field(default_factory=list)
    
    relations: list[RelationshipSchema] = Field(default_factory=list)