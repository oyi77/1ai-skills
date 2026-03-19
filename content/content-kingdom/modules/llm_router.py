"""
LLM Router — routes text generation requests to available providers.
Priority: Grok-Api (free) → OpenAI (if key) → Anthropic (if key)
"""

from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Optional

try:
    import openai

    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    import anthropic

    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


class LLMRouter:
    PROVIDERS = ["grok", "openai", "anthropic"]

    def __init__(self, config: dict | None = None):
        self.config = config or {}

        grok_cfg = self.config.get("grok_api", {})
        self.grok_url = grok_cfg.get("server_url", "http://localhost:6969")
        self.grok_proxy = grok_cfg.get("proxy", "")
        self.default_model = grok_cfg.get("default_model", "grok-3-fast")

        self.grok_client = None
        self.openai_client = None
        self.anthropic_client = None

        self._init_openai()
        self._init_anthropic()

    def _init_openai(self) -> None:
        if not HAS_OPENAI:
            return
        key = os.environ.get("OPENAI_API_KEY") or self.config.get("openai_api_key")
        if key:
            self.openai_client = openai.OpenAI(api_key=key)

    def _init_anthropic(self) -> None:
        if not HAS_ANTHROPIC:
            return
        key = os.environ.get("ANTHROPIC_API_KEY") or self.config.get(
            "anthropic_api_key"
        )
        if key:
            self.anthropic_client = anthropic.Anthropic(api_key=key)

    def _get_grok_client(self):
        if self.grok_client is None:
            from .grok_api_client import GrokApiClient

            self.grok_client = GrokApiClient(
                server_url=self.grok_url,
                proxy=self.grok_proxy,
            )
        return self.grok_client

    def generate(
        self,
        message: str,
        provider: str = "grok",
        model: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        conversation: list[dict] | None = None,
    ) -> dict:
        if provider == "grok" or provider not in self.PROVIDERS:
            return self._generate_grok(message, model, conversation)
        elif provider == "openai":
            return self._generate_openai(message, model, max_tokens, temperature)
        elif provider == "anthropic":
            return self._generate_anthropic(message, model, max_tokens, temperature)
        return {"error": f"Unknown provider: {provider}"}

    def _generate_grok(
        self,
        message: str,
        model: str | None = None,
        conversation: list[dict] | None = None,
    ) -> dict:
        try:
            client = self._get_grok_client()
            model = model or self.default_model

            if not client.is_alive():
                if not client.start_server():
                    return {
                        "error": "Grok-Api server not available and auto-start failed"
                    }

            if conversation:
                extra_data = (
                    conversation[-1].get("extra_data") if conversation else None
                )
                resp = client.continue_convo(
                    message, extra_data=extra_data, model=model
                )
            else:
                resp = client.start_convo(message, model=model)

            if resp.get("status") == "success":
                return {
                    "text": resp.get("response", ""),
                    "provider": "grok",
                    "model": model,
                    "usage": {},
                    "extra_data": resp.get("extra_data"),
                }
            return {"error": resp.get("error", "Unknown error"), "provider": "grok"}

        except Exception as e:
            return {"error": str(e), "provider": "grok"}

    def _generate_openai(
        self,
        message: str,
        model: str | None,
        max_tokens: int,
        temperature: float,
    ) -> dict:
        if not self.openai_client:
            return {"error": "OpenAI not configured (no API key)"}
        try:
            model = model or "gpt-4o"
            resp = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return {
                "text": resp.choices[0].message.content,
                "provider": "openai",
                "model": model,
                "usage": dict(resp.usage),
            }
        except Exception as e:
            return {"error": str(e), "provider": "openai"}

    def _generate_anthropic(
        self,
        message: str,
        model: str | None,
        max_tokens: int,
        temperature: float,
    ) -> dict:
        if not self.anthropic_client:
            return {"error": "Anthropic not configured (no API key)"}
        try:
            model = model or "claude-sonnet-4-20250514"
            resp = self.anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": message}],
            )
            return {
                "text": resp.content[0].text,
                "provider": "anthropic",
                "model": model,
                "usage": {
                    "input_tokens": resp.usage.input_tokens,
                    "output_tokens": resp.usage.output_tokens,
                },
            }
        except Exception as e:
            return {"error": str(e), "provider": "anthropic"}

    def generate_script(
        self,
        topic: str,
        style: str = "motivational",
        duration: int = 60,
        provider: str = "grok",
    ) -> str:
        prompt = (
            f"Write a {duration}-second video script for social media. "
            f"Topic: {topic}. Style: {style}. "
            f"Format: HOOK (first 3 seconds) + BODY (main content) + CTA (call to action). "
            f"Voice: conversational, engaging, Indonesian audience. "
            f"Include visual scene descriptions in brackets."
        )
        result = self.generate(prompt, provider=provider)
        return result.get("text", result.get("error", ""))

    def generate_video_prompts(
        self,
        script: str,
        num_scenes: int = 4,
        provider: str = "grok",
    ) -> list[dict]:
        prompt = (
            f"Break down this video script into {num_scenes} distinct visual scenes. "
            f"For each scene, provide a GeminiGen video prompt (50-100 words) "
            f"describing the visual scene for AI video generation. "
            f"Script:\n{script}\n\n"
            f'Return as JSON array: [{{"scene": 1, "prompt": "..."}}, ...]'
        )
        result = self.generate(prompt, provider=provider)
        text = result.get("text", "")
        try:
            import re

            match = re.search(r"\[.*\]", text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except Exception:
            pass
        return []
