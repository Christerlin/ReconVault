# ReconVault 🧭

ReconVault is a **CTF & lab-oriented reconnaissance framework** written in Python.  
Its goal is to **centralize, normalize, and analyze reconnaissance data** in order to speed up the transition from recon to exploitation.

⚠️ **ReconVault is intended for authorized environments only**: CTFs, labs, training ranges, or systems you own/have permission to test.

---

## ✨ Features

- 🔎 Automated or import-based reconnaissance
- 📥 Supports multiple tools:
  - Nmap (ports & services)
  - FFUF (directory & endpoint discovery)
  - Gobuster (content discovery)
  - Httpx (web fingerprinting)
- 🧠 Recon triage & attack-surface analysis
- 🗂️ Organized per-target workspace
- 📝 Report generation in:
  - Markdown (`.md`)
  - Plain text (`.txt`)
  - JSON (`.json`)
- 🧱 Modular & extensible architecture

---

## 🧩 Workflow Overview

1. Enter one or more targets interactively
2. (Optional) ReconVault runs recon tools automatically (Linux/Kali)
3. Import and normalize tool outputs
4. Analyze results (ports, services, web entry points)
5. Generate structured reports + next steps

---

## 📁 Project Structure

ReconVault/
├── reconvault.py
├── config.yaml
├── requirements.txt
├── modules/
│ ├── models.py
│ ├── runner.py
│ ├── io_utils.py
│ ├── import_nmap_xml.py
│ ├── import_ffuf_json.py
│ ├── import_gobuster_txt.py
│ ├── triage.py
│ ├── report_md.py
│ ├── report_txt.py
│ └── report_json.py
├── output/
│ └── <target>/
│ ├── raw/
│ ├── report.md
│ ├── report.txt
│ └── report.json
└── README.md


---

## ⚙️ Installation

### Clone the repository
```bash
git clone https://github.com/Christerlin/ReconVault.git
cd ReconVault
````
##Create virtual environment (recommended)
````
python3 -m venv venv
source venv/bin/activate
````
##Install Python dependencies
````
pip install -r requirements.txt
````
##Usage
````
python3 reconvault.py
````
##Enable auto-run in config.yaml
````
auto_run:
  enabled: true
  profile: "fast"

tools:
  nmap:
    enabled: true
  httpx:
    enabled: true
  ffuf:
    enabled: true
  gobuster:
    enabled: true

````
##Legal Notice

ReconVault does not bypass authorization.
You are responsible for ensuring that all targets are explicitly permitted (CTF, labs, or owned systems).

##Contributing

This project is educational.
Pull requests, ideas, and improvements are welcome.

##Author

Built by Christerlin as part of hands-on cybersecurity training and CTF practice.
