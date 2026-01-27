import os
import shutil
import subprocess


def run(cmd: str):
    print(f"[RUN] {cmd}")
    # check=False so the pipeline continues even if a tool fails
    subprocess.run(cmd, shell=True, check=False)


def tool_exists(name: str) -> bool:
    return shutil.which(name) is not None


def run_nmap(target, outdir, cfg):
    if not tool_exists("nmap"):
        print("[SKIP] nmap not found in PATH")
        return

    args = cfg.get("tools", {}).get("nmap", {})
    profile = cfg.get("auto_run", {}).get("profile", "fast")

    nmap_args = (
        args.get("fast_args", "-Pn -T4 --top-ports 1000 -sVC -oX")
        if profile == "fast"
        else args.get("normal_args", "-Pn -p- -sVC -oX")
    )

    out = os.path.join(outdir, "nmap.xml")
    run(f"nmap {nmap_args} {out} {target}")


def run_httpx(target, outdir, cfg):
    if not tool_exists("httpx"):
        print("[SKIP] httpx not found in PATH")
        return

    out = os.path.join(outdir, "httpx.txt")
    args = cfg.get("tools", {}).get("httpx", {})
    httpx_args = args.get("args", "-title -tech-detect -status-code")

    # Use printf for safer echo across shells
    run(f"printf '%s\n' {target} | httpx {httpx_args} -o {out}")


def run_ffuf(target, outdir, cfg):
    if not tool_exists("ffuf"):
        print("[SKIP] ffuf not found in PATH")
        return

    args = cfg.get("tools", {}).get("ffuf", {})
    wl = args.get("wordlist", "/usr/share/wordlists/dirb/common.txt")
    ffuf_args = args.get("args", "-mc 200,204,301,302,307,401,403 -of json")

    scheme = args.get("scheme", "http")  # http|https
    url = args.get("url", f"{scheme}://{target}/FUZZ")

    out = os.path.join(outdir, "ffuf.json")
    run(f"ffuf -u '{url}' -w '{wl}' {ffuf_args} -o '{out}'")


def run_gobuster(target, outdir, cfg):
    if not tool_exists("gobuster"):
        print("[SKIP] gobuster not found in PATH")
        return

    args = cfg.get("tools", {}).get("gobuster", {})
    wl = args.get("wordlist", "/usr/share/wordlists/dirb/common.txt")
    gobuster_args = args.get("args", "dir -q")

    scheme = args.get("scheme", "http")  # http|https
    url = args.get("url", f"{scheme}://{target}")

    out = os.path.join(outdir, "gobuster.txt")
    # redirect stdout to file like your original behavior
    run(f"gobuster {gobuster_args} -u '{url}' -w '{wl}' > '{out}'")
