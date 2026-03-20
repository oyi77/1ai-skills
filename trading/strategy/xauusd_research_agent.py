#!/usr/bin/env python3
"""
XAUUSD Research Agent (Dexter-inspired)

Autonomous research agent for XAUUSD gold trading analysis.
Decomposes questions, gathers market data, analyzes via LLM, and outputs structured reports.

Usage:
    python xauusd_research_agent.py "Is XAUUSD likely to break 2400 this week?"
    python xauusd_research_agent.py --question "What are key support levels?" --depth deep
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

OMNIROUTE_BASE = "http://localhost:20128/v1"
OMNIROUTE_KEY = "omniroute"
OMNIROUTE_MODEL = "auto/pro-chat"
LOG_DIR = Path(__file__).parent / "research_logs"


def get_llm_client():
    """Get OpenAI-compatible client via OmniRoute."""
    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: openai not installed. Run: pip install openai")
        sys.exit(1)
    return OpenAI(base_url=OMNIROUTE_BASE, api_key=OMNIROUTE_KEY)


def llm_chat(client, system_prompt, user_prompt, temperature=0.3):
    """Send a chat completion request via OmniRoute."""
    try:
        resp = client.chat.completions.create(
            model=OMNIROUTE_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"[LLM Error: {e}]"


def fetch_market_data():
    """Fetch XAUUSD, DXY, and related market data via yfinance."""
    try:
        import yfinance as yf
    except ImportError:
        print("ERROR: yfinance not installed. Run: pip install yfinance")
        sys.exit(1)

    symbols = {
        "XAUUSD": "GC=F",
        "DXY": "DX-Y.NYB",
        "EURUSD": "EURUSD=X",
        "USDJPY": "USDJPY=X",
        "US10Y": "^TNX",
        "SPX": "^GSPC",
    }

    data = {}
    end = datetime.now()
    start_short = end - timedelta(days=30)
    start_long = end - timedelta(days=90)

    for name, ticker in symbols.items():
        try:
            t = yf.Ticker(ticker)
            hist_short = t.history(start=start_short, end=end)
            hist_long = t.history(start=start_long, end=end)

            if hist_short.empty:
                data[name] = {"error": "No data available"}
                continue

            latest = hist_short.iloc[-1]
            data[name] = {
                "current_price": round(float(latest["Close"]), 4),
                "30d_high": round(float(hist_short["High"].max()), 4),
                "30d_low": round(float(hist_short["Low"].min()), 4),
                "30d_change_pct": round(float((latest["Close"] - hist_short.iloc[0]["Close"]) / hist_short.iloc[0]["Close"] * 100), 2),
                "90d_high": round(float(hist_long["High"].max()), 4),
                "90d_low": round(float(hist_long["Low"].min()), 4),
                "5d_avg_volume": round(float(hist_short["Volume"].tail(5).mean()), 0) if "Volume" in hist_short else 0,
            }
        except Exception as e:
            data[name] = {"error": str(e)}

    return data


def decompose_question(client, question):
    """Break down the research question into sub-questions."""
    system = "You are a gold trading research analyst. Decompose the user's question into 3-5 specific sub-questions that need to be answered. Return as a JSON array of strings."
    raw = llm_chat(client, system, question)
    try:
        # Try to parse JSON from the response
        start = raw.find("[")
        end = raw.rfind("]") + 1
        if start >= 0 and end > start:
            return json.loads(raw[start:end])
    except (json.JSONDecodeError, ValueError):
        pass
    return [question]


def analyze_data(client, question, sub_questions, market_data):
    """Analyze market data in context of the research question."""
    system = """You are an expert XAUUSD (Gold/USD) analyst. Analyze the provided market data
to answer the research question. Be specific with price levels, percentages, and timeframes.
Consider correlations between gold, DXY, yields, and equities."""

    prompt = f"""Research Question: {question}

Sub-questions to address:
{json.dumps(sub_questions, indent=2)}

Current Market Data:
{json.dumps(market_data, indent=2)}

Provide a thorough analysis addressing each sub-question with data-backed reasoning."""

    return llm_chat(client, system, prompt, temperature=0.2)


def validate_analysis(client, question, analysis):
    """Cross-check and validate the analysis for logical consistency."""
    system = """You are a senior trading risk manager. Review the analysis below for:
1. Logical consistency
2. Data accuracy (flag any suspicious claims)
3. Missing considerations
4. Risk factors not addressed
Return a brief validation note and confidence score (0-100)."""

    prompt = f"Question: {question}\n\nAnalysis:\n{analysis}"
    return llm_chat(client, system, prompt, temperature=0.1)


def generate_summary(client, question, analysis, validation, market_data):
    """Generate final structured summary in markdown."""
    system = """You are a gold trading research analyst. Generate a clean, structured markdown report.
Include: Executive Summary, Key Findings, Price Levels, Risk Factors, and Actionable Insights.
Be concise but thorough. Use tables where appropriate."""

    prompt = f"""Research Question: {question}

Analysis:
{analysis}

Validation Notes:
{validation}

Raw Market Data:
{json.dumps(market_data, indent=2)}

Generate the final research report in markdown format."""

    return llm_chat(client, system, prompt, temperature=0.2)


def log_research(question, result):
    """Log research output to JSONL."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "summary_length": len(result.get("summary", "")),
        "data_symbols": list(result.get("market_data", {}).keys()),
        "sub_questions_count": len(result.get("sub_questions", [])),
    }
    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")


def run_research(question, depth="standard"):
    """Main research pipeline: decompose -> gather -> analyze -> validate -> output."""
    print(f"[XAUUSD Research Agent] Starting research...")
    print(f"  Question: {question}")
    print(f"  Depth: {depth}")
    print()

    client = get_llm_client()

    # Step 1: Decompose
    print("[1/5] Decomposing question...")
    sub_questions = decompose_question(client, question)
    print(f"  Sub-questions: {len(sub_questions)}")

    # Step 2: Gather data
    print("[2/5] Fetching market data...")
    market_data = fetch_market_data()
    for name, info in market_data.items():
        if "current_price" in info:
            print(f"  {name}: {info['current_price']} (30d: {info['30d_change_pct']}%)")
        else:
            print(f"  {name}: {info.get('error', 'N/A')}")

    # Step 3: Analyze
    print("[3/5] Analyzing data...")
    analysis = analyze_data(client, question, sub_questions, market_data)

    # Step 4: Validate
    print("[4/5] Validating analysis...")
    validation = validate_analysis(client, question, analysis)

    # Step 5: Generate summary
    print("[5/5] Generating report...")
    summary = generate_summary(client, question, analysis, validation, market_data)

    result = {
        "question": question,
        "timestamp": datetime.now().isoformat(),
        "sub_questions": sub_questions,
        "market_data": market_data,
        "analysis": analysis,
        "validation": validation,
        "summary": summary,
    }

    # Log
    log_research(question, result)

    print()
    print("=" * 60)
    print(summary)
    print("=" * 60)

    return result


def main():
    parser = argparse.ArgumentParser(description="XAUUSD Research Agent")
    parser.add_argument("question", nargs="?", help="Research question")
    parser.add_argument("--question", "-q", dest="question_flag", help="Research question (alternative)")
    parser.add_argument("--depth", choices=["quick", "standard", "deep"], default="standard")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of markdown")

    args = parser.parse_args()
    question = args.question or args.question_flag

    if not question:
        print("ERROR: Provide a research question.")
        print('Usage: python xauusd_research_agent.py "Your question here"')
        sys.exit(1)

    result = run_research(question, args.depth)

    if args.json:
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
