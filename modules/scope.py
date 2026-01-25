import ipaddress
from typing import List


def load_targets(path: str) -> List[str]:
    targets: List[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            targets.append(line)
    return targets


def is_private_ip(s: str) -> bool:
    try:
        return ipaddress.ip_address(s).is_private
    except ValueError:
        return False


def enforce_scope(target: str, allowed: List[str], allow_private_ranges: bool = True) -> None:
    """
    Strict scope guard:
      - allow if exact match in allowed list
      - optionally allow private IPs if allow_private_ranges is True AND allowed list includes at least one private IP
    """
    if target in allowed:
        return

    if allow_private_ranges and is_private_ip(target):
        if any(is_private_ip(t) for t in allowed):
            return

    raise SystemExit(f"[SCOPE] Target '{target}' not in allowed scope list.")
