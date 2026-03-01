import requests
import json

TOKEN = "EAAKA2OT1FroBQ3AEm2R1RnAZCXxZBPCZBUsRZAjp0e9StIHwu5AOFczMrWU0c32L2AB3iZA9Jk5Jt5uraMG97sTX8iDveC6zaJHXRoZBKKbzMcUZBBkMyZAkgUYCTGKSef7LJwU7EOGVuUF0GlTnu9xnrUQiSEYtq98TF9pwgipX1MbVyASGubRvzCzsj6cJR0KXORRKgU6FSzsPrXe1JmASERCGEDosIwFdEtPdUxOHFIRixZBZB8Tq9Yv97LhhyebZCeavqSA8rsWbEDClmvGubNb3qZCNIt0ZD"

def check_token():
    url = f"https://graph.facebook.com/v19.0/me?fields=id,name,adaccounts{{name,account_id,currency,account_status,balance}}&access_token={TOKEN}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if "error" in data:
            print(f"❌ ERROR: {data['error']['message']}")
            return
            
        print(f"✅ TOKEN VALID!")
        print(f"👤 User: {data.get('name', 'Unknown')}")
        print(f"🆔 User ID: {data.get('id', 'Unknown')}")
        
        if "adaccounts" in data and "data" in data["adaccounts"]:
            print(f"\n📂 DAFTAR AD ACCOUNTS ({len(data['adaccounts']['data'])} found):")
            for acc in data["adaccounts"]["data"]:
                status_map = {1: "ACTIVE", 2: "DISABLED", 3: "UNSETTLED", 7: "PENDING_RISK_REVIEW", 8: "IN_GRACE_PERIOD", 9: "PENDING_CLOSURE", 100: "CLOSED", 101: "ANY_ACTIVE", 102: "ANY_CLOSED"}
                status = status_map.get(acc.get('account_status'), f"UNKNOWN({acc.get('account_status')})")
                
                print(f"- Name: {acc.get('name')}")
                print(f"  ID: act_{acc.get('account_id')}")
                print(f"  Currency: {acc.get('currency')}")
                print(f"  Status: {status}")
                print(f"  Balance: {acc.get('balance', 0)}")
                print("-" * 30)
        else:
            print("\n⚠️ TIDAK ADA AD ACCOUNT YANG TERHUBUNG.")
            
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {str(e)}")

if __name__ == "__main__":
    check_token()
