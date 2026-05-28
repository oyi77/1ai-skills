from __future__ import annotations

import subprocess
import urllib.request
import urllib.error
import json
import time
import os
import signal
from pathlib import Path

GROK_API_REPO = "/home/openclaw/.openclaw/workspace/projects/grok-api"


class GrokApiClient:
    DEFAULT_URL = "http://localhost:6969"
    MODELS = ["grok-3-auto", "grok-3-fast", "grok-4", "grok-4-mini-thinking-tahoe"]

    def __init__(self, server_url: str = DEFAULT_URL, proxy: str = ""):
        self.server_url = server_url.rstrip("/")
        self.proxy = proxy
        self._proc: subprocess.Popen | None = None
        self._conversation: list[dict] | None = None

    def is_alive(self) -> bool:
        try:
            req = urllib.request.Request(
                f"{self.server_url}/docs",
                method="GET",
            )
            urllib.request.urlopen(req, timeout=3)
            return True
        except Exception:
            return False

    def start_server(
        self,
        port: int = 6969,
        workers: int = 5,
        background: bool = True,
    ) -> bool:
        if self.is_alive():
            return True

        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"

        cmd = [
            "/usr/bin/python3",
            "-m",
            "uvicorn",
            "api_server:app",
            "--host",
            "0.0.0.0",
            "--port",
            str(port),
            "--workers",
            str(workers),
        ]

        try:
            if background:
                self._proc = subprocess.Popen(
                    cmd,
                    cwd=GROK_API_REPO,
                    env=env,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    preexec_fn=os.setsid,
                )
            else:
                subprocess.run(cmd, cwd=GROK_API_REPO, env=env, check=True)
                return True

            for _ in range(15):
                time.sleep(1)
                if self.is_alive():
                    return True
            return False
        except Exception:
            return False

    def stop_server(self) -> None:
        if self._proc:
            try:
                os.killpg(os.getpgid(self._proc.pid), signal.SIGTERM)
            except Exception:
                pass
            self._proc = None

    def _post(self, payload: dict) -> dict:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.server_url}/ask",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            resp = urllib.request.urlopen(req, timeout=120)
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            return {"status": "error", "error": f"HTTP {e.code}: {body}"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def ask(
        self,
        message: str,
        model: str = "grok-3-fast",
        extra_data: dict | None = None,
    ) -> dict:
        proxy = self.proxy if self.proxy.strip() else "none"
        return self._post(
            {
                "proxy": proxy,
                "message": message,
                "model": model,
                "extra_data": extra_data if extra_data is not None else {},
            }
        )

    def start_convo(self, message: str, model: str = "grok-3-fast") -> dict:
        resp = self.ask(message, model=model, extra_data=None)
        if resp.get("status") == "success" and resp.get("extra_data"):
            self._conversation = resp["extra_data"]
        return resp

    def continue_convo(
        self,
        message: str,
        extra_data: dict | None = None,
        model: str = "grok-3-fast",
    ) -> dict:
        ctx = extra_data if extra_data is not None else self._conversation
        resp = self.ask(message, model=model, extra_data=ctx)
        if resp.get("status") == "success" and resp.get("extra_data"):
            self._conversation = resp["extra_data"]
        return resp

    def chat(
        self,
        message: str,
        model: str = "grok-3-fast",
        stream: bool = False,
    ) -> dict:
        if self._conversation:
            return self.continue_convo(message, model=model)
        return self.start_convo(message, model=model)
