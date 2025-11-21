import json
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parser import LayoutParser
from src.models import BoardItem

def test_parser():
    print("Testing LayoutParser...")
    with open("tests/sample_miro_data.json", "r") as f:
        raw_data = json.load(f)
    
    # Mock parsing raw dict to BoardItem since MiroClient usually does this
    items = []
    for d in raw_data["data"]:
        # Simplified mock conversion
        item = BoardItem(
            id=d["id"],
            type=d["type"],
            content=d.get("data", {}).get("content", "") or d.get("data", {}).get("title", ""),
            parent_id=d.get("parent", {}).get("id"),
            metadata=d.get("metadata", {})
        )
        items.append(item)
        
    parser = LayoutParser(items)
    graph = parser.parse()
    
    print("Frames:", graph.frames)
    print("Relations:", len(graph.relations))
    
    assert "frame_1" in graph.frames
    assert len(graph.relations) >= 2 # 2 containments + 1 connector
    print("Parser Test Passed!")

if __name__ == "__main__":
    test_parser()
