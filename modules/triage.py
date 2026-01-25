from typing import List
from .models import HostRecon

def triage_host(host: HostRecon, web_ports: List[int], highlight_ports: List[int]) -> None:
    # Tags based on ports
    open_ports = {s.port for s in host.services}
    for p in sorted(open_ports):
        if p in highlight_ports:
            host.tags.append(f"port:{p}")

    # Web detection
    for s in host.services:
        if s.port in web_ports:
            scheme = "https" if (s.tunnel == "ssl" or s.port in [443, 8443]) else "http"
            host.next_steps.append(f"Web: verify {scheme}://{host.ips[0] if host.ips else host.target}:{s.port}/")
            host.tags.append("web")

    # SMB hints
    if 445 in open_ports:
        host.tags.append("smb")
        host.next_steps.append("SMB: enumerate shares, users, and possible null sessions (CTF scope).")

    # SSH hints
    if 22 in open_ports:
        host.tags.append("ssh")
        host.next_steps.append("SSH: try creds found elsewhere; check banner/version for known issues.")

    # FTP hints
    if 21 in open_ports:
        host.tags.append("ftp")
        host.next_steps.append("FTP: check anonymous access; list files; look for backups.")

    # Deduplicate
    host.tags = sorted(set(host.tags))
    host.next_steps = list(dict.fromkeys(host.next_steps))
