#!/usr/bin/env python3
"""
General Financial Research Agent
Supports: stocks, forex (XAUUSD/DXY), crypto (BTC/ETH), Polymarket events
"""
import json, sys, os
from datetime import datetime
from pathlib import Path

try:
    import yfinance as yf
    YF_AVAILABLE = True
except ImportError:
    YF_AVAILABLE = False

try:
    from openai import OpenAI
    client = OpenAI(base_url="http://localhost:20128/v1", api_key="omniroute")
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False

ASSET_MAP = {
    "gold": "GC=F", "xauusd": "GC=F", "xau": "GC=F",
    "dxy": "DX-Y.NYB", "usd": "DX-Y.NYB",
    "btc": "BTC-USD", "bitcoin": "BTC-USD",
    "eth": "ETH-USD", "ethereum": "ETH-USD",
    "sp500": "^GSPC", "nasdaq": "^IXIC",
}

def detect_asset(query):
    q = query.lower()
    for key, ticker in ASSET_MAP.items():
        if key in q:
            return ticker, key
    # Try as direct ticker
    words = q.split()
    for w in words:
        if w.isupper() and 2 <= len(w) <= 6:
            return w, w.lower()
    return None, None

def get_price_data(ticker, period="5d"):
    if not YF_AVAILABLE:
        return {"error": "yfinance not installed. Run: pip install yfinance --break-system-packages"}
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period=period)
        if hist.empty:
            return {"error": f"No data for {ticker}"}
        latest = hist.iloc[-1]
        prev = hist.iloc[-2] if len(hist) > 1 else latest
        return {
            "ticker": ticker,
            "price": round(latest["Close"], 4),
            "change": round(latest["Close"] - prev["Close"], 4),
            "change_pct": round((latest["Close"] - prev["Close"]) / prev["Close"] * 100, 2),
            "high": round(latest["High"], 4),
            "low": round(latest["Low"], 4),
            "volume": int(latest["Volume"]),
            "period_high": round(hist["High"].max(), 4),
            "period_low": round(hist["Low"].min(), 4),
        }
    except Exception as e:
        return {"error": str(e)}

def search_news(query, limit=5):
    try:
        result = __import__("subprocess").run(
            ["python3", "-c", f"from duckduckgo_search import DDGS; [print(r['title'],'|',r['href']) for r in DDGS().news('{query}', max_results={limit})]"],
            capture_output=True, text=True, timeout=15
        )
        return result.stdout.strip().split("\n") if result.returncode == 0 else []
    except:
        return []

def analyze(question, price_data, news):
    if not LLM_AVAILABLE:
        return "LLM not available"
    news_str = "\n".join(news[:5]) if news else "No recent news found"
    price_str = json.dumps(price_data, indent=2) if "error" not in price_data else str(price_data)
    prompt = f"""You are a financial analyst. Answer this question: "{question}"

Price Data:
{price_str}

Recent News:
{news_str}

Provide: 1) Current situation 2) Key factors 3) Short-term outlook 4) Risk factors
Be concise and data-driven."""
    try:
        r = client.chat.completions.create(
            model="auto/pro-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"Analysis failed: {e}"

def research(question):
    ticker, asset_name = detect_asset(question)
    price_data = get_price_data(ticker) if ticker else {"info": "No specific asset detected"}
    news = search_news(f"{asset_name or question} price analysis", limit=5)
    analysis = analyze(question, price_data, news)
    
    result = {
        "question": question,
        "asset": ticker,
        "timestamp": datetime.now().isoformat(),
        "price_data": price_data,
        "news_headlines": news,
        "analysis": analysis
    }
    
    # Save log
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    date = datetime.now().strftime("%Y-%m-%d")
    asset_slug = (asset_name or "general").replace("/", "_")
    log_file = log_dir / f"{date}-{asset_slug}.json"
    log_file.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    
    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Financial Research Agent")
    parser.add_argument("question", nargs="?", default="What is the current state of gold (XAUUSD)?")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    
    result = research(args.question)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n📊 Research: {result['question']}")
        if result.get('price_data') and 'price' in result['price_data']:
            d = result['price_data']
            print(f"💰 {result['asset']}: {d['price']} ({'+' if d['change_pct'] >= 0 else ''}{d['change_pct']}%)")
        print(f"\n🔍 Analysis:\n{result['analysis']}")
