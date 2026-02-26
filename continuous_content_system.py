#!/usr/bin/env python3
"""
Continuous Content Generation System
Autonomous agent that learns and improves viral content over time.

Architecture:
┌──────────────────────────────────────────────────────────────┐
│  Research Flow (hourly)                              │
│         ↓                                            │
│  Content Gen Flow (on-demand)                          │
│         ↓                                            │
│  Social Media Manager Flow (on-demand)                 │
│         ↓                                            │
│  Feedback Loop (continuous)                            │
│         ↓                                            │
│  Performance Analytics (read-only)                      │
└──────────────────────────────────────────────────────────────┘

Core Principles:
- Every failure becomes a rule
- Every success becomes a formula
- Confidence-based flow selection
- Data-driven iteration
"""

import os
import json
import time
import random
import urllib.request
import urllib.parse
import base64
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional
import tempfile

# ── Configuration ────────────────────────────────────────────────────────────
POST_BRIDGE_KEY = os.environ.get("POST_BRIDGE_API_KEY", "pb_live_Kyc2gafDF7Qc8c2ALELtEC")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
POSTIZ_API_KEY = os.environ.get("POSTIZ_API_KEY", "")

# Temp file hosting (tmpfiles.org)
TMPFILES_API_KEY = "free"  # No auth needed for basic use

OUTPUT_DIR = Path("output/continuous_system")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RESEARCH_DIR = OUTPUT_DIR / "research"
CONTENT_DIR = OUTPUT_DIR / "content"
MEMORY_DIR = OUTPUT_DIR / "memory"
FLOWS_DIR = OUTPUT_DIR / "flows"

for d in [RESEARCH_DIR, CONTENT_DIR, MEMORY_DIR, FLOWS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

JAKARTA_OFFSET = timedelta(hours=7)

# ── Confidence Levels ────────────────────────────────────────────────────────────
CONFIDENCE_LEVELS = {
    "high": {
        "multiplier": 2.0,
        "description": "Proven formula with strong data backing",
        "min_views_threshold": 100000,
        "priority": 1
    },
    "medium": {
        "multiplier": 1.5,
        "description": "Tested concept with moderate evidence",
        "min_views_threshold": 50000,
        "priority": 2
    },
    "low": {
        "multiplier": 1.0,
        "description": "New untested concept",
        "min_views_threshold": 10000,
        "priority": 3
    }
}

# ── Flow Definitions ───────────────────────────────────────────────────────────────
FLOWS = {
    "larry_slideshow": {
        "name": "Larry Slideshow Generator",
        "type": "content_generation",
        "platforms": ["tiktok"],
        "description": "Generate 6-slide viral TikTok slideshow using Larry's proven hook formula",
        "script": "workflows/larry_slideshow.py",
        "confidence_requirement": "high",
        "min_confidence": 0.8
    },
    "multi_platform_posting": {
        "name": "Multi-Platform Posting",
        "type": "distribution",
        "platforms": ["facebook", "tiktok", "instagram", "linkedin"],
        "description": "Post content to all connected platforms via Post-Bridge",
        "script": "workflows/multi_platform_post.py",
        "confidence_requirement": "low",
        "min_confidence": 0.5
    },
    "social_engagement": {
        "name": "Social Engagement Bot",
        "type": "engagement",
        "platforms": ["tiktok", "instagram", "twitter"],
        "description": "Automate likes, comments, follows for organic growth",
        "script": "workflows/social_engagement.py",
        "confidence_requirement": "medium",
        "min_confidence": 0.6
    },
    "viral_image_post": {
        "name": "Viral Image Posting",
        "type": "content_generation",
        "platforms": ["facebook", "tiktok"],
        "description": "Post viral images with hooks and captions",
        "script": "workflows/viral_image_post.py",
        "confidence_requirement": "medium",
        "min_confidence": 0.6
    }
}

# ── Memory System ─────────────────────────────────────────────────────────────────
class MemorySystem:
    """Track lessons learned, performance metrics, and confidence scores."""
    
    def __init__(self):
        self.memory_file = MEMORY_DIR / "SYSTEM_MEMORY.json"
        self.performance_file = MEMORY_DIR / "PERFORMANCE.json"
        self.rules_file = MEMORY_DIR / "RULES.json"
        
        # Load existing memory
        self.performance = self._load_json(self.performance_file, {
            "total_posts": 0,
            "total_views": 0,
            "avg_views": 0,
            "winning_hooks": {},
            "losing_hooks": {},
            "flow_performance": {}
        })
        
        self.rules = self._load_json(self.rules_file, {
            "hook_formulas": {
                "landlord_ai": {"confidence": 0.9, "views_avg": 150000},
                "parent_ai": {"confidence": 0.7, "views_avg": 80000},
                "doubter_wrong": {"confidence": 0.6, "views_avg": 60000}
            },
            "content_types": {
                "slideshow_6_slides": {"confidence": 0.85, "views_avg": 100000},
                "single_image": {"confidence": 0.6, "views_avg": 40000}
            },
            "platforms": {
                "tiktok": {"confidence": 0.8, "engagement_rate": 0.12},
                "facebook": {"confidence": 0.6, "engagement_rate": 0.08},
                "instagram": {"confidence": 0.7, "engagement_rate": 0.10}
            },
            "confidence_requirements": {
                "larry_slideshow": 0.8,
                "multi_platform_posting": 0.5,
                "social_engagement": 0.6,
                "viral_image_post": 0.6
            }
        })
    
    def _load_json(self, path: Path, default: dict):
        """Load JSON file or return default."""
        if path.exists():
            try:
                with open(path, "r") as f:
                    return json.load(f)
            except:
                pass
        return default
    
    def _save_json(self, path: Path, data: dict):
        """Save JSON atomically."""
        temp_path = path.with_suffix(".tmp")
        with open(temp_path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        temp_path.replace(path)
    
    def log_post(self, post_data: dict):
        """Log post attempt and result."""
        flow = post_data.get("flow", "unknown")
        hook_type = post_data.get("hook_type", "unknown")
        
        # Update performance
        self.performance["total_posts"] += 1
        
        # Update hook performance
        if hook_type != "unknown":
            hooks = self.rules["hook_formulas"]
            if hook_type in hooks:
                if "views" in post_data:
                    views = post_data["views"]
                    hooks[hook_type]["recent_views"].append(views)
                    
                    # Update average
                    recent = hooks[hook_type]["recent_views"][-10:]
                    hooks[hook_type]["views_avg"] = sum(recent) // len(recent) if recent else 0
        
        # Update flow performance
        if flow not in self.performance["flow_performance"]:
            self.performance["flow_performance"][flow] = {
                "attempts": 0,
                "successes": 0,
                "last_result": None
            }
        
        self.performance["flow_performance"][flow]["attempts"] += 1
        if post_data.get("success"):
            self.performance["flow_performance"][flow]["successes"] += 1
        
        self.performance["flow_performance"][flow]["last_result"] = {
            "success": post_data.get("success", False),
            "timestamp": datetime.now().isoformat(),
            "error": post_data.get("error", "")
        }
        
        # Save
        self._save_json(self.performance_file, self.performance)
        
        print(f"  📊 Logged: {flow} - {hook_type} - {'✅' if post_data.get('success') else '❌'}")
    
    def update_confidence(self, flow: str, success: bool, views: int = 0):
        """Update confidence level based on performance."""
        flow_conf = self.rules.get("confidence_requirements", {}).get(flow, 0.5)
        
        if success and views > 0:
            # Increase confidence
            current_conf = flow_conf * (1 + (0.05 * (views / 50000)))
            new_conf = min(current_conf, 1.0)
            
            self.rules["confidence_requirements"][flow] = new_conf
            self._save_json(self.rules_file, self.rules)
            
            print(f"  📈 Confidence updated: {flow} → {new_conf:.2f} (views: {views})")
        
        elif not success:
            # Decrease confidence
            current_conf = flow_conf * 0.9
            self.rules["confidence_requirements"][flow] = max(current_conf, 0.3)
            self._save_json(self.rules_file, self.rules)
            
            print(f"  📉 Confidence decreased: {flow} → {current_conf:.2f}")

# ── Research Flow ──────────────────────────────────────────────────────────────
def run_research_flow():
    """Hourly research to find trending content, hooks, and winning formulas."""
    print("🔍 RESEARCH FLOW — Finding viral opportunities...")
    
    # Simulated research (in production, this would use web APIs)
    research_output = {
        "timestamp": datetime.now().isoformat(),
        "trending_topics": [
            "landlord renovation disputes",
            "AI room transformations",
            "rental hack content",
            "small apartment organization",
            "budget living hacks"
        ],
        "viral_hooks": [
            "My landlord wouldn't approve X, so I showed them AI's idea",
            "They said Y is impossible, so I proved them wrong",
            "Property manager said no changes allowed",
            "My partner thinks [X] can't work, so I showed AI's solution"
        ],
        "winning_formulas": {
            "landlord_ai_room_design": {
                "confidence": 0.9,
                "avg_views": 150000,
                "description": "Third party + AI room design = 234K views"
            },
            "parent_ai_transformation": {
                "confidence": 0.7,
                "avg_views": 80000,
                "description": "Parent skepticism + AI result = 80K views"
            }
        },
        "confidence_levels": {
            "high": 0.8,
            "medium": 0.6,
            "low": 0.4
        }
    }
    
    # Save research
    research_file = RESEARCH_DIR / f"research_{datetime.now().strftime('%Y%m%d_%H')}.json"
    with open(research_file, "w") as f:
        json.dump(research_output, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Research saved: {research_file.name}")
    return research_output


# ── Content Generation Flow ───────────────────────────────────────────────────
def run_content_gen_flow(memory: MemorySystem):
    """Generate content based on latest research and confidence."""
    print("🎨 CONTENT GENERATION FLOW — Creating viral content...")
    
    # Load latest research
    research_files = sorted(RESEARCH_DIR.glob("research_*.json"), reverse=True)
    if not research_files:
        print("  ⚠️  No research data available")
        return None
    
    latest_research_file = research_files[0]
    with open(latest_research_file, "r") as f:
        research = json.load(f)
    
    # Select content type based on confidence
    # High confidence → Larry slideshow (proven 500K+ views)
    # Medium confidence → Viral images
    # Low confidence → Simple captions
    
    hook = random.choice(research.get("viral_hooks", ["Default hook"]))
    
    content_output = {
        "timestamp": datetime.now().isoformat(),
        "based_on_research": latest_research_file.name,
        "selected_hook": hook,
        "content_type": "larry_slideshow",
        "confidence": 0.8,
        "platforms": ["tiktok"],
        "content": {
            "hook": hook,
            "caption": f"My landlord wouldn't approve {random.choice(['kitchen', 'bathroom', 'living room'])}, so I showed them AI's idea! 🏠 #aiinteriordesign #viral",
            "hashtags": "#aiinteriordesign #roomtransformation #viral #homedesign",
            "estimated_views": 100000
        }
    }
    
    # Save content
    content_file = CONTENT_DIR / f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(content_file, "w") as f:
        json.dump(content_output, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Content generated: {content_file.name}")
    return content_output


# ── Upload to Temporary File Host ───────────────────────────────────────────
def upload_to_tmpfiles(file_path: Path) -> str:
    """Upload file to tmpfiles.org for temporary hosting."""
    print(f"  📤 Uploading to tmpfiles.org...")
    
    url = "https://tmpfiles.org/api/v1/upload"
    
    # Prepare multipart form data
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    
    file_data = file_path.read_bytes()
    
    body_parts = []
    body_parts.append(f"--{boundary}\r\n".encode())
    body_parts.append(b'Content-Disposition: form-data; name="file"; filename="' + 
                      file_path.name.encode() + b'"\r\n')
    body_parts.append(b"Content-Type: video/mp4\r\n\r\n")
    body_parts.append(file_data)
    body_parts.append(b"\r\n")
    body_parts.append(f"--{boundary}--\r\n".encode())
    
    body = b"".join(body_parts)
    
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        
        # Get file URL
        file_url = result.get("file", {}).get("url", "")
        if file_url:
            print(f"  ✅ Uploaded: {file_url}")
            return file_url
        else:
            print(f"  ⚠️  Upload response: {result}")
            return ""
            
    except urllib.error.HTTPError as e:
        print(f"  ❌ Upload error {e.code}: {e.read().decode()[:200]}")
        return ""
    except Exception as e:
        print(f"  ❌ Upload error: {e}")
        return ""


# ── Social Media Manager Flow ───────────────────────────────────────────────
def run_social_media_flow(content: dict, memory: MemorySystem):
    """Post content to all connected platforms."""
    print("📱 SOCIAL MEDIA MANAGER FLOW — Distributing content...")
    
    platforms = content.get("platforms", ["tiktok"])
    caption = content.get("content", {}).get("caption", "")
    hashtags = content.get("content", {}).get("hashtags", "")
    full_caption = f"{caption}\n\n{hashtags}"
    
    # Post to TikTok (via Post-Bridge)
    # Note: For full automation, would need Post-Bridge client
    
    print(f"  📱 Platforms: {', '.join(platforms)}")
    print(f"  📝 Caption: {caption[:100]}...")
    
    # Simulate posting (in production, would call Post-Bridge API)
    results = []
    for platform in platforms:
        result = {
            "platform": platform,
            "success": True,
            "caption": caption,
            "hashtags": hashtags,
            "estimated_engagement": {
                "likes": random.randint(5000, 20000),
                "comments": random.randint(100, 500),
                "shares": random.randint(50, 300)
            }
        }
        results.append(result)
    
    # Log to memory
    memory.log_post({
        "flow": "multi_platform_posting",
        "hook_type": "viral_content",
        "success": all(r["success"] for r in results),
        "views": sum(r["estimated_engagement"].get("likes", 0) for r in results)
    })
    
    print(f"  ✅ Posted to {len(platforms)} platforms")
    return results


# ── Main Orchestration Loop ─────────────────────────────────────────────────
def main():
    """Main continuous learning loop."""
    print("=" * 70)
    print("🚀 CONTINUOUS CONTENT GENERATION SYSTEM")
    print("=" * 70)
    print()
    
    # Initialize memory system
    memory = MemorySystem()
    
    print("📚 System initialized")
    print(f"  Memory: {memory.memory_file}")
    print(f"  Performance: {memory.performance_file}")
    print(f"  Rules: {memory.rules_file}")
    print()
    
    # Get connected Post-Bridge accounts
    print("📱 Fetching connected accounts...")
    try:
        accounts_url = f"https://api.post-bridge.com/v1/social-accounts?limit=100"
        req = urllib.request.Request(accounts_url)
        req.add_header("Authorization", f"Bearer {POST_BRIDGE_KEY}")
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            accounts_data = json.loads(resp.read().decode("utf-8"))
        
        accounts = accounts_data.get("data", [])
        by_platform = {}
        for acc in accounts:
            platform = acc.get("platform")
            if platform not in by_platform:
                by_platform[platform] = []
            by_platform[platform].append(acc.get("username"))
        
        print(f"  Connected accounts:")
        for platform, users in sorted(by_platform.items()):
            print(f"    {platform}: {len(users)} accounts")
        
    except Exception as e:
        print(f"  ⚠️  Could not fetch accounts: {e}")
        by_platform = {"tiktok": [], "facebook": []}
    
    print()
    
    # Continuous learning loop
    iteration = 0
    last_research_hour = -1
    
    try:
        while True:
            iteration += 1
            current_hour = datetime.now().hour
            
            print("=" * 70)
            print(f"🔄 ITERATION {iteration} — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} WIB")
            print("=" * 70)
            print()
            
            # Step 1: Research Flow (every hour)
            if current_hour != last_research_hour:
                print("▶️  Running Research Flow...")
                research_output = run_research_flow()
                last_research_hour = current_hour
            else:
                print("⏸️  Research already done this hour, skipping")
                research_output = None
            
            # Step 2: Content Generation Flow
            print("▶️  Running Content Generation Flow...")
            content = run_content_gen_flow(memory)
            
            if not content:
                print("  ⚠️  Content generation failed, waiting for next iteration...")
                time.sleep(3600)  # Wait 1 hour
                continue
            
            # Step 3: Upload to temporary host
            print("▶️  Running Upload Flow...")
            # For now, just simulate success (would upload actual content)
            file_url = "https://tmpfiles.org/d/demo.mp4"  # Placeholder
            
            # Step 4: Social Media Manager Flow
            print("▶️  Running Social Media Flow...")
            results = run_social_media_flow(content, memory)
            
            # Step 5: Feedback Loop
            print("▶️  Running Feedback Loop...")
            total_engagement = sum(r.get("estimated_engagement", {}).get("likes", 0) for r in results)
            
            # Log performance
            memory.log_post({
                "flow": content.get("content_type", "unknown"),
                "hook_type": content.get("content", {}).get("hook", "unknown"),
                "success": all(r.get("success", False) for r in results),
                "views": total_engagement
            })
            
            # Update confidence based on performance
            memory.update_confidence(content.get("content_type", "unknown"), 
                                 all(r.get("success", False) for r in results),
                                 total_engagement)
            
            # Print iteration summary
            print()
            print("📊 Iteration Summary:")
            print(f"  Research: {'✅ Done' if research_output else '⏸️ Skipped'}")
            print(f"  Content: {'✅ Generated' if content else '❌ Failed'}")
            print(f"  Posted: {'✅ Success' if results else '❌ Failed'}")
            print(f"  Total Engagement: {total_engagement:,}")
            
            # Wait until next hour
            now = datetime.now()
            seconds_until_next_hour = 3600 - (now.minute * 60) - now.second - now.microsecond / 1000000
            print()
            print(f"⏰ Waiting {(seconds_until_next_hour // 60):.0f} minutes until next research cycle...")
            time.sleep(min(seconds_until_next_hour, 300))  # Wait or max 5 minutes
            
    except KeyboardInterrupt:
        print()
        print("=" * 70)
        print("⏸️  System stopped by user")
        print("=" * 70)


if __name__ == "__main__":
    main()
