import time
import hmac
import hashlib
import requests
from typing import Dict

class ShopeeAffiliateConnector:
 def __init__(self, partner_id: str, partner_key: str, shop_id: str, affiliate_token: str):
 self.partner_id = partner_id
 self.partner_key = partner_key
 self.shop_id = shop_id
 self.affiliate_token = affiliate_token
 self.base_url = "https://partner.shopeemobile.com/api/v2"

 def _sign(self, path: str, params: Dict[str, str]):
 timestamp = int(time.time())
 basestring = f"{self.partner_id}{path}{timestamp}{self.partner_key}"
 signature = hmac.new(self.partner_key.encode(), basestring.encode(), hashlib.sha256).hexdigest()
 return signature, timestamp

 def _get(self, path: str, params: Dict[str, str]):
 signature, timestamp = self._sign(path, params)
 params.update({
 "partner_id": self.partner_id,
 "timestamp": timestamp,
 "sign": signature
 })
 resp = requests.get(f"{self.base_url}{path}", params=params, timeout=30)
 resp.raise_for_status()
 return resp.json()

 def get_affiliate_order(self, start_time: int, end_time: int, pagination_offset: int =0, pagination_entries_per_page: int =100):
 path = "/affiliate/v1/order/get"
 params = {
 "start_time": start_time,
 "end_time": end_time,
 "pagination_offset": pagination_offset,
 "pagination_entries_per_page": pagination_entries_per_page,
 "affiliate_token": self.affiliate_token
 }
 return self._get(path, params)
