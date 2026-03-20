from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class Workspace:
 data: Dict[str, Any]

 @property
 def facebook_accounts(self):
 return self.data.get("facebook", {}).get("ad_account_ids", [])

 @property
 def shopee_config(self):
 return self.data.get("shopee", {})

 @property
 def telegram_config(self):
 return self.data.get("reporting", {})
