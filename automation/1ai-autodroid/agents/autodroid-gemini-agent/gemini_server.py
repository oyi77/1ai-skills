#!/usr/bin/env python3
"""
FastAPI wrapper for Gemini Agent
Unified HTTP endpoints for all Gemini commands
Port: 8765
"""

import json
import sys
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="AutoDroid Gemini Agent", version="1.0")

# Get script path
SCRIPT_PATH = __file__.replace("gemini_server.py", "scripts/gemini_agent.py")

class ChatRequest(BaseModel):
    prompt: str
    timeout: int = 30
    device: Optional[str] = None

class ImagineRequest(BaseModel):
    prompt: str
    timeout: int = 60
    device: Optional[str] = None

class StatusRequest(BaseModel):
    device: Optional[str] = None

@app.get("/")
async def root():
    return {"status": "AutoDroid Gemini Agent running on port 8765"}

@app.get("/health")
async def health():
    return {"ok": True, "service": "gemini"}

@app.post("/api/gemini/status")
async def status(req: StatusRequest):
    """Check Gemini installation and device info"""
    cmd = [sys.executable, SCRIPT_PATH, "status"]
    if req.device:
        cmd.extend(["--device", req.device])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {result.stderr}")

@app.post("/api/gemini/chat")
async def chat(req: ChatRequest):
    """Send chat prompt to Gemini"""
    cmd = [sys.executable, SCRIPT_PATH, "chat", "--prompt", req.prompt, "--timeout", str(req.timeout)]
    if req.device:
        cmd.extend(["--device", req.device])
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=req.timeout + 10)
    try:
        return json.loads(result.stdout)
    except:
        raise HTTPException(status_code=500, detail=f"Chat failed: {result.stderr}")

@app.post("/api/gemini/imagine")
async def imagine(req: ImagineRequest):
    """Generate image with Gemini"""
    cmd = [sys.executable, SCRIPT_PATH, "imagine", "--prompt", req.prompt, "--timeout", str(req.timeout)]
    if req.device:
        cmd.extend(["--device", req.device])
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=req.timeout + 10)
    try:
        return json.loads(result.stdout)
    except:
        raise HTTPException(status_code=500, detail=f"Imagine failed: {result.stderr}")

@app.post("/api/gemini/screenshot")
async def screenshot(req: StatusRequest):
    """Take device screenshot"""
    cmd = [sys.executable, SCRIPT_PATH, "screenshot"]
    if req.device:
        cmd.extend(["--device", req.device])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except:
        raise HTTPException(status_code=500, detail=f"Screenshot failed: {result.stderr}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8765, log_level="info")
