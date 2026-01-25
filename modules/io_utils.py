import os
import json
from typing import Any


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def write_text(path: str, data: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)


def write_json(path: str, obj: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
