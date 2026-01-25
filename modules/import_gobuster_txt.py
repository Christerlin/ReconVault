from typing import List
from .models import ContentDiscoveryItem
from .io_utils import read_text

def import_gobuster_txt(path: str) -> List[ContentDiscoveryItem]:
    """
    Very basic parser for gobuster dir output lines like:
    /admin (Status: 301) [Size: 0]
    """
    text = read_text(path)
    items: List[ContentDiscoveryItem] = []

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "Status:" not in line:
            continue

        # crude parse
        url_part = line.split(" ", 1)[0]
        status = None
        size = None

        try:
            status = int(line.split("Status:")[1].split(")")[0].strip())
        except Exception:
            pass
        try:
            if "Size:" in line:
                size = int(line.split("Size:")[1].split("]")[0].strip())
        except Exception:
            pass

        items.append(ContentDiscoveryItem(
            tool="gobuster",
            url=url_part,
            status=status,
            length=size
        ))
    return items
