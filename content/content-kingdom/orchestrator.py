#!/usr/bin/env python3
"""
Content Kingdom Orchestrator — The BRAIN.

Thin coordinator. Phases delegate to EXISTING scripts — it does NOT recreate them.

Existing modules used (via subprocess or sys.path import):
  autopilot_affiliate_engine/research_agent.py     → Phase 1: RESEARCH
  autopilot_affiliate_engine/daily_workflow.py     → Phase 2: PLAN (reuse workflow)
  content/content-generator/scripts/storyboard.py  → Phase 3: SCRIPT (imported)
  skills/nano-banana-pro/scripts/generate_image.py → Phase 4: CREATE (subprocess)
  content/content-generator/scripts/quality_gate.py→ Phase 5: REVIEW (imported)
  autopilot_affiliate_engine/auto_postbridge_robust_v2.py → Phase 6+7: SCHEDULE+POST
  modules/comment_manager.py                       → Phase 8: ENGAGE (new)
  autopilot_affiliate_engine/evening_report.py     → Phase 9: ANALYZE (subprocess)
  autopilot_affiliate_engine/revenue_tracker.py    → Phase 10: OPTIMIZE (subprocess)
  skills/auto-clipper/scripts/auto_clipper.py      → Phase 11: REPURPOSE (subprocess)
  modules/engagement_engine.py                     → Phase 12: SCALE (new)

SOLID principles:
  S — Each phase is one responsibility, delegated to one module/script
  O — New phases: add to PHASE_REGISTRY, no orchestrator edits needed
  L — All modules implement BaseModule; orchestrator treats them uniformly
  I — run_phase() / run_daily_pipeline() / get_status() — narrow public API
  D — Orchestrator depends on BaseModule abstraction, not concrete classes

Usage:
  python3 orchestrator.py --phase research
  python3 orchestrator.py --pipeline
  python3 orchestrator.py --status
  python3 orchestrator.py --paperclip-issues
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ── Paths ──────────────────────────────────────────────────────────────────────
SKILL_DIR = Path(__file__).parent
WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
ENGINE_DIR = WORKSPACE / "autopilot_affiliate_engine"
CGEN_DIR = WORKSPACE / "content/content-generator/scripts"
NANO_DIR = WORKSPACE / "skills/nano-banana-pro/scripts"
CLIPPER_DIR = WORKSPACE / "skills/auto-clipper/scripts"

# Add local modules to path
sys.path.insert(0, str(SKILL_DIR))
sys.path.insert(0, str(CGEN_DIR))  # storyboard, quality_gate, scheduler

# ── Logging ────────────────────────────────────────────────────────────────────
LOG_DIR = SKILL_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
            LOG_DIR / f"orchestrator_{datetime.now().strftime('%Y%m%d')}.log"
        ),
    ],
)
log = logging.getLogger("ContentKingdom")

# ── Config ─────────────────────────────────────────────────────────────────────
CONFIG_PATH = SKILL_DIR / "config.json"


def load_config() -> dict:
    """Load config.json, merging with engine defaults where possible."""
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)

    # Extend with engine config values (products, account IDs) without duplicating
    engine_config = ENGINE_DIR / "config.py"
    if engine_config.exists():
        # Pull account IDs directly from the engine module via exec
        try:
            ns: dict = {}
            exec(engine_config.read_text(), ns)  # noqa: S102
            cfg.setdefault("account_ids", ns.get("ACCOUNT_IDS", {}))
            cfg.setdefault("all_accounts", ns.get("ALL_ACCOUNTS", []))
            cfg.setdefault("post_limits", ns.get("POST_LIMITS", {}))
            # Merge LYNK product URLs if not already in config
            engine_products = ns.get("LYNK_PRODUCTS", {})
            for cname, p in (
                cfg.get("products", {}).items()
                if isinstance(cfg.get("products"), dict)
                else []
            ):
                if cname in engine_products and "url" not in p:
                    p["url"] = engine_products[cname].get("link", "")
        except Exception as e:
            log.warning("Could not merge engine config: %s", e)

    return cfg


# ── Paperclip client (thin wrapper, mirrors pclip.py) ─────────────────────────
class PaperclipClient:
    """Thin HTTP wrapper for Paperclip API. Single responsibility: HTTP calls."""

    def __init__(self, cfg: dict):
        self.base = cfg.get("paperclip_api_url", "http://localhost:3100/api")
        self.company = cfg.get("paperclip_company_id", "")
        self.project = cfg.get("paperclip_project_id", "")
        self.headers = {
            "Authorization": f"Bearer {cfg.get('paperclip_token', '')}",
            "Content-Type": "application/json",
        }
        try:
            import requests as _req

            self._req = _req
        except ImportError:
            self._req = None

    def _post(self, path: str, data: dict) -> dict:
        if not self._req:
            log.warning("requests not installed — Paperclip call skipped")
            return {}
        try:
            r = self._req.post(
                f"{self.base}{path}", headers=self.headers, json=data, timeout=15
            )
            r.raise_for_status()
            return r.json()
        except Exception as exc:
            log.warning("Paperclip POST %s failed: %s", path, exc)
            return {}

    def _patch(self, path: str, data: dict) -> dict:
        if not self._req:
            return {}
        try:
            r = self._req.patch(
                f"{self.base}{path}", headers=self.headers, json=data, timeout=15
            )
            r.raise_for_status()
            return r.json()
        except Exception as exc:
            log.warning("Paperclip PATCH %s failed: %s", path, exc)
            return {}

    def create_issue(
        self, title: str, description: str = "", parent_id: str | None = None
    ) -> dict:
        payload: dict = {
            "title": title,
            "description": description,
            "companyId": self.company,
            "status": "todo",
        }
        if self.project:
            payload["projectId"] = self.project
        if parent_id:
            payload["parentId"] = parent_id
        # Try /companies/:id/issues first, fall back to /issues
        result = self._post(f"/companies/{self.company}/issues", payload)
        if not result:
            result = self._post("/issues", payload)
        return result

    def _get(self, path: str, params: dict | None = None) -> dict:
        if not self._req:
            return {}
        try:
            r = self._req.get(
                f"{self.base}{path}",
                headers=self.headers,
                params=params or {},
                timeout=15,
            )
            r.raise_for_status()
            return r.json()
        except Exception as exc:
            log.warning("Paperclip GET %s failed: %s", path, exc)
            return {}

    def list_issues(self, limit: int = 50) -> list:
        """List issues for this company."""
        # Try company-scoped first, then plain /issues
        resp = self._get(f"/companies/{self.company}/issues", {"limit": limit})
        if not resp:
            resp = self._get("/issues", {"limit": limit})
        if isinstance(resp, list):
            return resp
        return resp.get("data", resp.get("issues", []))

    def find_issue_by_title(self, title: str) -> dict | None:
        """Find an existing issue by exact title match."""
        issues = self.list_issues(limit=50)
        for issue in issues:
            if issue.get("title") == title:
                return issue
        return None

    def update_issue(self, issue_id: str, status: str, description: str = "") -> dict:
        data: dict = {"status": status}
        if description:
            data["description"] = description
        # Issues endpoint is /api/issues/:id (not under /companies/)
        return self._patch(f"/issues/{issue_id}", data)


# ── State management ───────────────────────────────────────────────────────────
STATE_PATH = SKILL_DIR / "state.json"


def load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except json.JSONDecodeError:
            pass
    return {"runs": [], "last_run": None, "phases": {}}


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2))


# ── subprocess helper (KISS: existing scripts → subprocess, no reimplementation) ──
def run_script(
    script_path: Path | str,
    args: list[str] | None = None,
    timeout: int = 300,
    env: dict | None = None,
) -> tuple[bool, str, str]:
    """
    Run an existing Python script as subprocess.
    Returns (success, stdout, stderr).
    """
    cmd = [sys.executable, str(script_path)] + (args or [])
    run_env = {**os.environ, **(env or {})}
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=run_env,
            cwd=str(Path(script_path).parent),
        )
        ok = result.returncode == 0
        if not ok:
            log.warning(
                "Script %s exited %d:\n%s",
                script_path,
                result.returncode,
                result.stderr[:500],
            )
        return ok, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", f"Timeout after {timeout}s"
    except Exception as exc:
        return False, "", str(exc)


# ── Phase implementations ──────────────────────────────────────────────────────
# Each _phase_*() is a standalone function: single responsibility, testable alone.


def _phase_research(cfg: dict) -> dict:
    """
    Phase 1: RESEARCH
    Delegates to: autopilot_affiliate_engine/research_agent.py (subprocess)
    Also runs: content/content-generator/scripts/viral_research_system.py --mode research
    """
    results: dict = {"sources": []}

    # Run JendralBot research agent
    ok, out, err = run_script(ENGINE_DIR / "research_agent.py", timeout=120)
    results["research_agent"] = {"success": ok, "output_lines": out.count("\n")}
    if ok:
        results["sources"].append("research_agent")

    # Run viral research system
    ok2, out2, _ = run_script(
        CGEN_DIR / "viral_research_system.py",
        args=["--mode", "research"],
        timeout=120,
    )
    results["viral_research"] = {"success": ok2, "output_lines": out2.count("\n")}
    if ok2:
        results["sources"].append("viral_research_system")

    results["success"] = bool(results["sources"])
    return results


def _phase_plan(cfg: dict, research_data: dict | None = None) -> dict:
    """
    Phase 2: PLAN
    Picks today's content from weekly plan & research output.
    Reads: autopilot_affiliate_engine/weekly_content_plan.json
    Generates: output/today_plan.json
    """
    today = datetime.now().strftime("%Y-%m-%d")
    weekday = datetime.now().strftime("%A").lower()

    # Load existing weekly plan if it exists
    weekly_plan_path = ENGINE_DIR / "weekly_content_plan.json"
    weekly_plan: dict = {}
    if weekly_plan_path.exists():
        try:
            weekly_plan = json.loads(weekly_plan_path.read_text())
        except json.JSONDecodeError:
            pass

    # Pick products to promote today (weighted rotation from config)
    products = cfg.get("products", [])
    if isinstance(products, list):
        # simple round-robin based on day-of-week ordinal
        day_index = datetime.now().weekday()
        selected = products[day_index % len(products)] if products else {}
    else:
        selected = {}

    plan = {
        "date": today,
        "weekday": weekday,
        "product_focus": selected.get("id") if isinstance(selected, dict) else selected,
        "platforms": [
            p for p, v in cfg.get("platforms", {}).items() if v.get("enabled")
        ],
        "posting_times": cfg.get("schedule", {}),
        "weekly_plan_found": bool(weekly_plan),
        "content_count_target": 3,  # posts per platform per day
    }

    out_dir = SKILL_DIR / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "today_plan.json").write_text(json.dumps(plan, indent=2))

    return plan


def _phase_script(cfg: dict, plan: dict | None = None) -> dict:
    """
    Phase 3: SCRIPT
    Imports: content/content-generator/scripts/storyboard.py (StoryboardTemplate)
    Uses:    modules/persona_manager.py (PersonaManager)
    Generates: output/scripts_YYYY-MM-DD.json
    """
    today = datetime.now().strftime("%Y-%m-%d")
    scripts: list[dict] = []

    # Import storyboard templates (already proper importable module)
    try:
        import storyboard  # via sys.path from CGEN_DIR

        templates_available = storyboard.list_templates()
        log.info("Storyboard templates available: %s", templates_available)
    except ImportError:
        log.warning("storyboard.py not importable — using fallback templates")
        templates_available = ["ad_short", "product_showcase"]

    # Import persona manager
    try:
        sys.path.insert(0, str(SKILL_DIR / "modules"))
        from persona_manager import PersonaManager  # noqa: PLC0415

        pm = PersonaManager(config_path=str(CONFIG_PATH))
        persona_ids = pm.list_personas()
    except Exception as exc:
        log.warning("PersonaManager load failed: %s", exc)
        pm = None
        persona_ids = []

    # Generate scripts for each platform
    products = cfg.get("products", [])
    if isinstance(products, list) and products:
        product = products[datetime.now().weekday() % len(products)]
    else:
        product = {"id": "jendralbot_bundle", "name": "JENDRALBOT Bundle"}

    platforms = [p for p, v in cfg.get("platforms", {}).items() if v.get("enabled")]

    for platform in platforms:
        for tpl_name in templates_available[:2]:  # max 2 templates per platform
            script_entry: dict = {
                "platform": platform,
                "template": tpl_name,
                "product_id": product.get("id", ""),
                "product_name": product.get("name", ""),
                "generated": today,
            }

            # Generate caption via PersonaManager if available
            if pm and persona_ids:
                try:
                    caption = pm.generate_caption(
                        product_id=product.get("id", ""),
                        persona_id=persona_ids[0],
                        platform=platform,
                        style="hook",
                    )
                    script_entry["caption"] = caption
                except Exception:
                    script_entry["caption"] = _fallback_caption(product, platform)
            else:
                script_entry["caption"] = _fallback_caption(product, platform)

            # Storyboard scenes
            try:
                tpl = storyboard.get_template(tpl_name)
                if tpl:
                    script_entry["scenes"] = [
                        {
                            "scene": s.scene_number,
                            "duration": s.duration_seconds,
                            "description": s.description,
                            "visual_prompt": s.visual_prompt,
                            "text_overlay": s.text_overlay,
                        }
                        for s in tpl.scenes
                    ]
                    script_entry["total_duration"] = tpl.total_duration_seconds
            except Exception:
                script_entry["scenes"] = []

            scripts.append(script_entry)

    out_path = SKILL_DIR / "output" / f"scripts_{today}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({"date": today, "scripts": scripts}, indent=2))

    return {
        "scripts_generated": len(scripts),
        "output_path": str(out_path),
        "templates_used": templates_available[:2],
    }


def _fallback_caption(product: dict, platform: str) -> str:
    hooks = product.get("hooks", [])
    base = hooks[0] if hooks else f"Coba {product.get('name', 'produk ini')} sekarang!"
    if platform == "tiktok":
        return f"{base}\n\n#AI #digitalproduct #jendralbot #fyp #viral"
    if platform == "instagram":
        return f"{base}\n\nLink di bio! 🔥\n\n#AI #digitalproduct #jendralbot #affiliatemarketing #passiveincome"
    return base


def _phase_create(cfg: dict, scripts_path: str | None = None) -> dict:
    """
    Phase 4: CREATE — Full fallback chain media generation with Veris design principles.

    Image chain (5 providers): GeminiGen → NVIDIA → Replicate → Fal.ai → PIL (always works)
    Video chain (5+ providers): BytePlus → XAI/GeminiGen → SiliconFlow → Fal.ai → FFmpeg placeholder

    Platform routing:
      - TikTok/YouTube → video
      - Instagram/Facebook/Threads → image (Veris dark-theme portrait)

    v3.0 change: Uses provider_chain.py for full 9-video + 5-image fallback.
    Veris design principles applied to all prompts (dark theme, 3-zone layout).
    """
    today = datetime.now().strftime("%Y-%m-%d")
    scripts_path = scripts_path or str(SKILL_DIR / "output" / f"scripts_{today}.json")
    out_dir = str(SKILL_DIR / "output" / "media" / today)
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    # Import Veris design + GeminiGen client
    import importlib.util as _ilu

    def _load_mod(name: str, path: Path):
        spec = _ilu.spec_from_file_location(name, str(path))
        mod = _ilu.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    veris = _load_mod("veris_design", SKILL_DIR / "modules" / "veris_design.py")
    gg_mod = _load_mod(
        "geminigen_client", SKILL_DIR / "modules" / "geminigen_client.py"
    )
    media_gen = _load_mod(
        "media_generator", SKILL_DIR / "modules" / "media_generator.py"
    )

    gg_cfg = cfg.get("geminigen", {})
    gg_client = gg_mod.GeminiGenClient(api_key=gg_cfg.get("api_key", ""))

    # Load scripts to get product info + visual prompts
    try:
        scripts_data = json.loads(Path(scripts_path).read_text())
        scripts = scripts_data.get("scripts", [])
    except Exception:
        scripts = []

    generated: list[dict] = []
    VIDEO_PLATFORMS = {"tiktok", "youtube", "reels"}

    for i, script in enumerate(scripts[:5]):  # cap at 5 per run
        scenes = script.get("scenes", [])
        product_name = script.get("product_name", "AI Product")
        platform = script.get("platform", "all").lower()
        media_type = "video" if platform in VIDEO_PLATFORMS else "image"

        # Build Veris-flavoured hook from caption or scenes
        caption = script.get("caption", "")
        hook_text = (
            caption.split("\n")[0][:80] if caption else f"Coba {product_name} Sekarang!"
        )

        if media_type == "image":
            # ── PRIMARY: GeminiGen + Veris design ─────────────────────────────
            veris_payload = veris.veris_prompt_for_platform(
                product_name=product_name,
                hook_text=hook_text,
                platform=platform,
                style=gg_cfg.get("default_style", "Photorealistic"),
            )
            out_path = str(Path(out_dir) / f"image_{i:02d}_{platform}.png")

            success = False
            provider = None

            # Try GeminiGen first
            if gg_client.api_key:
                try:
                    resp = gg_client.generate_image(**veris_payload)
                    uuid = resp.get("uuid") or resp.get("id", "")
                    if uuid:
                        completed = gg_client.wait_for_completion(
                            uuid,
                            timeout=gg_cfg.get("timeout_image_seconds", 120),
                            poll_interval=gg_cfg.get("poll_interval_seconds", 5),
                        )
                        img_url = gg_client.get_image_url(completed)
                        if img_url:
                            # Download to local path
                            import urllib.request as _ur

                            _ur.urlretrieve(img_url, out_path)
                            success = Path(out_path).exists()
                            provider = "geminigen"
                            log.info("GeminiGen: image saved → %s", out_path)
                except Exception as gg_exc:
                    log.warning("GeminiGen image failed: %s — falling back", gg_exc)

            # Fallback: full provider chain (5 providers, always ends with PIL)
            if not success:
                raw_prompt = (
                    scenes[0]["visual_prompt"]
                    if scenes
                    else f"Dark themed marketing image for {product_name}, minimalist, premium, black background"
                )
                try:
                    pc = _load_mod(
                        "provider_chain", SKILL_DIR / "modules" / "provider_chain.py"
                    )
                    res = pc.try_image_providers(raw_prompt, aspect="9:16")
                    result_url = res.get("url")
                    if result_url:
                        # If it's a URL, download; if it's a path, copy
                        if result_url.startswith("http"):
                            import urllib.request as _ur

                            _ur.urlretrieve(result_url, out_path)
                        else:
                            import shutil as _sh

                            _sh.copy(result_url, out_path)
                        success = Path(out_path).exists()
                        provider = res.get("provider", "provider_chain")
                        log.info("Provider chain image: %s → %s", provider, out_path)
                except Exception as pc_exc:
                    log.warning("Provider chain image failed: %s", pc_exc)
                    # Absolute last resort
                    try:
                        _create_pil_placeholder(out_path, product_name, hook_text)
                        success = Path(out_path).exists()
                        provider = "pil_placeholder"
                    except Exception:
                        pass

        else:
            # ── VIDEO: GeminiGen (Grok) → BytePlus ────────────────────────────
            out_path = str(Path(out_dir) / f"video_{i:02d}_{platform}.mp4")
            video_payload = veris.build_video_prompt(product_name, hook_text)
            success = False
            provider = None

            if gg_client.api_key:
                try:
                    resp = gg_client.generate_video_grok(**video_payload)
                    uuid = resp.get("uuid") or resp.get("id", "")
                    if uuid:
                        completed = gg_client.wait_for_completion(
                            uuid,
                            timeout=gg_cfg.get("timeout_video_seconds", 300),
                            poll_interval=gg_cfg.get("poll_interval_seconds", 5),
                        )
                        vid_url = gg_client.get_video_url(completed)
                        if vid_url:
                            import urllib.request as _ur

                            _ur.urlretrieve(vid_url, out_path)
                            success = Path(out_path).exists()
                            provider = "geminigen_grok"
                            log.info("GeminiGen Grok: video saved → %s", out_path)
                except Exception as gg_exc:
                    log.warning("GeminiGen video failed: %s — falling back", gg_exc)

            # Fallback: full video provider chain (BytePlus → XAI → SiliconFlow → Fal.ai → FFmpeg)
            if not success:
                raw_prompt = (
                    scenes[0]["visual_prompt"]
                    if scenes
                    else f"Product showcase for {product_name}, dark premium aesthetic, TikTok vertical"
                )
                try:
                    pc = _load_mod(
                        "provider_chain", SKILL_DIR / "modules" / "provider_chain.py"
                    )
                    res = pc.try_video_providers(raw_prompt)
                    result_url = res.get("url")
                    if result_url:
                        if result_url.startswith("http"):
                            import urllib.request as _ur

                            _ur.urlretrieve(result_url, out_path)
                        else:
                            import shutil as _sh

                            _sh.copy(result_url, out_path)
                        success = Path(out_path).exists()
                        provider = res.get("provider", "provider_chain_video")
                        log.info("Provider chain video: %s → %s", provider, out_path)
                except Exception as pc_exc:
                    log.warning("Provider chain video failed: %s", pc_exc)
                    provider = "provider_chain_failed"

        generated.append(
            {
                "index": i,
                "platform": platform,
                "media_type": media_type,
                "output": out_path if success else None,
                "success": success,
                "provider": provider,
                "product_name": product_name,
            }
        )

    images_ok = sum(1 for g in generated if g["success"] and g["media_type"] == "image")
    videos_ok = sum(1 for g in generated if g["success"] and g["media_type"] == "video")
    return {
        "images_generated": images_ok,
        "videos_generated": videos_ok,
        "total_attempted": len(generated),
        "output_dir": out_dir,
        "providers_used": list({g["provider"] for g in generated if g["provider"]}),
        "veris_design_applied": True,
        "details": generated,
    }


def _create_pil_placeholder(out_path: str, product_name: str, hook_text: str) -> None:
    """
    Create a minimal PIL placeholder image when all API providers fail.
    Follows Veris palette: black background, white text.
    This is the absolute last resort — never blocks the pipeline.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont  # type: ignore[import]
    except ImportError:
        # PIL not available — write a tiny black PNG via raw bytes
        import struct, zlib  # noqa: E401

        def _png(w: int, h: int) -> bytes:
            raw = b"\x00" + b"\x00\x00\x00" * w
            scanlines = raw * h
            compressed = zlib.compress(scanlines)

            def chunk(name: bytes, data: bytes) -> bytes:
                c = name + data
                return (
                    struct.pack(">I", len(data))
                    + c
                    + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
                )

            sig = b"\x89PNG\r\n\x1a\n"
            ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            idat = chunk(b"IDAT", compressed)
            iend = chunk(b"IEND", b"")
            return sig + ihdr + idat + iend

        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        Path(out_path).write_bytes(_png(800, 1000))
        return

    w, h = 800, 1000
    img = Image.new("RGB", (w, h), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    # White text — Veris palette
    try:
        font_lg = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36
        )
        font_sm = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24
        )
    except OSError:
        font_lg = font_sm = ImageFont.load_default()

    draw.text((40, 80), hook_text[:60], fill=(255, 255, 255), font=font_lg)
    draw.text((40, 160), product_name, fill=(128, 128, 128), font=font_sm)
    draw.rectangle([(40, h - 140), (w - 40, h - 60)], outline=(32, 32, 64), width=2)
    draw.text((60, h - 120), "Lihat Selengkapnya →", fill=(255, 255, 255), font=font_sm)

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG")


def _phase_review(cfg: dict, scripts_path: str | None = None) -> dict:
    """
    Phase 5: REVIEW
    Imports: content/content-generator/scripts/quality_gate.py
    Checks all queued content against brand safety + engagement prediction.
    """
    gates_config = cfg.get("quality_gates", {})
    min_score = gates_config.get("min_engagement_prediction_score", 6.0)

    # quality_gate.py is a module-style library (save_gate, get_gate, etc.)
    # We use it to check pending gates and auto-approve scoring-compliant content
    try:
        # Try using our modules.quality_gate (QualityGate class) first
        from modules.quality_gate import QualityGate  # noqa: PLC0415

        qg = QualityGate(cfg)
        today = datetime.now().strftime("%Y-%m-%d")
        sp = scripts_path or str(SKILL_DIR / "output" / f"scripts_{today}.json")
        passed = failed = 0
        try:
            scripts_data = json.loads(Path(sp).read_text())
            for script in scripts_data.get("scripts", []):
                caption = script.get("caption", "")
                platform = script.get("platform", "tiktok")
                report = qg.check_content(caption, platform)
                if report.passed:
                    passed += 1
                else:
                    failed += 1
        except Exception:
            pass
        return {
            "passed": passed,
            "failed": failed,
            "mode": "quality_gate_module",
            "min_score": min_score,
        }
    except Exception as qg_exc:
        log.info("QualityGate module: %s — falling back to basic check", qg_exc)
        return _basic_caption_review(cfg, scripts_path, min_score)


def _basic_caption_review(
    cfg: dict, scripts_path: str | None, min_score: float
) -> dict:
    """Fallback: check captions have required elements."""
    today = datetime.now().strftime("%Y-%m-%d")
    scripts_path = scripts_path or str(SKILL_DIR / "output" / f"scripts_{today}.json")
    gates_config = cfg.get("quality_gates", {})
    passed = failed = 0

    try:
        scripts_data = json.loads(Path(scripts_path).read_text())
        for script in scripts_data.get("scripts", []):
            caption = script.get("caption", "")
            issues = []
            if (
                gates_config.get("required_call_to_action")
                and "link" not in caption.lower()
                and "bio" not in caption.lower()
            ):
                issues.append("missing CTA")
            if gates_config.get("required_hashtags") and "#" not in caption:
                issues.append("missing hashtags")
            if len(caption) < gates_config.get("min_caption_length", 50):
                issues.append("caption too short")
            if issues:
                failed += 1
            else:
                passed += 1
    except Exception:
        pass

    return {"passed": passed, "failed": failed, "mode": "basic_caption_check"}


def _phase_schedule(cfg: dict, paperclip: PaperclipClient | None = None) -> dict:
    """
    Phase 6: SCHEDULE
    Delegates to: autopilot_affiliate_engine/auto_postbridge_robust_v2.py (subprocess)
    Reads existing queue file and schedules via PostBridge.
    """
    queue_file = ENGINE_DIR / "postbridge_queue_jendralbot.json"
    if not queue_file.exists():
        return {
            "skipped": True,
            "reason": "No queue file found",
            "queue_path": str(queue_file),
        }

    ok, out, err = run_script(ENGINE_DIR / "auto_postbridge_robust_v2.py", timeout=300)

    return {
        "success": ok,
        "output_lines": out.count("\n"),
        "queue_file": str(queue_file),
        "error": err[:200] if not ok else None,
    }


def _phase_post(cfg: dict) -> dict:
    """
    Phase 7: POST
    Monitors posting via PostBridge API — checks for failures and retries.
    Delegates retry logic to auto_postbridge_robust_v2.py (already has retry/backoff).
    """
    import requests as req

    api_key = cfg.get("postbridge_api_key", "")
    base_url = cfg.get("postbridge_base_url", "https://api.post-bridge.com/v1")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        resp = req.get(
            f"{base_url}/post-results?page=1&limit=50", headers=headers, timeout=20
        )
        resp.raise_for_status()
        data = resp.json()
        results = data if isinstance(data, list) else data.get("data", [])

        failures = [r for r in results if r.get("status") in ("failed", "error")]
        successes = [r for r in results if r.get("status") in ("published", "success")]

        retry_count = 0
        if failures:
            log.info(
                "Found %d failed posts — triggering retry via robust_v2", len(failures)
            )
            ok, _, _ = run_script(
                ENGINE_DIR / "auto_postbridge_robust_v2.py", timeout=300
            )
            if ok:
                retry_count = len(failures)

        return {
            "total_checked": len(results),
            "successful": len(successes),
            "failed": len(failures),
            "retried": retry_count,
        }

    except Exception as exc:
        log.warning("PostBridge post-results fetch failed: %s", exc)
        return {"error": str(exc), "retried": 0}


def _phase_engage(cfg: dict, prev_comment_counts: dict | None = None) -> dict:
    """
    Phase 8: ENGAGE
    Uses: modules/comment_manager.py (new — CommentManager)
    """
    try:
        # Direct import to avoid modules/__init__.py triggering PostBridgeClient
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "comment_manager", str(SKILL_DIR / "modules" / "comment_manager.py")
        )
        cm_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cm_mod)
        module = cm_mod.CommentManager(cfg)
        result = module.monitor_comments(hours=24)
        return {
            "comments_found": len(result) if isinstance(result, list) else 0,
            "mode": "comment_manager",
        }
    except Exception as exc:
        log.warning("CommentManager: %s — skipping engage", exc)
        return {"skipped": True, "reason": str(exc)}


def _phase_analyze(cfg: dict) -> dict:
    """
    Phase 9: ANALYZE
    Delegates to: autopilot_affiliate_engine/evening_report.py (subprocess)
    Also runs: autopilot_affiliate_engine/revenue_tracker.py
    Fetches PostBridge analytics for the day.
    """
    results: dict = {}

    # Evening report
    ok, out, _ = run_script(ENGINE_DIR / "evening_report.py", timeout=120)
    results["evening_report"] = {"success": ok, "lines": out.count("\n")}

    # Revenue tracker
    ok2, out2, _ = run_script(ENGINE_DIR / "revenue_tracker.py", timeout=120)
    results["revenue_tracker"] = {"success": ok2, "lines": out2.count("\n")}

    # Pull raw analytics from PostBridge API
    import requests as req

    api_key = cfg.get("postbridge_api_key", "")
    base_url = cfg.get("postbridge_base_url", "https://api.post-bridge.com/v1")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        resp = req.get(
            f"{base_url}/analytics?page=1&limit=100", headers=headers, timeout=20
        )
        resp.raise_for_status()
        data = resp.json()
        posts = data if isinstance(data, list) else data.get("data", [])
        results["analytics"] = {
            "posts_fetched": len(posts),
            "total_views": sum(p.get("views_count", 0) or 0 for p in posts),
            "total_likes": sum(p.get("likes_count", 0) or 0 for p in posts),
            "total_comments": sum(p.get("comments_count", 0) or 0 for p in posts),
            "total_shares": sum(p.get("shares_count", 0) or 0 for p in posts),
        }
        results["raw_posts"] = posts  # passed downstream to Phase 10+12
    except Exception as exc:
        log.warning("Analytics fetch failed: %s", exc)
        results["analytics"] = {"error": str(exc)}
        results["raw_posts"] = []

    return results


def _phase_optimize(cfg: dict, analyze_data: dict | None = None) -> dict:
    """
    Phase 10: OPTIMIZE
    Identifies patterns in winners, suggests improvements.
    Delegates to: revenue_tracker_REAL.py for revenue correlation.
    """
    raw_posts = (analyze_data or {}).get("raw_posts", [])

    # Compute simple engagement rate per platform
    by_platform: dict[str, dict] = {}
    for post in raw_posts:
        p = (post.get("platform") or "unknown").lower()
        if p not in by_platform:
            by_platform[p] = {"views": 0, "likes": 0, "comments": 0, "count": 0}
        by_platform[p]["views"] += post.get("views_count", 0) or 0
        by_platform[p]["likes"] += post.get("likes_count", 0) or 0
        by_platform[p]["comments"] += post.get("comments_count", 0) or 0
        by_platform[p]["count"] += 1

    recommendations: list[str] = []
    for platform, stats in by_platform.items():
        views = stats["views"]
        count = stats["count"] or 1
        avg_views = views / count
        if avg_views < 100:
            recommendations.append(
                f"{platform}: avg views low ({avg_views:.0f}) — test new hooks"
            )
        elif avg_views > 1000:
            recommendations.append(
                f"{platform}: strong performer ({avg_views:.0f} avg views) — increase volume"
            )

    # Run revenue tracker for correlation
    ok, _, _ = run_script(ENGINE_DIR / "revenue_tracker_REAL.py", timeout=60)

    today = datetime.now().strftime("%Y-%m-%d")
    opt_path = SKILL_DIR / "output" / f"optimize_{today}.json"
    opt_path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "date": today,
        "by_platform": by_platform,
        "recommendations": recommendations,
        "revenue_tracker_ran": ok,
    }
    opt_path.write_text(json.dumps(report, indent=2))

    return {
        "recommendations": len(recommendations),
        "platforms_analyzed": len(by_platform),
        "report_path": str(opt_path),
    }


def _phase_repurpose(cfg: dict, **kwargs) -> dict:
    """
    Phase 11: REPURPOSE
    Delegates to: skills/auto-clipper/scripts/auto_clipper.py (subprocess)
    Long videos → short clips. Text → carousel.
    """
    clipper = CLIPPER_DIR / "auto_clipper.py"
    if not clipper.exists():
        return {"skipped": True, "reason": "auto_clipper.py not found"}

    ok, out, err = run_script(clipper, timeout=300)
    return {
        "success": ok,
        "output_lines": out.count("\n"),
        "error": err[:200] if not ok else None,
    }


def _phase_scale(cfg: dict, analyze_data: dict | None = None) -> dict:
    """
    Phase 12: SCALE
    Uses: modules/engagement_engine.py (new — EngagementEngine)
    """
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "engagement_engine", str(SKILL_DIR / "modules" / "engagement_engine.py")
        )
        ee_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ee_mod)
        raw_posts = (analyze_data or {}).get("raw_posts", [])
        module = ee_mod.EngagementEngine(cfg)

        # Use available methods: warm up accounts + boost recent posts
        warmed = 0
        boosted = 0
        for post in raw_posts[:5]:  # Top 5 recent posts
            post_id = post.get("id") or post.get("post_id", "")
            if post_id:
                try:
                    module.boost_new_post(post_id, [])
                    boosted += 1
                except Exception:
                    pass

        return {"boosted": boosted, "warmed": warmed, "posts_analyzed": len(raw_posts)}
    except Exception as exc:
        log.warning("EngagementEngine: %s — skipping scale", exc)
        return {"skipped": True, "reason": str(exc)}


# ── Phase registry — Open/Closed: add new phase here, no other changes needed ─
PHASES: dict[str, dict] = {
    "research": {"fn": _phase_research, "label": "Phase 1: RESEARCH", "deps": []},
    "plan": {"fn": _phase_plan, "label": "Phase 2: PLAN", "deps": ["research"]},
    "script": {"fn": _phase_script, "label": "Phase 3: SCRIPT", "deps": ["plan"]},
    "create": {"fn": _phase_create, "label": "Phase 4: CREATE", "deps": ["script"]},
    "review": {"fn": _phase_review, "label": "Phase 5: REVIEW", "deps": ["script"]},
    "schedule": {
        "fn": _phase_schedule,
        "label": "Phase 6: SCHEDULE",
        "deps": ["review"],
    },
    "post": {"fn": _phase_post, "label": "Phase 7: POST", "deps": ["schedule"]},
    "engage": {"fn": _phase_engage, "label": "Phase 8: ENGAGE", "deps": ["post"]},
    "analyze": {"fn": _phase_analyze, "label": "Phase 9: ANALYZE", "deps": ["post"]},
    "optimize": {
        "fn": _phase_optimize,
        "label": "Phase 10: OPTIMIZE",
        "deps": ["analyze"],
    },
    "repurpose": {
        "fn": _phase_repurpose,
        "label": "Phase 11: REPURPOSE",
        "deps": ["analyze"],
    },
    "scale": {"fn": _phase_scale, "label": "Phase 12: SCALE", "deps": ["analyze"]},
}


# ── Orchestrator ───────────────────────────────────────────────────────────────
class ContentKingdomOrchestrator:
    """
    Thin coordinator. Sequences phases, persists state, integrates Paperclip.

    Public API (Interface Segregation):
      run_daily_pipeline()     → full 12-phase daily cycle
      run_phase(name)          → run single phase independently
      get_status()             → current state as JSON-serialisable dict
      create_paperclip_issues()→ seed Paperclip issue tree for today's run
    """

    def __init__(self, config_path: str | None = None):
        global CONFIG_PATH
        if config_path:
            CONFIG_PATH = Path(config_path)
        self.cfg = load_config()
        self.state = load_state()
        self.paperclip = PaperclipClient(self.cfg)
        self._run_context: dict = {}  # cross-phase data passed between phases

    # ── Public API ─────────────────────────────────────────────────────────────

    def run_daily_pipeline(self) -> dict:
        """Execute all 12 phases in order. Each phase gets context from previous."""
        today = datetime.now().strftime("%Y-%m-%d")
        run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        log.info("🚀 Content Kingdom Daily Pipeline — %s [%s]", today, run_id)

        # Create Paperclip tracking issues
        parent_id = self.create_paperclip_issues(run_id=run_id)

        run_record: dict = {
            "run_id": run_id,
            "date": today,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "phases": {},
            "paperclip_parent": parent_id,
        }

        analyze_data: dict = {}

        for phase_name, phase_meta in PHASES.items():
            label = phase_meta["label"]
            log.info("\n%s\n▶ %s\n%s", "=" * 60, label, "=" * 60)

            result = self.run_phase(phase_name, _run_context=self._run_context)
            run_record["phases"][phase_name] = result

            # Feed analyze output downstream to optimize/repurpose/scale
            if phase_name == "analyze":
                analyze_data = result.get("data", {})
                self._run_context["analyze_data"] = analyze_data

            # Update Paperclip sub-issue status
            issue_id = self._run_context.get(f"paperclip_{phase_name}")
            if issue_id:
                status = "done" if result.get("status") == "success" else "blocked"
                desc = json.dumps(result.get("data", {}), indent=2)[:500]
                self.paperclip.update_issue(issue_id, status, description=desc)

        run_record["finished_at"] = datetime.now(timezone.utc).isoformat()
        self.state["last_run"] = run_id
        self.state["runs"].append(run_record)
        self.state["runs"] = self.state["runs"][-30:]  # keep last 30 runs
        save_state(self.state)

        log.info("✅ Pipeline complete. Run ID: %s", run_id)
        return run_record

    def run_phase(self, phase_name: str, _run_context: dict | None = None) -> dict:
        """
        Run a single named phase independently.
        Returns serialisable result dict: {phase, status, data, error, duration_seconds}.
        """
        from base_module import PhaseResult, PhaseStatus  # noqa: PLC0415
        import datetime as dt

        phase_meta = PHASES.get(phase_name)
        if not phase_meta:
            return {
                "phase": phase_name,
                "status": "failed",
                "error": f"Unknown phase '{phase_name}'. Valid: {list(PHASES)}",
            }

        ctx = _run_context or self._run_context
        start = time.monotonic()
        ts = dt.datetime.now(dt.timezone.utc).isoformat()

        # Build kwargs from context
        kwargs: dict = {}
        if phase_name in ("create",):
            today = dt.datetime.now().strftime("%Y-%m-%d")
            kwargs["scripts_path"] = str(SKILL_DIR / "output" / f"scripts_{today}.json")
        if phase_name in ("optimize", "scale", "repurpose"):
            kwargs["analyze_data"] = ctx.get("analyze_data", {})
        if phase_name == "engage":
            kwargs["prev_comment_counts"] = ctx.get("prev_comment_counts", {})

        try:
            data = phase_meta["fn"](self.cfg, **kwargs)
            elapsed = time.monotonic() - start
            result = {
                "phase": phase_name,
                "status": "success",
                "data": data,
                "duration_seconds": round(elapsed, 2),
                "timestamp": ts,
            }
        except Exception as exc:
            elapsed = time.monotonic() - start
            log.error("Phase [%s] raised: %s", phase_name, exc, exc_info=True)
            result = {
                "phase": phase_name,
                "status": "failed",
                "error": str(exc),
                "duration_seconds": round(elapsed, 2),
                "timestamp": ts,
            }

        # Persist phase state
        self.state.setdefault("phases", {})[phase_name] = {
            "last_run": ts,
            "status": result["status"],
        }
        save_state(self.state)
        return result

    def get_status(self) -> dict:
        """Return current pipeline status as JSON-serialisable dict."""
        state = load_state()
        return {
            "last_run": state.get("last_run"),
            "total_runs": len(state.get("runs", [])),
            "phases": state.get("phases", {}),
            "config_path": str(CONFIG_PATH),
            "skill_dir": str(SKILL_DIR),
            "available_phases": list(PHASES.keys()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def create_paperclip_issues(self, run_id: str | None = None) -> str | None:
        """
        Create OR REUSE parent issue for today's run + sub-issues per phase.
        Deduplicates by title: "Content Kingdom — YYYY-MM-DD".
        Returns parent issue ID (or None if Paperclip unavailable).
        """
        today = datetime.now().strftime("%Y-%m-%d")
        run_label = run_id or f"run_{today}"
        parent_title = f"Content Kingdom — {today}"

        # Check for existing parent issue (dedup)
        existing = self.paperclip.find_issue_by_title(parent_title)
        if existing:
            parent_id = existing.get("id")
            log.info("📋 Paperclip: reusing existing issue %s", parent_id)
            # Update description with new run
            self.paperclip.update_issue(
                parent_id,
                "todo",
                f"Daily content pipeline run (rerun). ID: {run_label}\n\n12 phases: {', '.join(PHASES)}",
            )
            return parent_id

        # Create new parent issue
        parent = self.paperclip.create_issue(
            title=parent_title,
            description=f"Daily content pipeline run. ID: {run_label}\n\n12 phases: {', '.join(PHASES)}",
        )
        parent_id = parent.get("id") or parent.get("data", {}).get("id")
        if not parent_id:
            log.warning("Paperclip parent issue creation failed or server unavailable")
            return None

        log.info("📋 Paperclip parent issue: %s", parent_id)

        # Sub-issues per phase
        for phase_name, phase_meta in PHASES.items():
            sub_title = f"{phase_meta['label']}"
            # Check if sub-issue already exists
            existing_sub = self.paperclip.find_issue_by_title(sub_title)
            if existing_sub:
                sub_id = existing_sub.get("id")
            else:
                sub = self.paperclip.create_issue(
                    title=sub_title,
                    description=f"Phase: {phase_name} | Parent run: {run_label}",
                    parent_id=parent_id,
                )
                sub_id = sub.get("id") or sub.get("data", {}).get("id")
            if sub_id:
                self._run_context[f"paperclip_{phase_name}"] = sub_id

        return parent_id


# ── CLI entry point ────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Content Kingdom Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 orchestrator.py --pipeline               # Full 12-phase daily run
  python3 orchestrator.py --phase research         # Single phase
  python3 orchestrator.py --phase schedule         # Schedule posts
  python3 orchestrator.py --status                 # Show pipeline status
  python3 orchestrator.py --paperclip-issues       # Seed Paperclip issues only

Cron:
  0 8  * * *  cd /path/to/content-kingdom && python3 orchestrator.py --pipeline
  0 20 * * *  cd /path/to/content-kingdom && python3 orchestrator.py --phase analyze
  0 */2 * * * cd /path/to/content-kingdom && python3 orchestrator.py --phase engage
        """,
    )
    parser.add_argument(
        "--pipeline", action="store_true", help="Run full daily pipeline"
    )
    parser.add_argument(
        "--phase", metavar="PHASE", help=f"Run single phase: {list(PHASES)}"
    )
    parser.add_argument(
        "--status", action="store_true", help="Print current status JSON"
    )
    parser.add_argument(
        "--paperclip-issues",
        action="store_true",
        help="Create Paperclip issues for today",
    )
    parser.add_argument("--config", metavar="PATH", help="Custom config.json path")
    args = parser.parse_args()

    orch = ContentKingdomOrchestrator(config_path=args.config)

    if args.status:
        print(json.dumps(orch.get_status(), indent=2))

    elif args.paperclip_issues:
        pid = orch.create_paperclip_issues()
        print(f"Paperclip parent issue: {pid}")

    elif args.phase:
        result = orch.run_phase(args.phase)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result.get("status") == "success" else 1)

    elif args.pipeline:
        record = orch.run_daily_pipeline()
        failed = [
            p
            for p, v in record.get("phases", {}).items()
            if v.get("status") == "failed"
        ]
        if failed:
            log.warning("Pipeline finished with failures: %s", failed)
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
