from typing import Dict, List
from defusedxml.ElementTree import parse
from .models import Service


def import_nmap_xml(xml_path: str) -> Dict[str, List[Service]]:
    tree = parse(xml_path)
    root = tree.getroot()

    results: Dict[str, List[Service]] = {}

    for host in root.findall("host"):
        addr = host.find("address")
        ip = addr.get("addr") if addr is not None else "unknown"

        services: List[Service] = []
        ports = host.find("ports")
        if ports is None:
            results[ip] = services
            continue

        for p in ports.findall("port"):
            proto = p.get("protocol", "")
            portid = int(p.get("portid", "0"))
            state = p.find("state")
            if state is None or state.get("state") != "open":
                continue

            svc = p.find("service")
            services.append(Service(
                port=portid,
                proto=proto,
                name=svc.get("name", "") if svc is not None else "",
                product=svc.get("product", "") if svc is not None else "",
                version=svc.get("version", "") if svc is not None else "",
                extrainfo=svc.get("extrainfo", "") if svc is not None else "",
                tunnel=svc.get("tunnel", "") if svc is not None else "",
            ))

        results[ip] = services

    return results
