import subprocess
import os

def run(cmd: str):
    print(f"[RUN] {cmd}")
    subprocess.run(cmd, shell=True, check=False)


def run_nmap(target, outdir, cfg):
    args = cfg["tools"]["nmap"]
    profile = cfg["auto_run"]["profile"]
    nmap_args = args["fast_args"] if profile == "fast" else args["normal_args"]
    out = os.path.join(outdir, "nmap.xml")
    run(f"nmap {nmap_args} {out} {target}")


def run_httpx(target, outdir, cfg):
    out = os.path.join(outdir, "httpx.txt")
    args = cfg["tools"]["httpx"]["args"]
    run(f"echo {target} | httpx {args} -o {out}")


def run_ffuf(target, outdir, cfg):
    args = cfg["tools"]["ffuf"]
    wl = args["wordlist"]
    out = os.path.join(outdir, "ffuf.json")
    run(f"ffuf -u http://{target}/FUZZ -w {wl} {args['args']} -o {out}")


def run_gobuster(target, outdir, cfg):
    args = cfg["tools"]["gobuster"]
    wl = args["wordlist"]
    out = os.path.join(outdir, "gobuster.txt")
    run(f"gobuster {args['args']} -u http://{target} -w {wl} > {out}")
