from .models import ReconRun

def render_txt(run: ReconRun) -> str:
    out = []
    out.append(f"{run.project_name} Recon Report")
    out.append(f"Generated: {run.generated_at}")
    out.append("=" * 60)

    for h in run.hosts:
        out.append(f"\nTARGET: {h.target}")
        if h.ips: out.append(f"IPs: {', '.join(h.ips)}")
        if h.hostnames: out.append(f"Hostnames: {', '.join(h.hostnames)}")
        if h.tags: out.append(f"Tags: {', '.join(h.tags)}")

        out.append("\nOpen Services:")
        if not h.services:
            out.append("  - none")
        else:
            for s in sorted(h.services, key=lambda x: (x.proto, x.port)):
                out.append(f"  - {s.port}/{s.proto} {s.name} {s.product} {s.version} {s.extrainfo}".strip())

        out.append("\nNext Steps:")
        if not h.next_steps:
            out.append("  - none")
        else:
            for step in h.next_steps:
                out.append(f"  - {step}")

    return "\n".join(out)
