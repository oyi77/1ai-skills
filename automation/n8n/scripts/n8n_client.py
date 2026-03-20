#!/usr/bin/env python3
"""n8n Workflow Orchestration Client"""
import json, os, sys
import urllib.request, urllib.parse

N8N_BASE = os.environ.get("N8N_BASE_URL", "http://localhost:5678")
N8N_KEY = os.environ.get("N8N_API_KEY", "")

def api(method, path, data=None):
    url = f"{N8N_BASE}/api/v1{path}"
    headers = {"Content-Type": "application/json"}
    if N8N_KEY:
        headers["X-N8N-API-KEY"] = N8N_KEY
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}

def list_workflows(): return api("GET", "/workflows")
def get_workflow(wf_id): return api("GET", f"/workflows/{wf_id}")
def trigger_workflow(wf_id, data=None): return api("POST", f"/workflows/{wf_id}/execute", {"data": data or {}})
def get_executions(wf_id, limit=10): return api("GET", f"/executions?workflowId={wf_id}&limit={limit}")

def trigger_webhook(path, data=None):
    """Trigger n8n webhook endpoint"""
    url = f"{N8N_BASE}/webhook{path}"
    body = json.dumps(data or {}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--action", choices=["list","trigger","executions","webhook"], required=True)
    p.add_argument("--workflow-id")
    p.add_argument("--webhook-path")
    p.add_argument("--data", default="{}")
    args = p.parse_args()
    data = json.loads(args.data)
    
    if args.action == "list": print(json.dumps(list_workflows(), indent=2))
    elif args.action == "trigger": print(json.dumps(trigger_workflow(args.workflow_id, data), indent=2))
    elif args.action == "executions": print(json.dumps(get_executions(args.workflow_id), indent=2))
    elif args.action == "webhook": print(json.dumps(trigger_webhook(args.webhook_path, data), indent=2))
