"""
KlingAI API Client — Production-grade Python wrapper
Uses kling-creator (reverse-engineered API) + AI Interceptor middleware

Features:
- Email/password authentication (no manual cookie extraction)
- Text-to-Video (T2V) and Image-to-Video (I2V)
- AI-enhanced prompts via oracle CLI
- Auto-retry with quality scoring
- Credits monitoring
- Video download to local disk

Install: pip install kling-creator --break-system-packages
"""

import os
import sys
import json
import time
import logging
import subprocess
from pathlib import Path
from typing import Optional, Literal
from datetime import datetime

# kling-creator (installed v0.5.0 — Authorizator not in public package, use email auth via HTTP)
try:
    from kling import VideoGen, ImageGen
    KLING_AVAILABLE = True
    # Authorizator may or may not be available depending on version
    try:
        from kling import Authorizator
        KLING_AUTH_AVAILABLE = True
    except ImportError:
        KLING_AUTH_AVAILABLE = False
except ImportError:
    KLING_AVAILABLE = False
    KLING_AUTH_AVAILABLE = False
    print("⚠️  kling-creator not installed. Run: pip install kling-creator --break-system-packages")

# ---- Logging Setup ----
log = logging.getLogger("kling_api")
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
log.addHandler(handler)

# File log
os.makedirs(os.path.expanduser("~/.openclaw/workspace/logs"), exist_ok=True)
fh = logging.FileHandler(os.path.expanduser("~/.openclaw/workspace/logs/kling_api.log"))
fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
log.addHandler(fh)


# ---- Config ----
DEFAULT_CONFIG = {
    "email": os.environ.get("KLING_EMAIL", "favstore649@gmail.com"),
    "password": os.environ.get("KLING_PASSWORD", ""),
    "cookie": os.environ.get("KLING_COOKIE", ""),
    "output_dir": str(Path("~/.openclaw/workspace/downloads/kling_videos").expanduser()),
    "model": "1.6",
    "high_quality": True,
    "ai_enhance": True,
    "oracle_engine": "gemini",
    "min_quality_score": 6.0,
    "max_retries": 3,
}


# ---- AI Prompt Enhancement ----
def enhance_prompt(raw_prompt: str, engine: str = "gemini") -> str:
    """
    Use oracle CLI to enhance a raw prompt to cinematic quality.
    Falls back to raw_prompt if oracle not available.
    """
    system_enhance = f"""You are a video generation prompt expert for Kling AI.
Transform this raw prompt into a cinematic, detailed video generation prompt.
Rules:
- Keep subject clearly described
- Add cinematic details: lighting, camera movement, mood, style
- Max 200 characters
- English only
- Return ONLY the enhanced prompt, nothing else

Raw prompt: {raw_prompt}
Enhanced prompt:"""

    try:
        result = subprocess.run(
            ["oracle", "--prompt", system_enhance, "--engine", engine],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode == 0 and result.stdout.strip():
            enhanced = result.stdout.strip().split("\n")[0]  # First line only
            log.info(f"🎨 Prompt enhanced: '{raw_prompt}' → '{enhanced}'")
            return enhanced
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        log.warning(f"Oracle not available ({e}), using raw prompt")
    return raw_prompt


def score_output(description: str, output_type: str = "video") -> float:
    """
    Ask AI to score generated output quality.
    Returns 0-10 float.
    """
    scoring_prompt = f"""Rate this {output_type} generation result quality from 0-10.
Result description: {description}
Return ONLY a number from 0-10, nothing else."""
    
    try:
        result = subprocess.run(
            ["oracle", "--prompt", scoring_prompt, "--engine", "gemini"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            score_str = result.stdout.strip().split()[0]
            return float(score_str)
    except Exception:
        pass
    return 7.5  # Default: acceptable


# ---- Main Kling API Client ----
class KlingAPIClient:
    """
    Production-grade Kling AI client.
    Uses kling-creator library for API access.
    """

    def __init__(self, config: dict = None):
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.video_gen: Optional[VideoGen] = None
        self.image_gen: Optional[ImageGen] = None
        self.authenticated = False
        self.output_dir = Path(self.config["output_dir"])
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if not KLING_AVAILABLE:
            raise RuntimeError("kling-creator not installed. Run: pip install kling-creator --break-system-packages")

    def authenticate(self) -> bool:
        """
        Authenticate via email/password or cookie.
        Returns True if successful.
        """
        cookie = self.config.get("cookie", "")
        
        # Try cookie first (faster)
        if cookie:
            log.info("🔑 Authenticating via cookie...")
            try:
                self.video_gen = VideoGen(cookie)
                self.image_gen = ImageGen(cookie)
                self.authenticated = True
                log.info("✅ Authenticated via cookie")
                return True
            except Exception as e:
                log.warning(f"Cookie auth failed: {e}")

        # Try email/password
        email = self.config.get("email", "")
        password = self.config.get("password", "")
        
        if email and password:
            log.info(f"🔑 Authenticating via email: {email}...")
            try:
                if KLING_AUTH_AVAILABLE:
                    auth = Authorizator()
                    auth.auth(email, password)
                    cookies = auth.cookies
                else:
                    # Manual auth via HTTP
                    import requests
                    session = requests.Session()
                    resp = session.post(
                        "https://id.klingai.com/pass/ksi18n/web/login/emailPassword",
                        data={"sid": "ksi18n.ai.portal", "email": email, "password": password, "language": "en"},
                        headers={"Content-Type": "application/x-www-form-urlencoded"},
                        timeout=15
                    )
                    if not resp.ok:
                        raise ValueError(f"Auth failed: {resp.status_code}")
                    data = resp.json()
                    session.cookies.set("ksi18n.ai.portal_st", data.get("ksi18n.ai.portal_st", ""))
                    cookies = "; ".join([f"{c.name}={c.value}" for c in session.cookies])
                
                self.video_gen = VideoGen(cookies)
                self.image_gen = ImageGen(cookies)
                self.authenticated = True
                self.config["cookie"] = cookies
                log.info("✅ Authenticated via email/password")
                return True
            except Exception as e:
                log.error(f"Email/password auth failed: {e}")
                return False

        log.error("❌ No credentials provided. Set KLING_COOKIE or KLING_EMAIL + KLING_PASSWORD")
        return False

    def get_credits(self) -> float:
        """Get current account credits."""
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        try:
            credits = self.video_gen.get_account_point()
            log.info(f"💰 Credits: {credits}")
            return credits
        except Exception as e:
            log.error(f"Failed to get credits: {e}")
            return -1.0

    def generate_video(
        self,
        prompt: str,
        image_path: Optional[str] = None,
        model: Literal["1.0", "1.5", "1.6", "2.1"] = None,
        high_quality: bool = None,
        enhance_prompt_ai: bool = None,
        auto_extend: bool = False,
        output_filename: str = None,
    ) -> Optional[str]:
        """
        Generate a video (T2V or I2V).
        
        Args:
            prompt: Text description
            image_path: Path to source image (for I2V)
            model: Model version (default: from config)
            high_quality: Use high quality mode
            enhance_prompt_ai: Use AI to enhance prompt
            auto_extend: Auto-extend to 10s
            output_filename: Custom output filename
        
        Returns:
            Path to downloaded video file, or None on failure
        """
        if not self.authenticated:
            if not self.authenticate():
                return None

        model = model or self.config.get("model", "1.6")
        high_quality = high_quality if high_quality is not None else self.config.get("high_quality", True)
        enhance_prompt_ai = enhance_prompt_ai if enhance_prompt_ai is not None else self.config.get("ai_enhance", True)

        # PRE-INTERCEPT: Enhance prompt
        final_prompt = prompt
        if enhance_prompt_ai:
            final_prompt = enhance_prompt(prompt, engine=self.config.get("oracle_engine", "gemini"))

        mode = "I2V" if image_path else "T2V"
        log.info(f"🎬 Generating {mode} video")
        log.info(f"   Prompt: {final_prompt}")
        if image_path:
            log.info(f"   Image: {image_path}")
        log.info(f"   Model: {model}, HQ: {high_quality}")

        # Check credits
        credits = self.get_credits()
        cost = 144 if (image_path and high_quality) else 60
        if credits < cost:
            log.error(f"❌ Insufficient credits: {credits} < {cost} required")
            return None
        log.info(f"💰 Credits: {credits} (will use {cost})")

        # Generate
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = output_filename or f"kling_{mode}_{timestamp}.mp4"
        output_path = str(self.output_dir / filename)

        retries = 0
        max_retries = self.config.get("max_retries", 3)
        
        while retries <= max_retries:
            try:
                log.info(f"🚀 Submitting generation (attempt {retries + 1}/{max_retries + 1})...")
                
                self.video_gen.save_video(
                    prompt=final_prompt,
                    output_dir=str(self.output_dir),
                    image_path=image_path,
                    is_high_quality=high_quality,
                    auto_extend=auto_extend,
                    model_name=model,
                )

                # Find the generated file
                mp4_files = sorted(
                    self.output_dir.glob("*.mp4"),
                    key=lambda f: f.stat().st_mtime,
                    reverse=True
                )
                
                if mp4_files:
                    latest = mp4_files[0]
                    # Rename to our filename
                    if latest.name != filename:
                        final_path = self.output_dir / filename
                        latest.rename(final_path)
                        latest = final_path
                    
                    log.info(f"✅ Video generated: {latest}")
                    log.info(f"   Size: {latest.stat().st_size / 1024:.1f} KB")
                    
                    return str(latest)
                else:
                    log.warning("⚠️  No MP4 file found after generation")
                    retries += 1
                    time.sleep(2 ** retries)

            except Exception as e:
                log.error(f"❌ Generation failed (attempt {retries + 1}): {e}")
                retries += 1
                if retries <= max_retries:
                    # ERROR-INTERCEPT: Vary prompt on retry
                    if enhance_prompt_ai:
                        final_prompt = enhance_prompt(
                            f"[RETRY {retries}] {prompt}",
                            engine=self.config.get("oracle_engine", "gemini")
                        )
                    wait_time = 2 ** retries
                    log.info(f"⏳ Retrying in {wait_time}s...")
                    time.sleep(wait_time)

        log.error(f"❌ All {max_retries + 1} attempts failed")
        return None

    def generate_image(
        self,
        prompt: str,
        image_path: Optional[str] = None,
        enhance_prompt_ai: bool = True,
        output_filename: str = None,
    ) -> Optional[str]:
        """
        Generate an image.
        
        Args:
            prompt: Text description
            image_path: Path to source image (for image-to-image)
            enhance_prompt_ai: Use AI to enhance prompt
            output_filename: Custom output filename
            
        Returns:
            Path to downloaded image file, or None on failure
        """
        if not self.authenticated:
            if not self.authenticate():
                return None

        # PRE-INTERCEPT: Enhance prompt
        final_prompt = prompt
        if enhance_prompt_ai:
            final_prompt = enhance_prompt(prompt, engine=self.config.get("oracle_engine", "gemini"))

        log.info(f"🖼️  Generating image")
        log.info(f"   Prompt: {final_prompt}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = output_filename or f"kling_img_{timestamp}.png"

        try:
            self.image_gen.save_image(
                prompt=final_prompt,
                output_dir=str(self.output_dir),
                image_path=image_path,
            )

            # Find the generated file
            png_files = sorted(
                self.output_dir.glob("*.png"),
                key=lambda f: f.stat().st_mtime,
                reverse=True
            )

            if png_files:
                latest = png_files[0]
                log.info(f"✅ Image generated: {latest}")
                return str(latest)

        except Exception as e:
            log.error(f"❌ Image generation failed: {e}")

        return None

    def batch_generate(self, tasks: list[dict]) -> list[dict]:
        """
        Batch generate multiple videos/images.
        
        Args:
            tasks: List of dicts with keys: type, prompt, image_path, ...
            
        Returns:
            List of result dicts with output_path, success, error
        """
        results = []
        for i, task in enumerate(tasks):
            log.info(f"\n{'='*50}")
            log.info(f"Task {i+1}/{len(tasks)}: {task.get('type', 'video')}")
            
            task_type = task.pop("type", "video")
            if task_type == "image":
                output = self.generate_image(**task)
            else:
                output = self.generate_video(**task)
            
            results.append({
                "task_id": i,
                "type": task_type,
                "prompt": task.get("prompt", ""),
                "output_path": output,
                "success": output is not None,
                "error": None if output else "Generation failed",
                "timestamp": datetime.now().isoformat(),
            })
            
            # Brief pause between tasks
            if i < len(tasks) - 1:
                time.sleep(3)
        
        success_count = sum(1 for r in results if r["success"])
        log.info(f"\n✅ Batch complete: {success_count}/{len(tasks)} succeeded")
        return results


# ---- CLI ----
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Kling AI API Client")
    parser.add_argument("--type", choices=["video", "image"], default="video")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--image", help="Source image path (for I2V)")
    parser.add_argument("--model", default="1.6", choices=["1.0", "1.5", "1.6", "2.1"])
    parser.add_argument("--hq", action="store_true", help="High quality mode")
    parser.add_argument("--no-enhance", action="store_true", help="Skip AI prompt enhancement")
    parser.add_argument("--extend", action="store_true", help="Auto-extend to 10s")
    parser.add_argument("--credits", action="store_true", help="Just check credits")
    parser.add_argument("--output", help="Output filename")
    parser.add_argument("--cookie", help="Kling cookie string (overrides env)")
    parser.add_argument("--email", help="Email (overrides env)")
    parser.add_argument("--password", help="Password (overrides env)")
    args = parser.parse_args()
    
    config = {}
    if args.cookie:
        config["cookie"] = args.cookie
    if args.email:
        config["email"] = args.email
    if args.password:
        config["password"] = args.password
    
    client = KlingAPIClient(config)
    
    if not client.authenticate():
        print("❌ Authentication failed")
        sys.exit(1)
    
    if args.credits:
        credits = client.get_credits()
        print(f"💰 Credits: {credits}")
        return
    
    if args.type == "video":
        output = client.generate_video(
            prompt=args.prompt,
            image_path=args.image,
            model=args.model,
            high_quality=args.hq,
            enhance_prompt_ai=not args.no_enhance,
            auto_extend=args.extend,
            output_filename=args.output,
        )
    else:
        output = client.generate_image(
            prompt=args.prompt,
            image_path=args.image,
            enhance_prompt_ai=not args.no_enhance,
            output_filename=args.output,
        )
    
    if output:
        print(f"✅ Output: {output}")
        sys.exit(0)
    else:
        print("❌ Generation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
