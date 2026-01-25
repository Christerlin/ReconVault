from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class Service:
    port: int
    proto: str
    name: str = ""
    product: str = ""
    version: str = ""
    extrainfo: str = ""
    tunnel: str = ""


@dataclass
class WebFinding:
    url: str
    status: Optional[int] = None
    title: str = ""
    server: str = ""
    technologies: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


@dataclass
class ContentDiscoveryItem:
    tool: str
    url: str
    status: Optional[int] = None
    length: Optional[int] = None
    words: Optional[int] = None
    redirect: str = ""


@dataclass
class HostRecon:
    target: str
    ips: List[str] = field(default_factory=list)
    hostnames: List[str] = field(default_factory=list)
    services: List[Service] = field(default_factory=list)
    web: List[WebFinding] = field(default_factory=list)
    content_discovery: List[ContentDiscoveryItem] = field(default_factory=list)
    raw_files: Dict[str, List[str]] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    next_steps: List[str] = field(default_factory=list)


@dataclass
class ReconRun:
    project_name: str
    generated_at: str
    hosts: List[HostRecon] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)
