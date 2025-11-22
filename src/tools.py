import json
import re
from typing import Dict, Any, List
try:
    from miro_client import MiroClient
    from parser import LayoutParser
except ImportError:
    from .miro_client import MiroClient
    from .parser import LayoutParser

def fetch_board_info(board_url: str) -> Dict[str, Any]:
    """
    Tool to fetch board items from Miro.
    """
    try:
        client = MiroClient()
        board_id = client.get_board_id_from_url(board_url)
        items = client.fetch_board_items(board_id)
        return {"board_id": board_id, "raw_items": items}
    except Exception as e:
        return {"error": str(e)}

def parse_board_items(raw_items: List[Any]) -> Dict[str, Any]:
    """
    Tool to parse raw Miro items into a structural graph.
    """
    try:
        parser = LayoutParser(raw_items)
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
