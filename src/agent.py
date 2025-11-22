import json
import requests
from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END

try:
    from config import Config
    from prompts import DSL_GENERATION_PROMPT
    from tools import fetch_board_info, parse_board_items, extract_json
except ImportError:
    from .config import Config
    from .prompts import DSL_GENERATION_PROMPT
    from .tools import fetch_board_info, parse_board_items, extract_json

# --- State Definition ---
class AgentState(TypedDict):
    board_url: str
    board_id: str
    raw_items: list
    structural_graph: Dict[str, Any]
    agent_dsl: Dict[str, Any]
    error: str

# --- Nodes ---

def fetch_data_node(state: AgentState):
    print(f"Fetching data for board: {state['board_url']}")
    result = fetch_board_info(state['board_url'])
    if "error" in result:
        return {"error": result["error"]}
    return result

def parse_structure_node(state: AgentState):
    print("Parsing board structure...")
    if state.get("error"):
        return {}
    
    result = parse_board_items(state['raw_items'])
    if "error" in result:
        return {"error": result["error"]}
    return result

def generate_dsl_node(state: AgentState):
    print("Generating Agent DSL...")
    if state.get("error"):
        return {}

    graph_data = json.dumps(state['structural_graph'], indent=2)
    
    payload = {
        "model": Config.OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": DSL_GENERATION_PROMPT},
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
        
        # Use robust extraction from tools
        dsl_json = extract_json(content)
        
        return {"agent_dsl": dsl_json}
    except Exception as e:
        return {"error": f"LLM Generation failed: {str(e)}"}

# --- Graph Construction ---

workflow = StateGraph(AgentState)

workflow.add_node("fetch_data", fetch_data_node)
workflow.add_node("parse_structure", parse_structure_node)
workflow.add_node("generate_dsl", generate_dsl_node)

workflow.set_entry_point("fetch_data")

workflow.add_edge("fetch_data", "parse_structure")
workflow.add_edge("parse_structure", "generate_dsl")
workflow.add_edge("generate_dsl", END)

app = workflow.compile()
