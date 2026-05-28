#!/usr/bin/env python3
"""
GeminiGen AI Production-Grade Client

Robust implementation with:
- Proper error handling
- Exponential backoff retry
- Rate limiting compliance
- Async polling with timeout
- All media types: image, video (veo/sora/grok), TTS
"""

import os
import sys
import time
import json
import logging
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GenerationStatus(IntEnum):
    """GeminiGen API status codes"""
    PROCESSING = 1
    COMPLETED = 2
    FAILED = 3


@dataclass
class GenerationResult:
    """Result of a generation request"""
    uuid: str
    status: GenerationStatus
    result_url: Optional[str] = None
    error_message: Optional[str] = None
    raw_response: Optional[Dict] = None


class GeminiGenError(Exception):
    """Base exception for GeminiGen errors"""
    pass


class RateLimitError(GeminiGenError):
    """Rate limit exceeded"""
    pass


class GenerationFailedError(GeminiGenError):
    """Generation failed on server side"""
    pass


class TimeoutError(GeminiGenError):
    """Polling timeout"""
    pass


class GeminiGenClient:
    """
    Production-grade GeminiGen AI client.
    
    Usage:
        client = GeminiGenClient()
        
        # Generate image
        result = client.generate_image("A cat in space", style="Photorealistic")
        
        # Generate video
        result = client.generate_video_veo("A sunset timelapse", model="veo-2")
        
        # Generate TTS
        result = client.generate_tts("Hello world", voice_name="Gacrux")
    """
    
    BASE_URL = "https://api.geminigen.ai/uapi/v1"
    
    # Rate limits for nano-banana-pro (free tier)
    RATE_LIMIT_PER_MINUTE = 5
    RATE_LIMIT_PER_HOUR = 100
    RATE_LIMIT_PER_DAY = 1000
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize client.
        
        Args:
            api_key: GeminiGen API key. If None, reads from GEMINIGEN_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("GEMINIGEN_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Set GEMINIGEN_API_KEY env var or pass api_key parameter."
            )
        
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": self.api_key,
            "Accept": "application/json"
        })
        
        # Request tracking for rate limiting
        self._request_times: List[float] = []
    
    def _check_rate_limit(self, model: str = "nano-banana-pro") -> None:
        """Check and enforce rate limits for free tier models."""
        if model != "nano-banana-pro":
            return  # No rate limit for paid models
        
        now = time.time()
        minute_ago = now - 60
        hour_ago = now - 3600
        
        # Clean old entries
        self._request_times = [t for t in self._request_times if t > hour_ago]
        
        # Check limits
        recent_minute = sum(1 for t in self._request_times if t > minute_ago)
        recent_hour = len(self._request_times)
        
        if recent_minute >= self.RATE_LIMIT_PER_MINUTE:
            wait_time = 60 - (now - self._request_times[-self.RATE_LIMIT_PER_MINUTE])
            logger.warning(f"Rate limit: {recent_minute}/min. Waiting {wait_time:.1f}s...")
            time.sleep(wait_time + 1)
        
        if recent_hour >= self.RATE_LIMIT_PER_HOUR:
            raise RateLimitError(f"Hourly rate limit exceeded ({recent_hour}/{self.RATE_LIMIT_PER_HOUR})")
        
        self._request_times.append(now)
    
    def _request_with_retry(
        self,
        method: str,
        endpoint: str,
        max_retries: int = 3,
        **kwargs
    ) -> requests.Response:
        """
        Make request with exponential backoff retry.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (without base URL)
            max_retries: Maximum retry attempts
            **kwargs: Additional arguments for requests
        
        Returns:
            Response object
        """
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        
        for attempt in range(max_retries + 1):
            try:
                response = self.session.request(method, url, timeout=60, **kwargs)
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    logger.warning(f"Rate limited. Waiting {retry_after}s...")
                    time.sleep(retry_after)
                    continue
                
                # Handle server errors with retry
                if response.status_code >= 500:
                    if attempt < max_retries:
                        wait = 2 ** attempt
                        logger.warning(f"Server error {response.status_code}. Retry in {wait}s...")
                        time.sleep(wait)
                        continue
                
                return response
                
            except requests.exceptions.RequestException as e:
                if attempt < max_retries:
                    wait = 2 ** attempt
                    logger.warning(f"Request failed: {e}. Retry in {wait}s...")
                    time.sleep(wait)
                else:
                    raise GeminiGenError(f"Request failed after {max_retries} retries: {e}")
        
        raise GeminiGenError("Max retries exceeded")
    
    def _poll_for_result(
        self,
        uuid: str,
        timeout: int = 300,
        poll_interval: int = 5
    ) -> GenerationResult:
        """
        Poll for generation result with timeout.
        
        Args:
            uuid: Generation UUID
            timeout: Maximum wait time in seconds
            poll_interval: Time between polls in seconds
        
        Returns:
            GenerationResult with status and result URL
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            response = self._request_with_retry("GET", f"/history/{uuid}")
            
            try:
                data = response.json()
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON response: {response.text[:200]}")
                time.sleep(poll_interval)
                continue
            
            # Check for API-level error
            if data.get("code") and data.get("code") != "200":
                if data.get("code") == "404":
                    # UUID not found yet, keep polling
                    time.sleep(poll_interval)
                    continue
                raise GeminiGenError(f"API error: {data.get('message', 'Unknown error')}")
            
            status = data.get("status", 1)
            
            if status == GenerationStatus.COMPLETED:
                # Get result URL from various possible fields
                result_url = (
                    data.get("generate_result") or
                    data.get("generated_image", [{}])[0].get("image_url") or
                    data.get("generated_video", [{}])[0].get("video_url") or
                    data.get("generated_audio", [{}])[0].get("audio_url")
                )
                
                return GenerationResult(
                    uuid=uuid,
                    status=GenerationStatus.COMPLETED,
                    result_url=result_url,
                    raw_response=data
                )
            
            elif status == GenerationStatus.FAILED:
                error_msg = data.get("error_message", "Unknown error")
                return GenerationResult(
                    uuid=uuid,
                    status=GenerationStatus.FAILED,
                    error_message=error_msg,
                    raw_response=data
                )
            
            # Still processing
            progress = data.get("status_percentage", 0)
            logger.info(f"Processing... {progress}%")
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Generation timed out after {timeout}s")
    
    def generate_image(
        self,
        prompt: str,
        model: str = "nano-banana-pro",
        aspect_ratio: str = "1:1",
        style: str = "Photorealistic",
        resolution: str = "1K",
        output_format: str = "jpeg",
        ref_image_url: Optional[str] = None,
        wait_for_result: bool = True,
        timeout: int = 120
    ) -> GenerationResult:
        """
        Generate an image from text prompt.
        
        Args:
            prompt: Image description
            model: nano-banana-pro (free), nano-banana-2, imagen-4
            aspect_ratio: 1:1, 16:9, 9:16, 4:3, 3:4
            style: None, 3D Render, Photorealistic, Anime General, etc.
            resolution: 1K, 2K, 4K
            output_format: jpeg, png
            ref_image_url: Optional reference image URL
            wait_for_result: Whether to poll until complete
            timeout: Max wait time in seconds
        
        Returns:
            GenerationResult with image URL
        """
        self._check_rate_limit(model)
        
        data = {
            "prompt": prompt,
            "model": model,
            "aspect_ratio": aspect_ratio,
            "style": style,
            "resolution": resolution,
            "output_format": output_format
        }
        
        if ref_image_url:
            data["file_urls"] = ref_image_url
        
        logger.info(f"Generating image: {prompt[:50]}...")
        
        response = self._request_with_retry(
            "POST",
            "/generate_image",
            data=data
        )
        
        result = response.json()
        
        # Check for immediate error
        if result.get("code") and result.get("code") not in ["200", "201"]:
            raise GeminiGenError(f"API error: {result.get('message', result)}")
        
        uuid = result.get("uuid")
        if not uuid:
            raise GeminiGenError(f"No UUID in response: {result}")
        
        logger.info(f"Generation started: {uuid}")
        
        if wait_for_result:
            return self._poll_for_result(uuid, timeout=timeout)
        
        return GenerationResult(
            uuid=uuid,
            status=GenerationStatus.PROCESSING,
            raw_response=result
        )
    
    def generate_video_veo(
        self,
        prompt: str,
        model: str = "veo-2",
        aspect_ratio: str = "9:16",
        resolution: str = "720p",
        ref_image_url: Optional[str] = None,
        wait_for_result: bool = True,
        timeout: int = 600
    ) -> GenerationResult:
        """
        Generate video using Google Veo models.
        
        Args:
            prompt: Video description
            model: veo-2, veo-3.1, veo-3.1-fast
            aspect_ratio: 16:9, 9:16 (veo-2 only)
            resolution: 720p, 1080p (veo-3.1 only)
            ref_image_url: Optional reference image for image-to-video
            wait_for_result: Whether to poll until complete
            timeout: Max wait time in seconds
        
        Returns:
            GenerationResult with video URL
        """
        data = {
            "prompt": prompt,
            "model": model,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution
        }
        
        if ref_image_url:
            data["file_urls"] = ref_image_url
        
        logger.info(f"Generating Veo video: {prompt[:50]}...")
        
        response = self._request_with_retry(
            "POST",
            "/video-gen/veo",
            data=data
        )
        
        result = response.json()
        
        if result.get("code") and result.get("code") not in ["200", "201"]:
            raise GeminiGenError(f"API error: {result.get('message', result)}")
        
        uuid = result.get("uuid")
        if not uuid:
            raise GeminiGenError(f"No UUID in response: {result}")
        
        logger.info(f"Veo generation started: {uuid}")
        
        if wait_for_result:
            return self._poll_for_result(uuid, timeout=timeout, poll_interval=10)
        
        return GenerationResult(
            uuid=uuid,
            status=GenerationStatus.PROCESSING,
            raw_response=result
        )
    
    def generate_video_sora(
        self,
        prompt: str,
        model: str = "sora-2",
        aspect_ratio: str = "portrait",
        resolution: str = "small",
        duration: int = 10,
        wait_for_result: bool = True,
        timeout: int = 600
    ) -> GenerationResult:
        """
        Generate video using OpenAI Sora models.
        
        Args:
            prompt: Video description
            model: sora-2, sora-2-pro, sora-2-pro-hd
            aspect_ratio: landscape, portrait
            resolution: small (720p), large (1080p, sora-2-pro-hd only)
            duration: 10, 15, 25 seconds depending on model
            wait_for_result: Whether to poll until complete
            timeout: Max wait time in seconds
        
        Returns:
            GenerationResult with video URL
        """
        data = {
            "prompt": prompt,
            "model": model,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "duration": duration
        }
        
        logger.info(f"Generating Sora video: {prompt[:50]}...")
        
        response = self._request_with_retry(
            "POST",
            "/video-gen/sora",
            data=data
        )
        
        result = response.json()
        
        if result.get("code") and result.get("code") not in ["200", "201"]:
            raise GeminiGenError(f"API error: {result.get('message', result)}")
        
        uuid = result.get("uuid")
        if not uuid:
            raise GeminiGenError(f"No UUID in response: {result}")
        
        logger.info(f"Sora generation started: {uuid}")
        
        if wait_for_result:
            return self._poll_for_result(uuid, timeout=timeout, poll_interval=10)
        
        return GenerationResult(
            uuid=uuid,
            status=GenerationStatus.PROCESSING,
            raw_response=result
        )
    
    def generate_video_grok(
        self,
        prompt: str,
        model: str = "grok-aurora",
        aspect_ratio: str = "9:16",
        ref_image_url: Optional[str] = None,
        wait_for_result: bool = True,
        timeout: int = 600
    ) -> GenerationResult:
        """
        Generate video using xAI Grok models.
        
        Args:
            prompt: Video description
            model: grok-aurora
            aspect_ratio: 16:9, 9:16
            ref_image_url: Optional reference image for image-to-video
            wait_for_result: Whether to poll until complete
            timeout: Max wait time in seconds
        
        Returns:
            GenerationResult with video URL
        """
        data = {
            "prompt": prompt,
            "model": model,
            "aspect_ratio": aspect_ratio
        }
        
        if ref_image_url:
            data["file_urls"] = ref_image_url
        
        logger.info(f"Generating Grok video: {prompt[:50]}...")
        
        response = self._request_with_retry(
            "POST",
            "/video-gen/grok",
            data=data
        )
        
        result = response.json()
        
        if result.get("code") and result.get("code") not in ["200", "201"]:
            raise GeminiGenError(f"API error: {result.get('message', result)}")
        
        uuid = result.get("uuid")
        if not uuid:
            raise GeminiGenError(f"No UUID in response: {result}")
        
        logger.info(f"Grok generation started: {uuid}")
        
        if wait_for_result:
            return self._poll_for_result(uuid, timeout=timeout, poll_interval=10)
        
        return GenerationResult(
            uuid=uuid,
            status=GenerationStatus.PROCESSING,
            raw_response=result
        )
    
    def generate_tts(
        self,
        text: str,
        model: str = "tts-flash",
        voice_id: str = "GM013",
        voice_name: str = "Gacrux",
        speed: float = 1.0,
        output_format: str = "mp3",
        wait_for_result: bool = True,
        timeout: int = 120
    ) -> GenerationResult:
        """
        Generate text-to-speech audio.
        
        Args:
            text: Text to convert (max 10,000 chars)
            model: tts-flash (fast), tts-pro (quality)
            voice_id: Voice ID (e.g., GM013)
            voice_name: Voice name (e.g., Gacrux)
            speed: Speech speed (1-4)
            output_format: mp3, wav
            wait_for_result: Whether to poll until complete
            timeout: Max wait time in seconds
        
        Returns:
            GenerationResult with audio URL
        """
        if len(text) > 10000:
            raise ValueError(f"Text too long: {len(text)} chars (max 10,000)")
        
        payload = {
            "model": model,
            "voices": [{"name": voice_name, "voice": {"id": voice_id, "name": voice_name}}],
            "speed": speed,
            "input": text,
            "output_format": output_format
        }
        
        logger.info(f"Generating TTS: {text[:50]}...")
        
        response = self._request_with_retry(
            "POST",
            "/text-to-speech",
            json=payload
        )
        
        result = response.json()
        
        if result.get("code") and result.get("code") not in ["200", "201"]:
            raise GeminiGenError(f"API error: {result.get('message', result)}")
        
        uuid = result.get("uuid")
        if not uuid:
            raise GeminiGenError(f"No UUID in response: {result}")
        
        logger.info(f"TTS generation started: {uuid}")
        
        if wait_for_result:
            return self._poll_for_result(uuid, timeout=timeout)
        
        return GenerationResult(
            uuid=uuid,
            status=GenerationStatus.PROCESSING,
            raw_response=result
        )
    
    def get_history(
        self,
        uuid: Optional[str] = None,
        filter_by: str = "all",
        page: int = 1,
        items_per_page: int = 10
    ) -> Dict[str, Any]:
        """
        Get generation history.
        
        Args:
            uuid: Specific generation UUID (if provided, gets single item)
            filter_by: Filter type (all, image, video, audio)
            page: Page number
            items_per_page: Items per page
        
        Returns:
            History data dict
        """
        if uuid:
            response = self._request_with_retry("GET", f"/history/{uuid}")
        else:
            response = self._request_with_retry(
                "GET",
                "/histories",
                params={
                    "filter_by": filter_by,
                    "page": page,
                    "items_per_page": items_per_page
                }
            )
        
        return response.json()
    
    def download_result(
        self,
        url: str,
        output_path: str,
        timeout: int = 120
    ) -> str:
        """
        Download generated media to file.
        
        Args:
            url: Media URL
            output_path: Local file path
            timeout: Download timeout in seconds
        
        Returns:
            Output file path
        """
        logger.info(f"Downloading to {output_path}...")
        
        response = requests.get(url, timeout=timeout, stream=True)
        response.raise_for_status()
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        logger.info(f"Downloaded: {output_path}")
        return str(output_path)


def main():
    """CLI entry point for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="GeminiGen AI Client")
    parser.add_argument("action", choices=["image", "video-veo", "video-sora", "video-grok", "tts", "history"])
    parser.add_argument("--prompt", "-p", help="Generation prompt")
    parser.add_argument("--model", "-m", help="Model to use")
    parser.add_argument("--aspect", "-a", default="9:16", help="Aspect ratio")
    parser.add_argument("--style", "-s", default="Photorealistic", help="Image style")
    parser.add_argument("--uuid", help="UUID for history lookup")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--timeout", "-t", type=int, default=300, help="Timeout in seconds")
    
    args = parser.parse_args()
    
    client = GeminiGenClient()
    
    try:
        if args.action == "image":
            if not args.prompt:
                parser.error("--prompt required for image generation")
            result = client.generate_image(
                args.prompt,
                model=args.model or "nano-banana-pro",
                aspect_ratio=args.aspect,
                style=args.style,
                timeout=args.timeout
            )
        
        elif args.action == "video-veo":
            if not args.prompt:
                parser.error("--prompt required for video generation")
            result = client.generate_video_veo(
                args.prompt,
                model=args.model or "veo-2",
                aspect_ratio=args.aspect,
                timeout=args.timeout
            )
        
        elif args.action == "video-sora":
            if not args.prompt:
                parser.error("--prompt required for video generation")
            result = client.generate_video_sora(
                args.prompt,
                model=args.model or "sora-2",
                aspect_ratio="portrait" if args.aspect == "9:16" else "landscape",
                timeout=args.timeout
            )
        
        elif args.action == "video-grok":
            if not args.prompt:
                parser.error("--prompt required for video generation")
            result = client.generate_video_grok(
                args.prompt,
                model=args.model or "grok-aurora",
                aspect_ratio=args.aspect,
                timeout=args.timeout
            )
        
        elif args.action == "tts":
            if not args.prompt:
                parser.error("--prompt (text) required for TTS")
            result = client.generate_tts(
                args.prompt,
                model=args.model or "tts-flash",
                timeout=args.timeout
            )
        
        elif args.action == "history":
            data = client.get_history(uuid=args.uuid)
            print(json.dumps(data, indent=2))
            return
        
        # Print result
        print(f"\nStatus: {result.status.name}")
        if result.result_url:
            print(f"Result URL: {result.result_url}")
            
            if args.output:
                client.download_result(result.result_url, args.output)
        
        if result.error_message:
            print(f"Error: {result.error_message}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
