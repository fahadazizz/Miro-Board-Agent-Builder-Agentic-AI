from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field

# --- Unified Structural Model (Internal Representation) ---

class Position(BaseModel):
    x: float
    y: float

class BoardItem(BaseModel):
    id: str
    type: str
    content: str = ""
    position: Optional[Position] = None
    parent_id: Optional[str] = None # For items inside frames
    style: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Relation(BaseModel):
    source_id: str
    target_id: str
    type: str # e.g., "connected_to", "contains", "visually_near"
    label: Optional[str] = None

class StructuralGraph(BaseModel):
    items: Dict[str, BoardItem] = Field(default_factory=dict)
    relations: List[Relation] = Field(default_factory=list)
    frames: List[str] = Field(default_factory=list) # List of frame IDs

# --- Agent Build DSL (Output Format) ---

class AgentTool(BaseModel):
    name: str
    description: str
    arguments: Optional[Dict[str, str]] = None

class SubAgent(BaseModel):
    name: str
    role: str
    description: str
    goal: Optional[str] = None

class AgentStep(BaseModel):
    step_id: int
    description: str
    # Can be a tool name OR an agent name
    assigned_to: Optional[str] = None 
    tools_required: List[str] = Field(default_factory=list)
    expected_output: Optional[str] = None

class AgentWorkflow(BaseModel):
    name: str
    description: str
    steps: List[AgentStep]

class AgentSpec(BaseModel):
    name: str
    role: str
    goal: str
    type: str = "orchestrator" # 'orchestrator' or 'agent'
    sub_agents: List[SubAgent] = Field(default_factory=list)
    tools: List[AgentTool] = Field(default_factory=list)
    workflows: List[AgentWorkflow] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Orchestrator",
                "role": "Manager",
                "goal": "Manage sub-agents",
                "sub_agents": [{"name": "Researcher", "role": "Research", "description": "..."}],
                "tools": [{"name": "search", "description": "..."}],
                "workflows": []
            }
        }
