import urllib.request
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('POST_BRIDGE_API_KEY')
BASE_URL = os.environ.get('POST_BRIDGE_BASE_URL', 'https://api.post-bridge.com/v1')

print(f"DEBUG: Using API_KEY={API_KEY[:5]}...{API_KEY[-5:]}")
print(f"DEBUG: Using BASE_URL={BASE_URL}")

def get_connected_accounts():
    url = f"{BASE_URL}/social-accounts?limit=100&offset=0"
    req = urllib.request.Request(url)
    req.add_header('Authorization', f"Bearer {API_KEY}")
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode('utf-8')
            print(f"DEBUG: Response body: {body}")
            data = json.loads(body)
            return data
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode()}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

result = get_connected_accounts()
if result:
    print(json.dumps(result, indent=2))
