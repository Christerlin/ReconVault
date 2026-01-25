from dataclasses import asdict
from .models import ReconRun

def to_json_obj(run: ReconRun):
    return asdict(run)
