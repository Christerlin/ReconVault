import json
from typing import List
from .models import ContentDiscoveryItem


def import_ffuf_json(path: str) -> List[ContentDiscoveryItem]:
    """
    Parse ffuf JSON output (-of json)
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    items: List[ContentDiscoveryItem] = []

    for r in data.get("results", []):
        items.append(
            ContentDiscoveryItem(
                tool="ffuf",
                url=r.get("url", ""),
                status=r.get("status"),
                length=r.get("length"),
                words=r.get("words"),
                redirect=r.get("redirectlocation", "") or ""
            )
        )

    return items
