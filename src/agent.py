import json
import requests
import re
from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END

try:
    from config import Config
    from miro_client import MiroClient
    from parser import LayoutParser
except ImportError:
    from .config import Config
    from .miro_client import MiroClient
    from .parser import LayoutParser

# --- State Definition ---
class AgentState(TypedDict):
    board_url: str
    board_id: str
    raw_items: list
    structural_graph: Dict[str, Any]
    agent_dsl: Dict[str, Any]
    error: str

# --- Nodes ---

def fetch_board_data(state: AgentState):
    print(f"Fetching data for board: {state['board_url']}")
    try:
        client = MiroClient()
        board_id = client.get_board_id_from_url(state['board_url'])
        items = client.fetch_board_items(board_id)
        return {"board_id": board_id, "raw_items": items}
    except Exception as e:
        return {"error": str(e)}

def parse_structure(state: AgentState):
    print("Parsing board structure...")
    try:
        if state.get("error"):
            return {}
        
        parser = LayoutParser(state['raw_items'])
        graph = parser.parse()
        return {"structural_graph": graph.dict()}
    except Exception as e:
        return {"error": str(e)}

def extract_json(text: str) -> Dict[str, Any]:
    """
    Robustly extract JSON from a string that might contain markdown or other text.
    """
    # 1. Try direct parsing
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 2. Remove markdown code blocks
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 3. Find the first '{' and the last '}'
    start = text.find('{')
    end = text.rfind('}')
    
    if start != -1 and end != -1 and end > start:
        json_str = text[start:end+1]
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
            
    raise ValueError(f"Could not extract valid JSON from response: {text[:100]}...")

def generate_dsl(state: AgentState):
    print("Generating Agent DSL...")
    if state.get("error"):
        return {}

    graph_data = json.dumps(state['structural_graph'], indent=2)
    
    system_prompt = """
    You are an expert AI Architect. Your goal is to analyze the structural data of a Miro board and convert it into a formal Agent Build DSL (JSON).
    
    The Miro board represents a visual plan for a Multi-Agent System or a Single Agent.
    - Frames usually represent logical groupings, workflow steps, or specific Sub-Agents.
    - Shapes/Text inside frames represent details, instructions, or tools.
    - Arrows/Connectors represent flow or relationships.
    
    Differentiate between "Sub-Agents" and "Tools":
    - **Sub-Agents**: Autonomous entities that perform complex tasks (e.g., "Researcher", "Reviewer", "Coder"). Often represented by Frames or distinct groupings.
    - **Tools**: Specific functions or capabilities used by agents (e.g., "search_web", "read_file").
    
    Output MUST be a valid JSON object matching the following schema (AgentSpec):
    {
        "name": "SystemName",
        "role": "Orchestrator/Manager",
        "goal": "Overall Goal",
        "type": "orchestrator",
        "sub_agents": [
            {"name": "AgentName", "role": "Role", "description": "...", "goal": "..."}
        ],
        "tools": [
            {"name": "tool_name", "description": "..."}
        ],
        "workflows": [
            {
                "name": "WorkflowName",
                "description": "...",
                "steps": [
                    {
                        "step_id": 1, 
                        "description": "...", 
                        "assigned_to": "AgentName or System",
                        "tools_required": ["tool_name"]
                    }
                ]
            }
        ]
    }
    
    Analyze the graph carefully. Infer the architecture from the visual layout.
    IMPORTANT: Return ONLY the JSON object. Do not include markdown formatting or explanations.
    """
    
    payload = {
        "model": Config.OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the structural graph of the board:\n{graph_data}"}
        ],
        "format": "json",
        "stream": False
    }
    
    try:
        response = requests.post(f"{Config.OLLAMA_BASE_URL}/api/chat", json=payload)
        response.raise_for_status()
        result = response.json()
        content = result.get("message", {}).get("content", "{}")
        
        # Use robust extraction
        dsl_json = extract_json(content)
        
        return {"agent_dsl": dsl_json}
    except Exception as e:
        return {"error": f"LLM Generation failed: {str(e)}"}

# --- Graph Construction ---

workflow = StateGraph(AgentState)

workflow.add_node("fetch_data", fetch_board_data)
workflow.add_node("parse_structure", parse_structure)
workflow.add_node("generate_dsl", generate_dsl)

workflow.set_entry_point("fetch_data")

workflow.add_edge("fetch_data", "parse_structure")
workflow.add_edge("parse_structure", "generate_dsl")
workflow.add_edge("generate_dsl", END)

app = workflow.compile()
