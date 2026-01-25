from .models import ReconRun
from datetime import datetime

def render_md(run: ReconRun) -> str:
    lines = []
    lines.append(f"# {run.project_name} Recon Report")
    lines.append(f"- Generated: `{run.generated_at}`")
    lines.append("")

    for h in run.hosts:
        lines.append(f"## Target: {h.target}")
        if h.ips:
            lines.append(f"- IPs: {', '.join(h.ips)}")
        if h.hostnames:
            lines.append(f"- Hostnames: {', '.join(h.hostnames)}")
        if h.tags:
            lines.append(f"- Tags: {', '.join(h.tags)}")
        lines.append("")

        lines.append("### Open Services")
        if not h.services:
            lines.append("_No services imported._")
        else:
            lines.append("| Port | Proto | Service | Product | Version | Extra |")
            lines.append("|---:|:---:|:---|:---|:---|:---|")
            for s in sorted(h.services, key=lambda x: (x.proto, x.port)):
                lines.append(f"| {s.port} | {s.proto} | {s.name} | {s.product} | {s.version} | {s.extrainfo} |")
        lines.append("")

        lines.append("### Content Discovery (Imported)")
        if not h.content_discovery:
            lines.append("_No discovery results imported._")
        else:
            lines.append("| Tool | URL | Status | Length | Words | Redirect |")
            lines.append("|:---|:---|---:|---:|---:|:---|")
            for it in h.content_discovery[:200]:
                lines.append(f"| {it.tool} | {it.url} | {it.status or ''} | {it.length or ''} | {it.words or ''} | {it.redirect} |")
            if len(h.content_discovery) > 200:
                lines.append(f"\n_Showing first 200 of {len(h.content_discovery)} results._")
        lines.append("")

        lines.append("### Next Steps")
        if not h.next_steps:
            lines.append("_No triage steps generated._")
        else:
            for step in h.next_steps:
                lines.append(f"- {step}")
        lines.append("")

        if h.raw_files:
            lines.append("### Raw Evidence Paths")
            for k, v in h.raw_files.items():
                lines.append(f"- **{k}**:")
                for p in v:
                    lines.append(f"  - `{p}`")
            lines.append("")

    return "\n".join(lines)
