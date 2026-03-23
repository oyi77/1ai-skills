#!/usr/bin/env python3
"""Paperclip Manager CLI - Manage BerkahKarya AI agents."""
import requests, json, sys

BASE = "http://localhost:3100/api"
TOKEN = "pcp_0a284b0dd33364992dcbec9f46995cfaffc72fdedcf2621f"
COMPANY = "33e1e20e-d9f2-45f2-b907-0579ab795942"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def get(path): return requests.get(f"{BASE}{path}", headers=HEADERS).json()
def patch(path, data): return requests.patch(f"{BASE}{path}", headers=HEADERS, json=data).json()

def agents():
    data = get(f"/companies/{COMPANY}/agents")
    agents = data if isinstance(data, list) else data.get("data", [])
    for a in agents:
        print(f"  {a['name']:20} | {a.get('status','?'):10} | {a.get('id','?')[:8]}")

def issues(status=None):
    url = f"/companies/{COMPANY}/issues"
    if status: url += f"?status={status}"
    data = get(url)
    issues = data if isinstance(data, list) else data.get("data", [])
    for i in issues:
        assignee = i.get("assignee", {})
        aname = assignee.get("name", "unassigned") if assignee else "unassigned"
        print(f"  {i.get('identifier','?'):8} | {i.get('status','?'):12} | {aname:15} | {i.get('title','?')[:40]}")

def unblock(issue_id):
    result = patch(f"/companies/{COMPANY}/issues/{issue_id}", {"status": "todo"})
    print(f"Set to todo: {json.dumps(result)[:100]}")

def assign(issue_id, agent_id):
    result = patch(f"/companies/{COMPANY}/issues/{issue_id}", {"assigneeId": agent_id})
    print(f"Assigned: {json.dumps(result)[:100]}")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "agents": agents()
    elif cmd == "issues": issues(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "unblock": unblock(sys.argv[2])
    elif cmd == "assign": assign(sys.argv[2], sys.argv[3])
    else: print("Usage: pclip.py [agents|issues|unblock <id>|assign <id> <agent_id>]")
