import requests
import json
import time
from datetime import datetime

# CONFIGURATION
ACCESS_TOKEN = "EAAKA2OT1FroBQ3AEm2R1RnAZCXxZBPCZBUsRZAjp0e9StIHwu5AOFczMrWU0c32L2AB3iZA9Jk5Jt5uraMG97sTX8iDveC6zaJHXRoZBKKbzMcUZBBkMyZAkgUYCTGKSef7LJwU7EOGVuUF0GlTnu9xnrUQiSEYtq98TF9pwgipX1MbVyASGubRvzCzsj6cJR0KXORRKgU6FSzsPrXe1JmASERCGEDosIwFdEtPdUxOHFIRixZBZB8Tq9Yv97LhhyebZCeavqSA8rsWbEDClmvGubNb3qZCNIt0ZD"
AD_ACCOUNT_ID = "act_372862778840800"  # Mahir ID 1484
API_VERSION = "v19.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

def get_account_insights():
    """Fetch current insights for the account"""
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/insights"
    params = {
        "access_token": ACCESS_TOKEN,
        "date_preset": "today",
        "fields": "spend,cpm,ctr,cpc,impressions,clicks,reach,actions",
        "level": "account"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "error" in data:
            print(f"❌ API Error: {data['error']['message']}")
            return None
            
        if "data" in data and len(data["data"]) > 0:
            return data["data"][0]
        else:
            print("⚠️ No data found for today (Account might be idle today).")
            return None
            
    except Exception as e:
        print(f"❌ Connection Error: {str(e)}")
        return None

def get_active_campaigns():
    """List active campaigns"""
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/campaigns"
    params = {
        "access_token": ACCESS_TOKEN,
        "fields": "name,status,daily_budget,lifetime_budget,start_time",
        "effective_status": "['ACTIVE']"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data.get("data", [])
    except Exception as e:
        print(f"❌ Error fetching campaigns: {str(e)}")
        return []

def main():
    print(f"🚀 FACEBOOK ADS MANAGER V1 - MONITORING MODE")
    print(f"🎯 Target Account: {AD_ACCOUNT_ID}")
    print("="*50)
    
    # 1. Check Active Campaigns
    campaigns = get_active_campaigns()
    print(f"\n📋 ACTIVE CAMPAIGNS ({len(campaigns)}):")
    if campaigns:
        for camp in campaigns:
            budget = camp.get('daily_budget', camp.get('lifetime_budget', 'N/A'))
            print(f"   🔹 {camp['name']} | Status: {camp['status']} | Budget: {budget}")
    else:
        print("   ⚠️ No active campaigns found.")

    # 2. Check Today's Performance
    print(f"\n📊 TODAY'S PERFORMANCE:")
    insights = get_account_insights()
    
    if insights:
        spend = float(insights.get('spend', 0))
        cpm = float(insights.get('cpm', 0))
        ctr = float(insights.get('ctr', 0))
        clicks = int(insights.get('clicks', 0))
        
        print(f"   💸 SPEND: Rp {spend:,.2f}")
        print(f"   👀 CPM: Rp {cpm:,.2f}")
        print(f"   👆 CTR: {ctr:.2f}%")
        print(f"   🖱️ CLICKS: {clicks}")
        
        # Simple Analysis
        if cpm > 50000:
            print("\n   ⚠️ WARNING: CPM is HIGH (>50k). Consider refreshing creatives.")
        elif cpm < 15000:
            print("\n   ✅ GOOD: CPM is cheap (<15k).")
            
        if ctr < 1.0:
            print("   ⚠️ WARNING: CTR is LOW (<1%). Ad creative might be boring.")
        elif ctr > 2.0:
            print("   ✅ GOOD: CTR is healthy (>2%).")
            
    else:
        print("   (No spend data for today yet)")

if __name__ == "__main__":
    main()
