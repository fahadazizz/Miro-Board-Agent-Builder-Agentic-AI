import requests
import re
from typing import Dict, Any, List, Optional

try:
    from config import Config
    from models import BoardItem, Position
except ImportError:
    from .config import Config
    from .models import BoardItem, Position

class MiroClient:
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or Config.MIRO_ACCESS_TOKEN
        self.base_url = "https://api.miro.com/v2"
        
    def get_headers(self) -> Dict[str, str]:
        if not self.access_token:
            raise ValueError("Miro Access Token is missing.")
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json"
        }

    def get_board_id_from_url(self, url: str) -> str:
        match = re.search(r"board/([^/]+)", url)
        if match:
            return match.group(1)
        raise ValueError("Invalid Miro Board URL")

    def fetch_board_items(self, board_id: str) -> List[BoardItem]:
        items = []
        url = f"{self.base_url}/boards/{board_id}/items"
        params = {"limit": 50}
        
        while url:
            response = requests.get(url, headers=self.get_headers(), params=params)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch board items: {response.text}")
            
            data = response.json()
            for item_data in data.get("data", []):
                items.append(self._parse_item(item_data))
            
            url = data.get("links", {}).get("next")
            params = {}
            
        return items

    def _parse_item(self, data: Dict[str, Any]) -> BoardItem:
        pos_data = data.get("position", {})
        position = None
        if "x" in pos_data and "y" in pos_data:
            position = Position(x=pos_data["x"], y=pos_data["y"])
            
        content = ""
        if data["type"] == "sticky_note":
            content = data.get("data", {}).get("content", "")
        elif data["type"] == "text":
            content = data.get("data", {}).get("content", "")
        elif data["type"] == "shape":
             content = data.get("data", {}).get("content", "")
        
        content = self._clean_html(content)

        return BoardItem(
            id=data["id"],
            type=data["type"],
            content=content,
            position=position,
            parent_id=data.get("parent", {}).get("id"),
            style=data.get("style", {}),
            metadata=data
        )

    def _clean_html(self, raw_html: str) -> str:
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext
