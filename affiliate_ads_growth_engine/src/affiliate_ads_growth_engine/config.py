import json
from pathlib import Path

class ConfigLoader:
 def __init__(self, path: str | Path | None = None):
 self.path = Path(path or "config/default_workspace.json")

 def load(self):
 with open(self.path) as f:
 return json.load(f)
