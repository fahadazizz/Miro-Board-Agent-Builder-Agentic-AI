import json
import requests
from typing import TypedDict, Dict, Any, List
from langgraph.graph import StateGraph, END

try:
    from config import Config
    from prompts import ARCHITECT_PROMPT, WORKFLOW_PLANNER_PROMPT, DSL_GENERATOR_PROMPT
    from tools import fetch_board_info, parse_board_items, extract_json
except ImportError:
    from .config import Config
    from .prompts import ARCHITECT_PROMPT, WORKFLOW_PLANNER_PROMPT, DSL_GENERATOR_PROMPT
    from .tools import fetch_board_info, parse_board_items, extract_json

# --- State Definition ---
class AgentState(TypedDict):
    board_url: str
    board_id: str
    raw_items: list
    structural_graph: Dict[str, Any]
    
    # Intermediate Artifacts
    identified_components: Dict[str, Any] # sub_agents, tools
    workflow_plan: Dict[str, Any] # workflows
    
    agent_dsl: Dict[str, Any]
    error: str

# --- Helper for LLM Calls ---
def call_llm(prompt: str, data: str) -> Dict[str, Any]:
    payload = {
        "model": Config.OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Context Data:\n{data}"}
        ],
        "format": "json",
        "stream": False
    }
    try:
        response = requests.post(f"{Config.OLLAMA_BASE_URL}/api/chat", json=payload)
        response.raise_for_status()
        result = response.json()
        content = result.get("message", {}).get("content", "{}")
        return extract_json(content)
    except Exception as e:
        raise Exception(f"LLM Call Failed: {str(e)}")

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

def architect_agent_node(state: AgentState):
    print("Architect Agent: Identifying components...")
    if state.get("error"):
        return {}
    
    graph_data = json.dumps(state['structural_graph'], indent=2)
    try:
        components = call_llm(ARCHITECT_PROMPT, graph_data)
        return {"identified_components": components}
    except Exception as e:
        return {"error": str(e)}

def workflow_planner_node(state: AgentState):
    print("Workflow Planner: Designing workflows...")
    if state.get("error"):
        return {}
    
    # Combine graph and components for context
    context = {
        "structural_graph": state['structural_graph'],
        "identified_components": state['identified_components']
    }
    context_str = json.dumps(context, indent=2)
    
    try:
        plan = call_llm(WORKFLOW_PLANNER_PROMPT, context_str)
        return {"workflow_plan": plan}
    except Exception as e:
        return {"error": str(e)}

def dsl_generator_node(state: AgentState):
    print("DSL Generator: Synthesizing final plan...")
    if state.get("error"):
        return {}
    
    context = {
        "components": state['identified_components'],
        "workflows": state['workflow_plan']
    }
    context_str = json.dumps(context, indent=2)
    
    try:
        dsl = call_llm(DSL_GENERATOR_PROMPT, context_str)
        return {"agent_dsl": dsl}
    except Exception as e:
        return {"error": str(e)}

# --- Graph Construction ---

workflow = StateGraph(AgentState)

workflow.add_node("fetch_data", fetch_data_node)
workflow.add_node("parse_structure", parse_structure_node)
workflow.add_node("architect_agent", architect_agent_node)
workflow.add_node("workflow_planner", workflow_planner_node)
workflow.add_node("dsl_generator", dsl_generator_node)

workflow.set_entry_point("fetch_data")

workflow.add_edge("fetch_data", "parse_structure")
workflow.add_edge("parse_structure", "architect_agent")
workflow.add_edge("architect_agent", "workflow_planner")
workflow.add_edge("workflow_planner", "dsl_generator")
workflow.add_edge("dsl_generator", END)

app = workflow.compile()
