#!/usr/bin/env python3
"""
E2E Content Pipeline Test
Tests the full content pipeline: research → generate → approve → (mock) post.
Runs 3 complete pipeline executions, validates guardrails, records pass/fail per stage.
"""

import json
import os
import sys
import time
import tempfile
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional
from unittest.mock import patch, MagicMock

import pytest

# Add workspace to path
workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, workspace_root)


# ── Pipeline Components (self-contained for E2E isolation) ────────────────────


class RateLimiter:
    """Enforces rate limits on content posting."""

    def __init__(self, max_posts_per_hour: int = 5, max_posts_per_day: int = 20):
        self.max_per_hour = max_posts_per_hour
        self.max_per_day = max_posts_per_day
        self.post_timestamps: List[datetime] = []

    def can_post(self) -> bool:
        """Check if posting is allowed under rate limits."""
        now = datetime.now(timezone.utc)
        one_hour_ago = now - timedelta(hours=1)
        one_day_ago = now - timedelta(days=1)

        recent_hour = [t for t in self.post_timestamps if t > one_hour_ago]
        recent_day = [t for t in self.post_timestamps if t > one_day_ago]

        return (
            len(recent_hour) < self.max_per_hour and len(recent_day) < self.max_per_day
        )

    def record_post(self):
        """Record a post timestamp."""
        self.post_timestamps.append(datetime.now(timezone.utc))

    def get_usage(self) -> Dict[str, int]:
        """Get current rate limit usage."""
        now = datetime.now(timezone.utc)
        one_hour_ago = now - timedelta(hours=1)
        one_day_ago = now - timedelta(days=1)

        return {
            "hourly": len([t for t in self.post_timestamps if t > one_hour_ago]),
            "daily": len([t for t in self.post_timestamps if t > one_day_ago]),
            "max_hourly": self.max_per_hour,
            "max_daily": self.max_per_day,
        }


class ApprovalQueue:
    """Content approval gate with guardrails."""

    BLOCKED_WORDS = [
        "guaranteed",
        "100% profit",
        "get rich quick",
        "free money",
        "no risk",
        "pyramid",
        "ponzi",
        "scam",
    ]

    MIN_CAPTION_LENGTH = 20
    MAX_CAPTION_LENGTH = 2200  # TikTok limit
    MAX_HASHTAGS = 30
    REQUIRED_FIELDS = ["hook", "caption", "content_type", "platforms"]

    def validate(self, content: dict) -> Dict[str, any]:
        """Validate content against guardrails. Returns {approved, reasons}."""
        reasons = []

        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in content:
                reasons.append(f"Missing required field: {field}")

        caption = content.get("caption", "")

        # Caption length
        if len(caption) < self.MIN_CAPTION_LENGTH:
            reasons.append(
                f"Caption too short ({len(caption)} < {self.MIN_CAPTION_LENGTH})"
            )
        if len(caption) > self.MAX_CAPTION_LENGTH:
            reasons.append(
                f"Caption too long ({len(caption)} > {self.MAX_CAPTION_LENGTH})"
            )

        # Blocked words
        caption_lower = caption.lower()
        for word in self.BLOCKED_WORDS:
            if word in caption_lower:
                reasons.append(f"Blocked word detected: '{word}'")

        # Hashtag count
        hashtag_count = caption.count("#")
        if hashtag_count > self.MAX_HASHTAGS:
            reasons.append(f"Too many hashtags ({hashtag_count} > {self.MAX_HASHTAGS})")

        # Confidence threshold
        confidence = content.get("confidence", 0)
        if confidence < 0.3:
            reasons.append(f"Confidence too low ({confidence} < 0.3)")

        return {
            "approved": len(reasons) == 0,
            "reasons": reasons,
            "content_id": content.get("id", "unknown"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


class ContentPipeline:
    """Full content pipeline: research → generate → approve → post."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.research_dir = output_dir / "research"
        self.content_dir = output_dir / "content"
        self.results_dir = output_dir / "results"
        self.rate_limiter = RateLimiter(max_posts_per_hour=5, max_posts_per_day=20)
        self.approval_queue = ApprovalQueue()

        for d in [self.research_dir, self.content_dir, self.results_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def stage_research(self, niche: str = "motivation") -> Dict:
        """Stage 1: Research trending content and hooks."""
        research = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "niche": niche,
            "trending_topics": self._get_trending_topics(niche),
            "viral_hooks": self._get_viral_hooks(niche),
            "winning_formulas": self._get_winning_formulas(niche),
            "confidence": self._calculate_research_confidence(niche),
        }

        # Persist research
        research_file = (
            self.research_dir
            / f"research_{niche}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(research_file, "w") as f:
            json.dump(research, f, indent=2)

        return research

    def stage_generate(self, research: Dict) -> Dict:
        """Stage 2: Generate content based on research."""
        niche = research.get("niche", "motivation")
        hooks = research.get("viral_hooks", [])
        hook = hooks[0] if hooks else "Default motivational hook"

        content = {
            "id": f"content_{niche}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "hook": hook,
            "caption": self._generate_caption(niche, hook),
            "content_type": "slideshow",
            "platforms": ["tiktok"],
            "confidence": research.get("confidence", 0.5),
            "based_on_research": research.get("timestamp", ""),
            "niche": niche,
            "estimated_views": self._estimate_views(research.get("confidence", 0.5)),
        }

        # Persist content
        content_file = self.content_dir / f"{content['id']}.json"
        with open(content_file, "w") as f:
            json.dump(content, f, indent=2)

        return content

    def stage_approve(self, content: Dict) -> Dict:
        """Stage 3: Run content through approval guardrails."""
        result = self.approval_queue.validate(content)
        result["content"] = content
        return result

    def stage_post(self, approved_content: Dict) -> Dict:
        """Stage 4: Mock post to platforms (never posts to real TikTok)."""
        content = approved_content.get("content", {})

        # Rate limit check
        if not self.rate_limiter.can_post():
            return {
                "success": False,
                "error": "Rate limit exceeded",
                "rate_usage": self.rate_limiter.get_usage(),
            }

        # Mock posting — simulate success
        platforms = content.get("platforms", ["tiktok"])
        post_results = []

        for platform in platforms:
            post_result = {
                "platform": platform,
                "success": True,
                "post_id": f"mock_{platform}_{datetime.now().strftime('%H%M%S')}",
                "caption": content.get("caption", "")[:100],
                "mock": True,  # Always mock — never real
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            post_results.append(post_result)

        self.rate_limiter.record_post()

        return {
            "success": True,
            "platforms_posted": len(post_results),
            "results": post_results,
            "rate_usage": self.rate_limiter.get_usage(),
        }

    def run_full_pipeline(self, niche: str = "motivation") -> Dict:
        """Execute complete pipeline: research → generate → approve → post."""
        stages = {}
        pipeline_start = time.time()

        # Stage 1: Research
        try:
            research = self.stage_research(niche)
            stages["research"] = {"success": True, "data": research}
        except Exception as e:
            stages["research"] = {"success": False, "error": str(e)}
            return self._finalize_result(stages, pipeline_start, niche)

        # Stage 2: Generate
        try:
            content = self.stage_generate(research)
            stages["generate"] = {"success": True, "data": content}
        except Exception as e:
            stages["generate"] = {"success": False, "error": str(e)}
            return self._finalize_result(stages, pipeline_start, niche)

        # Stage 3: Approve
        try:
            approval = self.stage_approve(content)
            stages["approve"] = {
                "success": approval["approved"],
                "data": approval,
                "reasons": approval.get("reasons", []),
            }
            if not approval["approved"]:
                return self._finalize_result(stages, pipeline_start, niche)
        except Exception as e:
            stages["approve"] = {"success": False, "error": str(e)}
            return self._finalize_result(stages, pipeline_start, niche)

        # Stage 4: Post (mocked)
        try:
            post_result = self.stage_post(approval)
            stages["post"] = {"success": post_result["success"], "data": post_result}
        except Exception as e:
            stages["post"] = {"success": False, "error": str(e)}

        return self._finalize_result(stages, pipeline_start, niche)

    def _finalize_result(self, stages: Dict, start_time: float, niche: str) -> Dict:
        """Build final pipeline result."""
        elapsed = time.time() - start_time
        all_success = all(s.get("success", False) for s in stages.values())

        result = {
            "niche": niche,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "elapsed_seconds": round(elapsed, 3),
            "overall_success": all_success,
            "stages": stages,
            "stages_passed": sum(1 for s in stages.values() if s.get("success")),
            "stages_total": len(stages),
        }

        # Persist result
        result_file = (
            self.results_dir
            / f"result_{niche}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(result_file, "w") as f:
            json.dump(result, f, indent=2, default=str)

        return result

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _get_trending_topics(self, niche: str) -> List[str]:
        topics = {
            "motivation": [
                "morning routines",
                "discipline",
                "growth mindset",
                "5AM club",
            ],
            "money": [
                "passive income",
                "side hustles",
                "investing basics",
                "crypto trends",
            ],
            "beauty": [
                "skincare routines",
                "makeup transformation",
                "glow up",
                "hair care",
            ],
        }
        return topics.get(niche, topics["motivation"])

    def _get_viral_hooks(self, niche: str) -> List[str]:
        hooks = {
            "motivation": [
                "My landlord wouldn't approve this, so I showed them AI's idea",
                "They said it was impossible, so I proved them wrong",
                "Stop waiting for the perfect moment — it doesn't exist",
            ],
            "money": [
                "I stopped buying coffee and invested instead",
                "The #1 money mistake everyone makes",
                "Why your 9-5 is keeping you broke",
            ],
            "beauty": [
                "POV: You finally found the holy grail product",
                "This $5 product changed my entire routine",
                "My dermatologist was SHOCKED by these results",
            ],
        }
        return hooks.get(niche, hooks["motivation"])

    def _get_winning_formulas(self, niche: str) -> Dict:
        return {
            f"{niche}_hook_formula": {
                "confidence": 0.8,
                "avg_views": 100000,
                "description": f"Proven {niche} hook with strong performance",
            }
        }

    def _calculate_research_confidence(self, niche: str) -> float:
        confidence_map = {
            "motivation": 0.85,
            "money": 0.75,
            "beauty": 0.70,
        }
        return confidence_map.get(niche, 0.6)

    def _generate_caption(self, niche: str, hook: str) -> str:
        captions = {
            "motivation": (
                f"{hook} 💪 Every single day is a fresh start. "
                "Stop comparing yourself to others. "
                "#motivation #mindset #success #growth #viral"
            ),
            "money": (
                f"{hook} 💰 The people winning financially started before they were ready. "
                "#money #wealth #entrepreneur #investing"
            ),
            "beauty": (
                f"{hook} ✨ Save this for your next routine! "
                "#beauty #skincare #glowup #viral"
            ),
        }
        return captions.get(niche, captions["motivation"])

    def _estimate_views(self, confidence: float) -> int:
        base = 50000
        return int(base * (confidence * 2))


# ── Test Suite ────────────────────────────────────────────────────────────────


class TestE2EContentPipeline:
    """End-to-end tests for the full content pipeline."""

    @pytest.fixture(autouse=True)
    def setup_teardown(self, tmp_path):
        """Create isolated test directory for each test."""
        self.test_dir = tmp_path / "e2e_content_test"
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.pipeline = ContentPipeline(self.test_dir)
        yield
        # Cleanup handled by tmp_path

    # ── Full Pipeline Runs (3 executions) ─────────────────────────────────────

    def test_full_pipeline_run_1_motivation(self):
        """Run 1: Full pipeline with motivation niche."""
        result = self.pipeline.run_full_pipeline("motivation")

        assert result["overall_success"] is True
        assert result["niche"] == "motivation"
        assert result["stages_passed"] == 4
        assert result["stages_total"] == 4

        # Verify each stage passed
        assert result["stages"]["research"]["success"] is True
        assert result["stages"]["generate"]["success"] is True
        assert result["stages"]["approve"]["success"] is True
        assert result["stages"]["post"]["success"] is True

        # Verify post is mocked
        post_data = result["stages"]["post"]["data"]
        assert post_data["results"][0]["mock"] is True

    def test_full_pipeline_run_2_money(self):
        """Run 2: Full pipeline with money niche."""
        result = self.pipeline.run_full_pipeline("money")

        assert result["overall_success"] is True
        assert result["niche"] == "money"
        assert result["stages_passed"] == 4

        # Verify content was generated correctly
        content = result["stages"]["generate"]["data"]
        assert "money" in content["caption"].lower() or "💰" in content["caption"]
        assert content["confidence"] > 0

    def test_full_pipeline_run_3_beauty(self):
        """Run 3: Full pipeline with beauty niche."""
        result = self.pipeline.run_full_pipeline("beauty")

        assert result["overall_success"] is True
        assert result["niche"] == "beauty"
        assert result["stages_passed"] == 4

        # Verify platform targeting
        content = result["stages"]["generate"]["data"]
        assert "tiktok" in content["platforms"]

    # ── Stage-Level Tests ─────────────────────────────────────────────────────

    def test_research_stage_output(self):
        """Test research stage produces valid output."""
        research = self.pipeline.stage_research("motivation")

        assert "timestamp" in research
        assert "niche" in research
        assert "trending_topics" in research
        assert "viral_hooks" in research
        assert "winning_formulas" in research
        assert "confidence" in research

        assert len(research["trending_topics"]) > 0
        assert len(research["viral_hooks"]) > 0
        assert 0 < research["confidence"] <= 1.0

    def test_generate_stage_output(self):
        """Test content generation stage produces valid output."""
        research = self.pipeline.stage_research("motivation")
        content = self.pipeline.stage_generate(research)

        assert "id" in content
        assert "hook" in content
        assert "caption" in content
        assert "content_type" in content
        assert "platforms" in content
        assert "confidence" in content
        assert content["content_type"] == "slideshow"
        assert len(content["caption"]) >= 20

    def test_approve_stage_accepts_valid_content(self):
        """Test approval stage accepts properly structured content."""
        research = self.pipeline.stage_research("motivation")
        content = self.pipeline.stage_generate(research)
        approval = self.pipeline.stage_approve(content)

        assert approval["approved"] is True
        assert len(approval["reasons"]) == 0

    def test_post_stage_is_mocked(self):
        """Test post stage never posts to real TikTok."""
        research = self.pipeline.stage_research("motivation")
        content = self.pipeline.stage_generate(research)
        approval = self.pipeline.stage_approve(content)
        post_result = self.pipeline.stage_post(approval)

        assert post_result["success"] is True
        for platform_result in post_result["results"]:
            assert platform_result["mock"] is True
            assert platform_result["post_id"].startswith("mock_")

    # ── Guardrail Tests ───────────────────────────────────────────────────────

    def test_guardrail_rejects_blocked_words(self):
        """Test approval rejects content with blocked words."""
        content = {
            "hook": "guaranteed money",
            "caption": "Get rich quick with this guaranteed method! No risk at all!",
            "content_type": "slideshow",
            "platforms": ["tiktok"],
            "confidence": 0.8,
        }
        result = self.pipeline.approval_queue.validate(content)

        assert result["approved"] is False
        assert any("Blocked word" in r for r in result["reasons"])

    def test_guardrail_rejects_short_caption(self):
        """Test approval rejects captions that are too short."""
        content = {
            "hook": "Short",
            "caption": "Too short",
            "content_type": "slideshow",
            "platforms": ["tiktok"],
            "confidence": 0.8,
        }
        result = self.pipeline.approval_queue.validate(content)

        assert result["approved"] is False
        assert any("too short" in r for r in result["reasons"])

    def test_guardrail_rejects_missing_fields(self):
        """Test approval rejects content missing required fields."""
        content = {"caption": "This is a valid caption that is long enough"}
        result = self.pipeline.approval_queue.validate(content)

        assert result["approved"] is False
        assert any("Missing required field" in r for r in result["reasons"])

    def test_guardrail_rejects_low_confidence(self):
        """Test approval rejects content with very low confidence."""
        content = {
            "hook": "Low confidence hook",
            "caption": "This content has very low confidence score applied to it",
            "content_type": "slideshow",
            "platforms": ["tiktok"],
            "confidence": 0.1,
        }
        result = self.pipeline.approval_queue.validate(content)

        assert result["approved"] is False
        assert any("Confidence too low" in r for r in result["reasons"])

    def test_guardrail_rejects_too_many_hashtags(self):
        """Test approval rejects content with excessive hashtags."""
        hashtags = " ".join([f"#{i}tag" for i in range(35)])
        content = {
            "hook": "Too many hashtags",
            "caption": f"Content with too many hashtags {hashtags}",
            "content_type": "slideshow",
            "platforms": ["tiktok"],
            "confidence": 0.8,
        }
        result = self.pipeline.approval_queue.validate(content)

        assert result["approved"] is False
        assert any("Too many hashtags" in r for r in result["reasons"])

    # ── Rate Limiter Tests ────────────────────────────────────────────────────

    def test_rate_limiter_allows_under_limit(self):
        """Test rate limiter allows posts under the limit."""
        assert self.pipeline.rate_limiter.can_post() is True

    def test_rate_limiter_blocks_over_hourly_limit(self):
        """Test rate limiter blocks when hourly limit exceeded."""
        limiter = RateLimiter(max_posts_per_hour=3, max_posts_per_day=20)
        for _ in range(3):
            limiter.record_post()

        assert limiter.can_post() is False

    def test_rate_limiter_blocks_over_daily_limit(self):
        """Test rate limiter blocks when daily limit exceeded."""
        limiter = RateLimiter(max_posts_per_hour=100, max_posts_per_day=3)
        for _ in range(3):
            limiter.record_post()

        assert limiter.can_post() is False

    def test_rate_limiter_reports_usage(self):
        """Test rate limiter correctly reports usage."""
        self.pipeline.rate_limiter.record_post()
        self.pipeline.rate_limiter.record_post()
        usage = self.pipeline.rate_limiter.get_usage()

        assert usage["hourly"] == 2
        assert usage["daily"] == 2
        assert usage["max_hourly"] == 5
        assert usage["max_daily"] == 20

    def test_pipeline_respects_rate_limit(self):
        """Test full pipeline stops posting when rate limited."""
        # Exhaust the rate limit
        limiter = RateLimiter(max_posts_per_hour=2, max_posts_per_day=20)
        self.pipeline.rate_limiter = limiter

        # Run pipelines until rate limited
        results = []
        for niche in ["motivation", "money", "beauty"]:
            result = self.pipeline.run_full_pipeline(niche)
            results.append(result)

        # First 2 should succeed, 3rd should fail at post stage
        assert results[0]["stages"]["post"]["success"] is True
        assert results[1]["stages"]["post"]["success"] is True
        assert results[2]["stages"]["post"]["success"] is False
        assert "Rate limit" in results[2]["stages"]["post"]["data"].get("error", "")

    # ── Result Persistence Tests ──────────────────────────────────────────────

    def test_research_files_persisted(self):
        """Test research output is saved to disk."""
        self.pipeline.stage_research("motivation")
        research_files = list(self.pipeline.research_dir.glob("research_*.json"))
        assert len(research_files) >= 1

    def test_content_files_persisted(self):
        """Test content output is saved to disk."""
        research = self.pipeline.stage_research("motivation")
        self.pipeline.stage_generate(research)
        content_files = list(self.pipeline.content_dir.glob("content_*.json"))
        assert len(content_files) >= 1

    def test_result_files_persisted(self):
        """Test pipeline results are saved to disk."""
        self.pipeline.run_full_pipeline("motivation")
        result_files = list(self.pipeline.results_dir.glob("result_*.json"))
        assert len(result_files) >= 1

    def test_persisted_results_are_valid_json(self):
        """Test that persisted result files contain valid JSON."""
        self.pipeline.run_full_pipeline("motivation")
        result_files = list(self.pipeline.results_dir.glob("result_*.json"))

        for rf in result_files:
            with open(rf) as f:
                data = json.load(f)
            assert "overall_success" in data
            assert "stages" in data


class TestE2EThreeRuns:
    """Run 3 sequential pipeline executions and record aggregate results."""

    @pytest.fixture(autouse=True)
    def setup_teardown(self, tmp_path):
        """Create isolated test directory."""
        self.test_dir = tmp_path / "e2e_three_runs"
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.pipeline = ContentPipeline(self.test_dir)
        yield

    def test_three_sequential_runs(self):
        """Execute 3 full pipeline runs and verify all pass."""
        niches = ["motivation", "money", "beauty"]
        results = []

        for i, niche in enumerate(niches):
            result = self.pipeline.run_full_pipeline(niche)
            results.append(result)

            # Print run status
            status = "PASS" if result["overall_success"] else "FAIL"
            print(f"\n  Run {i + 1}/3 [{niche}]: {status}")
            for stage_name, stage_data in result["stages"].items():
                stage_status = "✅" if stage_data["success"] else "❌"
                print(f"    {stage_status} {stage_name}")

        # All 3 runs should succeed
        for i, result in enumerate(results):
            assert result["overall_success"] is True, (
                f"Run {i + 1} ({result['niche']}) failed: "
                f"{json.dumps(result['stages'], indent=2, default=str)}"
            )

        # All should have 4 stages
        for result in results:
            assert result["stages_total"] == 4
            assert result["stages_passed"] == 4

    def test_three_runs_with_result_recording(self):
        """Execute 3 runs and persist aggregate results report."""
        niches = ["motivation", "money", "beauty"]
        run_results = []

        for niche in niches:
            result = self.pipeline.run_full_pipeline(niche)
            run_results.append(
                {
                    "run": len(run_results) + 1,
                    "niche": niche,
                    "success": result["overall_success"],
                    "stages_passed": result["stages_passed"],
                    "stages_total": result["stages_total"],
                    "elapsed": result["elapsed_seconds"],
                    "stage_details": {
                        name: {"success": data["success"]}
                        for name, data in result["stages"].items()
                    },
                }
            )

        # Write aggregate report
        report = {
            "test_run": "e2e_content_pipeline",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_runs": len(run_results),
            "passed": sum(1 for r in run_results if r["success"]),
            "failed": sum(1 for r in run_results if not r["success"]),
            "results": run_results,
        }

        report_path = self.test_dir / "e2e_report.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        # Validate report
        assert report["total_runs"] == 3
        assert report["passed"] == 3
        assert report["failed"] == 0
        assert report_path.exists()

    def test_three_runs_different_content(self):
        """Verify 3 runs produce distinct content."""
        niches = ["motivation", "money", "beauty"]
        contents = []

        for niche in niches:
            result = self.pipeline.run_full_pipeline(niche)
            content = result["stages"]["generate"]["data"]
            contents.append(content)

        # All captions should be different
        captions = [c["caption"] for c in contents]
        assert len(set(captions)) == 3, "All 3 runs should produce distinct captions"

        # All should target TikTok
        for content in contents:
            assert "tiktok" in content["platforms"]

        # Confidence should vary by niche
        confidences = [c["confidence"] for c in contents]
        assert len(set(confidences)) >= 2, (
            "Different niches should have varying confidence"
        )


class TestApprovalQueueGuardrails:
    """Focused tests for approval queue guardrails enforcement."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.queue = ApprovalQueue()

    def test_valid_content_passes(self):
        """Valid content should be approved."""
        content = {
            "hook": "Amazing transformation",
            "caption": "Check out this incredible transformation! Save for later! #viral #motivation",
            "content_type": "slideshow",
            "platforms": ["tiktok"],
            "confidence": 0.8,
        }
        result = self.queue.validate(content)
        assert result["approved"] is True

    def test_multiple_violations_all_reported(self):
        """Content with multiple violations reports all of them."""
        content = {
            "caption": "Scam!",  # short + blocked word + missing fields
            "confidence": 0.1,
        }
        result = self.queue.validate(content)

        assert result["approved"] is False
        assert len(result["reasons"]) >= 3  # multiple violations

    def test_each_blocked_word_detected(self):
        """Each individual blocked word triggers rejection."""
        for word in ApprovalQueue.BLOCKED_WORDS:
            content = {
                "hook": "Test hook",
                "caption": f"This content contains {word} which should be blocked from posting",
                "content_type": "slideshow",
                "platforms": ["tiktok"],
                "confidence": 0.8,
            }
            result = self.queue.validate(content)
            assert result["approved"] is False, f"Blocked word '{word}' was not caught"

    def test_caption_at_exact_min_length(self):
        """Caption at exact minimum length should pass."""
        content = {
            "hook": "Edge case test",
            "caption": "A" * ApprovalQueue.MIN_CAPTION_LENGTH,
            "content_type": "slideshow",
            "platforms": ["tiktok"],
            "confidence": 0.8,
        }
        result = self.queue.validate(content)
        assert result["approved"] is True

    def test_caption_one_under_min_length(self):
        """Caption one char under minimum should fail."""
        content = {
            "hook": "Edge case test",
            "caption": "A" * (ApprovalQueue.MIN_CAPTION_LENGTH - 1),
            "content_type": "slideshow",
            "platforms": ["tiktok"],
            "confidence": 0.8,
        }
        result = self.queue.validate(content)
        assert result["approved"] is False


# ── Standalone Runner ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    """Run E2E test outside pytest for quick validation."""
    print("=" * 70)
    print("🧪 E2E CONTENT PIPELINE TEST — 3 Full Runs")
    print("=" * 70)
    print()

    test_dir = Path(tempfile.mkdtemp(prefix="e2e_content_"))
    pipeline = ContentPipeline(test_dir)

    niches = ["motivation", "money", "beauty"]
    all_results = []

    for i, niche in enumerate(niches):
        print(f"{'─' * 70}")
        print(f"🔄 Run {i + 1}/3 — Niche: {niche}")
        print(f"{'─' * 70}")

        result = pipeline.run_full_pipeline(niche)
        all_results.append(result)

        status = "✅ PASS" if result["overall_success"] else "❌ FAIL"
        print(f"  Result: {status}")
        print(f"  Stages: {result['stages_passed']}/{result['stages_total']}")

        for stage_name, stage_data in result["stages"].items():
            icon = "✅" if stage_data["success"] else "❌"
            print(f"    {icon} {stage_name}")
            if not stage_data["success"]:
                error = stage_data.get("error", "")
                reasons = stage_data.get("reasons", [])
                if error:
                    print(f"       Error: {error}")
                if reasons:
                    for r in reasons:
                        print(f"       Reason: {r}")
        print()

    # Summary
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    passed = sum(1 for r in all_results if r["overall_success"])
    failed = len(all_results) - passed
    print(f"  Total: {len(all_results)} | Passed: {passed} | Failed: {failed}")
    print(f"  Results dir: {test_dir}")
    print()

    # Cleanup
    shutil.rmtree(test_dir, ignore_errors=True)

    sys.exit(0 if failed == 0 else 1)
