import requests

class HTTPClient:
 def get(self, url, params=None, headers=None):
 resp = requests.get(url, params=params, headers=headers, timeout=30)
 resp.raise_for_status()
 return resp.json()
