from dataclasses import dataclass
from typing import Optional

@dataclass
class CompetitorInput:
 ads_library_url: Optional[str] = None
 screenshot_path: Optional[str] = None
 ad_text: Optional[str] = None

@dataclass
class CompetitorAnalysis:
 hook: str
 creative_style: str
 audience: str
 strategy: str
 campaign_structure: str

class CompetitorAnalyzer:
 def analyze(self, data: CompetitorInput) -> CompetitorAnalysis:
 hook = self._extract_hook(data)
 style = self._detect_style(data)
 audience = self._infer_audience(data)
 strategy = self._summarize_strategy(data)
 structure = self._guess_campaign_structure(data)
 return CompetitorAnalysis(hook, style, audience, strategy, structure)

 def _extract_hook(self, data: CompetitorInput) -> str:
 text = data.ad_text or ""
 return text.split("\n")[0][:120] if text else "Unknown hook"

 def _detect_style(self, data: CompetitorInput) -> str:
 text = data.ad_text or ""
 if "testimoni" in text.lower():
 return "testimonial"
 if "sebelum" in text.lower() or "before" in text.lower():
 return "before_after"
 if "masalah" in text.lower():
 return "problem_solution"
 return "lifestyle" if "hari" in text.lower() else "generic"

 def _infer_audience(self, data: CompetitorInput) -> str:
 text = data.ad_text or ""
 if "ibu" in text.lower():
 return "Parents"
 if "bisnis" in text.lower():
 return "SMB owners"
 return "General"

 def _summarize_strategy(self, data: CompetitorInput) -> str:
 return "Positioning + offer + urgency"

 def _guess_campaign_structure(self, data: CompetitorInput) -> str:
 return "Probably TOF/MOF/BOF with CBO"
