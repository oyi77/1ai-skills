"""Vast.ai Serverless ComfyUI provider for video generation.

Wraps vastai_sdk Serverless → routes T2V/I2V requests to a ComfyUI
instance on Vast.ai GPU workers. Supports both text-to-video and
image-to-video modes.

Usage:
    provider = VastAIProvider(endpoint_name="ozeap3mc", serverless_key="...")
    result = await provider.generate("a cat running in the rain")
    print(result.data["video_path"])  # local MP4 path

Environment variables:
    VASTAI_SERVERLESS_KEY  - Vast.ai serverless API key
    VASTAI_ENDPOINT_NAME   - Serverless endpoint name (e.g. "ozeap3mc")
"""

import asyncio
import base64
import json
import os
import random
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

from .base import AIProvider, GenerationResult, ProviderType

VASTAI_SERVERLESS_KEY_ENV = "VASTAI_SERVERLESS_KEY"
VASTAI_ENDPOINT_NAME_ENV = "VASTAI_ENDPOINT_NAME"
DEFAULT_COMFYUI_PORT = 8188
DEFAULT_POLL_INTERVAL = 5
DEFAULT_POLL_TIMEOUT = 600
COST_T2V = 500
COST_I2V = 750
COST_PER_STEP = 20


class VastAIError(Exception):
    pass


class VastAIAuthError(VastAIError):
    pass


SUPPORTED_MODELS = [
    "cogvideo-x/CogVideoX-5b-T2V",
    "cogvideo-x/CogVideoX-5b-I2V",
    "hunyuanvideo",
    "ltx-video",
]


class VastAIProvider(AIProvider):
    """Vast.ai Serverless ComfyUI provider for video generation."""

    @property
    def supported_models(self) -> list[str]:
        return SUPPORTED_MODELS

    def __init__(
        self,
        endpoint_name: Optional[str] = None,
        serverless_key: Optional[str] = None,
        comfyui_port: int = DEFAULT_COMFYUI_PORT,
        output_dir: Optional[str] = None,
        poll_interval: int = DEFAULT_POLL_INTERVAL,
        poll_timeout: int = DEFAULT_POLL_TIMEOUT,
        **kwargs,
    ):
        super().__init__(
            provider_type=ProviderType.VIDEO,
            provider_name="Vast.ai ComfyUI",
            api_key=serverless_key,
            **kwargs,
        )
        self.endpoint_name = (
            endpoint_name
            or os.environ.get(VASTAI_ENDPOINT_NAME_ENV)
            or os.environ.get("VASTAI_ENDPOINT_NAME")
        )
        self.serverless_key = (
            serverless_key
            or os.environ.get(VASTAI_SERVERLESS_KEY_ENV)
            or os.environ.get("VASTAI_SERVERLESS_KEY")
            or os.environ.get("VASTAI_API_KEY")
        )
        self.comfyui_port = comfyui_port
        self.output_dir = Path(output_dir or "/tmp/vastai_videos")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.poll_interval = poll_interval
        self.poll_timeout = poll_timeout
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from vastai_sdk import Serverless
            except ImportError:
                raise VastAIError(
                    "vastai-sdk not installed. Run: pip install vastai-sdk"
                )
            if not self.serverless_key:
                raise VastAIAuthError(
                    f"Set ${VASTAI_SERVERLESS_KEY_ENV} env var or pass "
                    f"serverless_key to VastAIProvider()."
                )
            self._client = Serverless(api_key=self.serverless_key)
        return self._client

    def _build_t2v_prompt(
        self,
        prompt: str,
        negative_prompt: str = "",
        seed: int = -1,
        steps: int = 25,
        cfg: float = 7.0,
        sampler_name: str = "euler",
        scheduler: str = "normal",
        width: int = 1024,
        height: int = 576,
        image: Optional[str] = None,
    ) -> dict:
        actual_seed = seed if seed != -1 else random.randint(0, 2**32 - 1)
        model_name = (
            "cogvideo-x/CogVideoX-5b-I2V" if image else "cogvideo-x/CogVideoX-5b-T2V"
        )
        return {
            "prompt": {
                "0": {
                    "class_type": "CheckpointLoaderSimple",
                    "inputs": {"model_name": model_name},
                },
                "1": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {"text": prompt, "clip": ["0", 1]},
                },
                "2": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {
                        "text": negative_prompt
                        or "blurry, low quality, distorted, watermark",
                        "clip": ["0", 1],
                    },
                },
                "3": {
                    "class_type": "EmptyLatentVideo",
                    "inputs": {
                        "width": width,
                        "height": height,
                        "frames": steps * 4,
                        "batch_size": 1,
                    },
                },
                "4": {
                    "class_type": "KSampler",
                    "inputs": {
                        "model": ["0", 0],
                        "seed": actual_seed,
                        "steps": steps,
                        "cfg": cfg,
                        "sampler_name": sampler_name,
                        "scheduler": scheduler,
                        "positive": ["1", 0],
                        "negative": ["2", 0],
                        "latent_image": ["3", 0],
                    },
                },
                "5": {
                    "class_type": "VAEDecode",
                    "inputs": {"samples": ["4", 0], "vae": ["0", 2]},
                },
            },
            "seed": actual_seed,
        }

    def _http_post(
        self, url: str, payload: dict, headers: Optional[dict] = None
    ) -> dict:
        h = dict(headers or {})
        h["Content-Type"] = "application/json"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=h, method="POST")
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, context=ctx, timeout=120) as r:
            return json.loads(r.read())

    def _http_get(self, url: str, headers: Optional[dict] = None) -> dict:
        req = urllib.request.Request(url, headers=headers or {}, method="GET")
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            return json.loads(r.read())

    def _download_file(self, url: str, path: Path) -> Path:
        req = urllib.request.Request(url, headers={}, method="GET")
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, context=ctx, timeout=300) as r:
            path.write_bytes(r.read())
        return path

    def _execute_via_vast_serverless(self, comfyui_payload: dict, cost: int):
        client = self._get_client()
        if not self.endpoint_name:
            raise VastAIAuthError(
                "Set VASTAI_ENDPOINT_NAME env var or pass endpoint_name to VastAIProvider()."
            )
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        endpoint = loop.run_until_complete(client.get_endpoint(name=self.endpoint_name))
        result = loop.run_until_complete(
            endpoint.request(
                "/prompt",
                comfyui_payload,
                cost=cost,
                timeout=float(self.poll_timeout),
                retry=True,
            )
        )
        if isinstance(result, dict):
            return "serverless", result.get("prompt_id", "")
        try:
            parsed = json.loads(str(result))
            return "serverless", parsed.get("prompt_id", "")
        except Exception:
            return "serverless", str(result)

    async def _poll_comfyui_history(self, worker_url: str, prompt_id: str) -> dict:
        deadline = time.time() + self.poll_timeout
        while time.time() < deadline:
            if worker_url == "serverless":
                url = f"http://localhost:{self.comfyui_port}/history/{prompt_id}"
            else:
                url = f"{worker_url}/history/{prompt_id}"
            try:
                history = self._http_get(url)
                if prompt_id in history:
                    return history[prompt_id]
            except Exception:
                pass
            await asyncio.sleep(self.poll_interval)
        raise TimeoutError(
            f"Polling timed out after {self.poll_timeout}s for prompt {prompt_id}"
        )

    def _extract_video_from_history(self, history_output: dict) -> Optional[dict]:
        for node_output in history_output.values():
            if not isinstance(node_output, dict):
                continue
            if "images" in node_output:
                return {"image_paths": node_output["images"]}
            if "gifs" in node_output or "videos" in node_output:
                return {
                    "video_path": node_output.get("gifs") or node_output.get("videos"),
                    "images": node_output.get("images", []),
                }
            for key in ["executed", "output", "result"]:
                if key in node_output:
                    sub = node_output[key]
                    if isinstance(sub, dict):
                        if "images" in sub:
                            return {"image_paths": sub["images"]}
                        if "videos" in sub or "gifs" in sub:
                            return {
                                "video_path": sub.get("videos") or sub.get("gifs"),
                                "images": sub.get("images", []),
                            }
        return None

    async def generate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> GenerationResult:
        if not self.validate_api_key() and not self.serverless_key:
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=model or "default",
                metadata={"error": f"Set ${VASTAI_SERVERLESS_KEY_ENV} env var."},
            )
        negative_prompt = kwargs.get("negative_prompt", "")
        seed = kwargs.get("seed", -1)
        steps = kwargs.get("steps", 25)
        cfg = kwargs.get("cfg", 7.0)
        sampler_name = kwargs.get("sampler_name", "euler")
        scheduler = kwargs.get("scheduler", "normal")
        width = kwargs.get("width", 1024)
        height = kwargs.get("height", 576)
        image = kwargs.get("image")
        poll_timeout = kwargs.get("poll_timeout", self.poll_timeout)
        is_i2v = image is not None
        cost = (COST_I2V if is_i2v else COST_T2V) + steps * COST_PER_STEP

        try:
            comfyui_payload = self._build_t2v_prompt(
                prompt=prompt,
                negative_prompt=negative_prompt,
                seed=seed,
                steps=steps,
                cfg=cfg,
                sampler_name=sampler_name,
                scheduler=scheduler,
                width=width,
                height=height,
                image=image,
            )
            worker_url, prompt_id = self._execute_via_vast_serverless(
                comfyui_payload, cost=cost
            )
            history = await self._poll_comfyui_history(worker_url, prompt_id)
            output = self._extract_video_from_history(history)
            if not output:
                return GenerationResult(
                    success=False,
                    provider=self.provider_name,
                    model=model or "default",
                    metadata={
                        "error": "No video output found in ComfyUI history",
                        "history_keys": list(history.keys()),
                        "prompt_id": prompt_id,
                    },
                )
            ts_path = self.output_dir / f"vastai_video_{int(time.time())}.mp4"
            if worker_url != "serverless":
                video_filename = output.get("video_path")
                if video_filename:
                    self._download_file(
                        f"{worker_url}/view?filename={video_filename}", ts_path
                    )
            else:
                video_path = output.get("video_path")
                if isinstance(video_path, list):
                    video_path = video_path[0]
                if video_path:
                    if video_path.startswith("http"):
                        self._download_file(video_path, ts_path)
                    else:
                        try:
                            ts_path.write_bytes(base64.b64decode(video_path))
                        except Exception:
                            return GenerationResult(
                                success=False,
                                provider=self.provider_name,
                                model=model or "default",
                                metadata={
                                    "error": "Failed to decode video",
                                    "output": str(output)[:500],
                                },
                            )
            if not ts_path.exists() or ts_path.stat().st_size == 0:
                return GenerationResult(
                    success=False,
                    provider=self.provider_name,
                    model=model or "default",
                    metadata={
                        "error": "Video file not found after download",
                        "output": str(output)[:500],
                    },
                )
            return GenerationResult(
                success=True,
                data={
                    "video_path": str(ts_path),
                    "prompt_id": prompt_id,
                    "seed": comfyui_payload.get("seed", seed),
                    "steps": steps,
                    "mode": "i2v" if is_i2v else "t2v",
                },
                cost=cost / 1000.0,
                provider=self.provider_name,
                model=model or "default",
                metadata={
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "width": width,
                    "height": height,
                    "i2v": is_i2v,
                },
            )
        except VastAIAuthError as e:
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=model or "default",
                metadata={"error": f"Auth error: {e}"},
            )
        except TimeoutError as e:
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=model or "default",
                metadata={"error": f"Timeout: {e}"},
            )
        except Exception as e:
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=model or "default",
                metadata={"error": str(e)},
            )

    async def is_available(self) -> bool:
        try:
            client = self._get_client()
            loop = asyncio.get_event_loop()
        except Exception:
            return False
        try:
            endpoint = loop.run_until_complete(
                client.get_endpoint(name=self.endpoint_name or "")
            )
            workers = loop.run_until_complete(endpoint.get_workers())
            return isinstance(workers, list)
        except Exception:
            return False

    def get_cost_estimate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> float:
        steps = kwargs.get("steps", 25)
        is_i2v = kwargs.get("image") is not None
        cost = (COST_I2V if is_i2v else COST_T2V) + steps * COST_PER_STEP
        return round(cost / 1000.0, 4)


__all__ = ["VastAIProvider", "VastAIError", "VastAIAuthError"]
