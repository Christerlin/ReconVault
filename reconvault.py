import os
import yaml
from datetime import datetime, timezone
DEBUG = False
from modules.models import ReconRun, HostRecon
from modules.runner import run_nmap, run_httpx, run_ffuf, run_gobuster
from modules.io_utils import ensure_dir, write_text, write_json
from modules.import_nmap_xml import import_nmap_xml
from modules.import_ffuf_json import import_ffuf_json
from modules.import_gobuster_txt import import_gobuster_txt
from modules.triage import triage_host
from modules.report_md import render_md
from modules.report_txt import render_txt
from modules.report_json import to_json_obj
print("[DBG] reconvault.py loaded")



def load_config(path="config.yaml"):
    if not os.path.exists(path):
        raise SystemExit(f"[CONFIG] Missing {path}. Run from the project root (ReconVault/).")

    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    if cfg is None:
        raise SystemExit(f"[CONFIG] {path} is empty or invalid YAML.")
    if not isinstance(cfg, dict):
        raise SystemExit(f"[CONFIG] {path} must contain a YAML dictionary at top-level.")

    return cfg



def parse_targets_from_input(user_in: str):
    """
    Accepts:
      - single target: 10.10.10.10
      - multiple separated by space/commas:
          10.10.10.10 10.10.10.11
          10.10.10.10,10.10.10.11
          10.10.10.10, 10.10.10.11
    """
    user_in = user_in.strip()
    if not user_in:
        return []
    # split on commas then spaces
    parts = []
    for chunk in user_in.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts.extend([p.strip() for p in chunk.split() if p.strip()])
    # dedupe while preserving order
    seen = set()
    targets = []
    for t in parts:
        if t not in seen:
            seen.add(t)
            targets.append(t)
    return targets


def confirm_scope(targets):
    print("\n[SCOPE] You should only run this on targets you are authorized to test (CTF/lab).")
    print("[SCOPE] Targets entered:")
    for t in targets:
        print(f"  - {t}")
    ans = input("\nType 'I AGREE' to continue: ").strip()
    if ans != "I AGREE":
        raise SystemExit("[STOP] Scope confirmation not provided.")


def main():
    print("[DBG] main() entered")
    cfg = load_config()
    project = cfg.get("project_name", "ReconVault")
    out_dir = cfg.get("output_dir", "output")
    ensure_dir(out_dir)

    # Ask targets interactively
    raw = input("Enter target(s) (space or comma separated): ")
    targets = parse_targets_from_input(raw)
    if not targets:
        raise SystemExit("No targets provided.")

    confirm_scope(targets)

    run = ReconRun(
        project_name=project,
        generated_at=datetime.now(timezone.utc).isoformat(),
        meta={"imports": cfg.get("imports", {}), "report": cfg.get("report", {})}
    )

    # Safe defaults if config sections are missing
    auto_run_cfg = cfg.get("auto_run", {"enabled": False})
    tools_cfg = cfg.get("tools", {})
    imports_cfg = cfg.get("imports", {})
    report_cfg = cfg.get("report", {"formats": ["md", "txt", "json"]})
    triage_cfg = cfg.get("triage", {
        "web_ports": [80, 443, 8080, 8000, 8443],
        "highlight_ports": [80, 443, 8080, 8443, 22, 21, 445, 3389]
    })

    for target in targets:
        host = HostRecon(target=target, ips=[target])
        base = os.path.join(out_dir, target)
        raw_dir = os.path.join(base, "raw")
        ensure_dir(raw_dir)

        # Auto-run tools if enabled
        if auto_run_cfg.get("enabled", False):
            print(f"\n[AUTO] Running tools for {target}")

            if tools_cfg.get("nmap", {}).get("enabled", False):
                run_nmap(target, raw_dir, cfg)

            if tools_cfg.get("httpx", {}).get("enabled", False):
                run_httpx(target, raw_dir, cfg)

            if tools_cfg.get("ffuf", {}).get("enabled", False):
                run_ffuf(target, raw_dir, cfg)

            if tools_cfg.get("gobuster", {}).get("enabled", False):
                run_gobuster(target, raw_dir, cfg)

        # Import Nmap XML (if present)
        nmap_path = os.path.join(raw_dir, "nmap.xml")
        if imports_cfg.get("nmap_xml", True) and os.path.exists(nmap_path):
            data = import_nmap_xml(nmap_path)
            if target in data:
                host.services = data[target]
            elif host.ips and host.ips[0] in data:
                host.services = data[host.ips[0]]
            elif len(data) == 1:
                host.services = list(data.values())[0]
            host.raw_files.setdefault("nmap_xml", []).append(nmap_path)

        # Import ffuf json (if present)
        ffuf_path = os.path.join(raw_dir, "ffuf.json")
        if imports_cfg.get("ffuf_json", True) and os.path.exists(ffuf_path):
            host.content_discovery.extend(import_ffuf_json(ffuf_path))
            host.raw_files.setdefault("ffuf_json", []).append(ffuf_path)

        # Import gobuster txt (if present)
        gob_path = os.path.join(raw_dir, "gobuster.txt")
        if imports_cfg.get("gobuster_txt", True) and os.path.exists(gob_path):
            host.content_discovery.extend(import_gobuster_txt(gob_path))
            host.raw_files.setdefault("gobuster_txt", []).append(gob_path)

        # Triage
        triage_host(
            host,
            web_ports=triage_cfg["web_ports"],
            highlight_ports=triage_cfg["highlight_ports"]
        )

        run.hosts.append(host)

        # Per-host reports
        formats = report_cfg.get("formats", ["md", "txt", "json"])
        if "md" in formats:
            write_text(os.path.join(base, "report.md"),
                       render_md(ReconRun(project, run.generated_at, [host], run.meta)))
        if "txt" in formats:
            write_text(os.path.join(base, "report.txt"),
                       render_txt(ReconRun(project, run.generated_at, [host], run.meta)))
        if "json" in formats:
            write_json(os.path.join(base, "report.json"),
                       to_json_obj(ReconRun(project, run.generated_at, [host], run.meta)))

    # Global report
    formats = report_cfg.get("formats", ["md", "txt", "json"])
    if "md" in formats:
        write_text(os.path.join(out_dir, "ALL_REPORT.md"), render_md(run))
    if "txt" in formats:
        write_text(os.path.join(out_dir, "ALL_REPORT.txt"), render_txt(run))
    if "json" in formats:
        write_json(os.path.join(out_dir, "ALL_REPORT.json"), to_json_obj(run))

    print(f"\n[OK] Reports generated in: {out_dir}")
if __name__ == "__main__":
    print("[DBG] __main__ block running")
    main()
