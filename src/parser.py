from typing import List, Dict

try:
    from models import BoardItem, StructuralGraph, Relation
except ImportError:
    from .models import BoardItem, StructuralGraph, Relation

class LayoutParser:
    def __init__(self, items: List[BoardItem]):
        self.items = {item.id: item for item in items}
        self.graph = StructuralGraph()
        self.graph.items = self.items

    def parse(self) -> StructuralGraph:
        self._identify_frames()
        self._identify_containment()
        self._identify_connectors()
        return self.graph

    def _identify_frames(self):
        for item in self.items.values():
            if item.type == "frame":
                self.graph.frames.append(item.id)

    def _identify_containment(self):
        for item in self.items.values():
            if item.parent_id and item.parent_id in self.items:
                self.graph.relations.append(Relation(
                    source_id=item.parent_id,
                    target_id=item.id,
                    type="contains"
                ))

    def _identify_connectors(self):
        for item in self.items.values():
            if item.type == "connector":
                data = item.metadata
                start_item = data.get("startItem", {}).get("id")
                end_item = data.get("endItem", {}).get("id")
                
                if start_item and end_item:
                    self.graph.relations.append(Relation(
                        source_id=start_item,
                        target_id=end_item,
                        type="connected_to",
                        label=item.content
                    ))
