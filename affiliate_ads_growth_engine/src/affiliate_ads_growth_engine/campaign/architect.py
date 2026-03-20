from typing import List, Dict

class CampaignArchitect:
 def __init__(self, budget_split: Dict[str, float] | None = None):
 self.budget_split = budget_split or {"CBO":0.6, "ABO":0.4}

 def build_structure(self, objectives: List[str]):
 structure = {
 "budgets": self.budget_split,
 "campaigns": []
 }
 for obj in objectives:
 structure["campaigns"].append({
 "objective": obj,
 "adsets": [
 {"name": f"{obj} Prospecting", "budget":50},
 {"name": f"{obj} Retargeting", "budget":30},
 ]
 })
 return structure
