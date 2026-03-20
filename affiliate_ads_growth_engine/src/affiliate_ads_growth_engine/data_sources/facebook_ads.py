import requests
from typing import List

class FacebookAdsConnector:
 def __init__(self, access_token: str, api_version: str = "v18.0"):
 self.access_token = access_token
 self.api_version = api_version
 self.base_url = f"https://graph.facebook.com/{api_version}"

 def _get(self, endpoint: str, params: dict):
 params = {**params, "access_token": self.access_token}
 resp = requests.get(f"{self.base_url}/{endpoint}", params=params, timeout=30)
 resp.raise_for_status()
 return resp.json()

 def get_campaigns(self, ad_account_id: str, fields: List[str] | None = None):
 fields = fields or ["id", "name", "status", "objective"]
 return self._get(f"act_{ad_account_id}/campaigns", {"fields": ",".join(fields)})

 def get_insights(self, ad_account_id: str, level: str = "ad", date_preset: str = "yesterday", fields: List[str] | None = None):
 fields = fields or ["impressions", "clicks", "spend", "ctr", "cpm", "actions"]
 params = {
 "level": level,
 "date_preset": date_preset,
 "fields": ",".join(fields)
 }
 return self._get(f"act_{ad_account_id}/insights", params)
