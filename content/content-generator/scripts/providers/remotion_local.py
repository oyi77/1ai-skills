"""Remotion local image and video generation provider.

Fully local fallback provider - zero API dependency.
Generates animated videos from images, text, and audio using Remotion.
Also generates static images using PIL when all image APIs are down.
"""

import os
import json
import subprocess
import shutil
import tempfile
from pathlib import Path
from typing import Optional

from .base import AIProvider, ProviderType, GenerationResult

REMOTION_ENGINE_DIR = Path(__file__).resolve().parents[4] / "remotion_engine"


class RemotionVideoProvider(AIProvider):
    """Remotion local video provider - fallback when all video APIs are down.

    Generates animated videos locally using Remotion compositions:
    - KenBurns slideshow from images
    - Animated text reveals
    - Caption animations synced to audio
    - Motion graphics and transitions
    """

    COMPOSITIONS = [
        "NicheFlow",
        "MasterpieceV2",
        "MasterpieceV3",
        "Sample5s",
    ]

    def __init__(self, engine_dir: Optional[str] = None, **kwargs):
        self.engine_dir = Path(engine_dir) if engine_dir else REMOTION_ENGINE_DIR
        super().__init__(
            provider_type=ProviderType.VIDEO,
            provider_name="Remotion Local",
            api_key="local",
            **kwargs,
        )

    @property
    def supported_models(self) -> list[str]:
        return self.COMPOSITIONS

    async def generate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> GenerationResult:
        """Generate video using Remotion.

        Args:
            prompt: Text content for the video (used for captions/overlays)
            model: Composition ID (default: NicheFlow)
            **kwargs:
                images: List of image file paths
                texts: List of text overlays per scene
                audio_path: Path to voiceover audio
                bgm_path: Path to background music
                output_path: Where to save the rendered video
                width: Video width (default 1080)
                height: Video height (default 1920)
                fps: Frames per second (default 30)
                duration_seconds: Total video duration
        """
        composition = model or "NicheFlow"
        output_path = kwargs.get("output_path") or self._default_output_path()

        # Build input props for Remotion
        props = {
            "prompt": prompt,
            "images": kwargs.get("images", []),
            "texts": kwargs.get("texts", [prompt]),
            "audioPath": kwargs.get("audio_path", ""),
            "bgmPath": kwargs.get("bgm_path", ""),
        }

        # Copy assets to Remotion public directory if provided
        self._stage_assets(props)

        # Calculate duration
        fps = kwargs.get("fps", 30)
        duration_seconds = kwargs.get("duration_seconds", 30)
        duration_frames = int(duration_seconds * fps)

        try:
            props_json = json.dumps(props)
            cmd = [
                "npx",
                "remotion",
                "render",
                composition,
                str(output_path),
                f"--props={props_json}",
                f"--width={kwargs.get('width', 1080)}",
                f"--height={kwargs.get('height', 1920)}",
                f"--fps={fps}",
                f"--frames=0-{duration_frames - 1}",
                "--codec=h264",
                "--log=error",
            ]

            result = subprocess.run(
                cmd,
                cwd=str(self.engine_dir),
                capture_output=True,
                text=True,
                timeout=300,
            )

            if result.returncode != 0:
                return GenerationResult(
                    success=False,
                    provider=self.provider_name,
                    model=composition,
                    metadata={
                        "error": result.stderr[:500],
                        "command": " ".join(cmd),
                    },
                )

            return GenerationResult(
                success=True,
                data=str(output_path),
                cost=0.0,
                provider=self.provider_name,
                model=composition,
                metadata={"local": True, "duration_seconds": duration_seconds},
            )

        except subprocess.TimeoutExpired:
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=composition,
                metadata={"error": "Remotion render timed out (5min)"},
            )
        except Exception as e:
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=composition,
                metadata={"error": str(e)},
            )

    def _stage_assets(self, props: dict):
        """Copy provided image/audio files into Remotion's public/assets dir."""
        assets_dir = self.engine_dir / "public" / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)

        staged_images = []
        for i, img_path in enumerate(props.get("images", [])):
            if os.path.isfile(img_path):
                ext = Path(img_path).suffix or ".jpg"
                dest = assets_dir / f"scene_{i:02d}{ext}"
                shutil.copy2(img_path, dest)
                staged_images.append(f"assets/scene_{i:02d}{ext}")
        props["images"] = staged_images

        for key, prop_key in [("audioPath", "audio_path"), ("bgmPath", "bgm_path")]:
            path = props.get(key, "")
            if path and os.path.isfile(path):
                dest = assets_dir / Path(path).name
                shutil.copy2(path, dest)
                props[key] = f"assets/{Path(path).name}"

    def _default_output_path(self) -> str:
        output_dir = REMOTION_ENGINE_DIR.parent / "output" / "remotion"
        output_dir.mkdir(parents=True, exist_ok=True)
        import time

        return str(output_dir / f"video_{int(time.time())}.mp4")

    async def is_available(self) -> bool:
        """Check if Remotion CLI is available."""
        try:
            result = subprocess.run(
                ["npx", "remotion", "--version"],
                cwd=str(self.engine_dir),
                capture_output=True,
                text=True,
                timeout=15,
            )
            return result.returncode == 0
        except Exception:
            return False

    def get_cost_estimate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> float:
        return 0.0  # Fully local, no API cost

    def validate_api_key(self) -> bool:
        return True  # No API key needed


class RemotionImageProvider(AIProvider):
    """Local static image generation using PIL - last resort for images.

    Generates styled text-on-gradient images when all image APIs are down.
    """

    def __init__(self, **kwargs):
        super().__init__(
            provider_type=ProviderType.IMAGE,
            provider_name="Remotion Static",
            api_key="local",
            **kwargs,
        )

    @property
    def supported_models(self) -> list[str]:
        return ["gradient-text", "solid-text"]

    async def generate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> GenerationResult:
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=model or "gradient-text",
                metadata={"error": "PIL not installed"},
            )

        width = kwargs.get("width", 1080)
        height = kwargs.get("height", 1920)
        output_path = kwargs.get("output_path")

        if not output_path:
            output_dir = REMOTION_ENGINE_DIR.parent / "output" / "static_images"
            output_dir.mkdir(parents=True, exist_ok=True)
            import time

            output_path = str(output_dir / f"img_{int(time.time())}.png")

        try:
            img = Image.new("RGB", (width, height))
            draw = ImageDraw.Draw(img)

            # Gradient background
            for y in range(height):
                r = int(20 + (40 * y / height))
                g = int(10 + (20 * y / height))
                b = int(40 + (80 * y / height))
                draw.line([(0, y), (width, y)], fill=(r, g, b))

            # Text overlay
            text = prompt[:120]
            try:
                font = ImageFont.truetype(
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56
                )
            except OSError:
                font = ImageFont.load_default()

            # Word wrap
            words = text.split()
            lines = []
            current_line = ""
            for word in words:
                test = f"{current_line} {word}".strip()
                bbox = draw.textbbox((0, 0), test, font=font)
                if bbox[2] - bbox[0] > width - 120:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
                else:
                    current_line = test
            if current_line:
                lines.append(current_line)

            y_offset = height // 2 - (len(lines) * 70) // 2
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                x = (width - (bbox[2] - bbox[0])) // 2
                # Shadow
                draw.text((x + 3, y_offset + 3), line, fill=(0, 0, 0), font=font)
                draw.text((x, y_offset), line, fill=(255, 255, 255), font=font)
                y_offset += 70

            img.save(output_path, quality=95)

            return GenerationResult(
                success=True,
                data=output_path,
                cost=0.0,
                provider=self.provider_name,
                model=model or "gradient-text",
                metadata={"local": True, "dimensions": f"{width}x{height}"},
            )

        except Exception as e:
            return GenerationResult(
                success=False,
                provider=self.provider_name,
                model=model or "gradient-text",
                metadata={"error": str(e)},
            )

    async def is_available(self) -> bool:
        try:
            from PIL import Image

            return True
        except ImportError:
            return False

    def get_cost_estimate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> float:
        return 0.0

    def validate_api_key(self) -> bool:
        return True
