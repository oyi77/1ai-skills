"""
Module 10 (support): Orchestrator
Ties all Content Kingdom modules together.
Loads config once; instantiates modules on demand (lazy).
"""

import logging
from typing import Optional
from .base import load_config, BaseModule

logger = logging.getLogger("content_kingdom.orchestrator")


class Orchestrator:
    """
    Single entry-point for the Content Kingdom system.

    Usage:
        ck = Orchestrator()          # loads config from default path
        ck = Orchestrator(config)    # pass pre-loaded config dict

    Modules are lazy-loaded to keep startup fast.
    """

    def __init__(
        self, config: Optional[dict] = None, config_path: Optional[str] = None
    ):
        self.config = (
            config or load_config(config_path)
            if config_path
            else config or load_config()
        )
        self._modules = {}

    # ── Lazy module accessors ──────────────────────────────────────────────

    @property
    def persona(self):
        if "persona" not in self._modules:
            from .persona_manager import PersonaManager

            self._modules["persona"] = PersonaManager(self.config)
        return self._modules["persona"]

    @property
    def planner(self):
        if "planner" not in self._modules:
            from .content_planner import ContentPlanner

            self._modules["planner"] = ContentPlanner(self.config)
        return self._modules["planner"]

    @property
    def gate(self):
        if "gate" not in self._modules:
            from .quality_gate import QualityGate

            self._modules["gate"] = QualityGate(self.config)
        return self._modules["gate"]

    @property
    def analytics(self):
        if "analytics" not in self._modules:
            from .analytics_engine import AnalyticsEngine

            self._modules["analytics"] = AnalyticsEngine(
                self.config, self._modules.get("publisher")
            )
        return self._modules["analytics"]

    @property
    def comments(self):
        if "comments" not in self._modules:
            from .comment_manager import CommentManager

            self._modules["comments"] = CommentManager(self.config)
        return self._modules["comments"]

    @property
    def engagement(self):
        if "engagement" not in self._modules:
            from .engagement_engine import EngagementEngine

            self._modules["engagement"] = EngagementEngine(self.config)
        return self._modules["engagement"]

    @property
    def repurposer(self):
        if "repurposer" not in self._modules:
            from .content_repurposer import ContentRepurposer

            self._modules["repurposer"] = ContentRepurposer(self.config)
        return self._modules["repurposer"]

    @property
    def trends(self):
        if "trends" not in self._modules:
            from .trend_scanner import TrendScanner

            self._modules["trends"] = TrendScanner(self.config)
        return self._modules["trends"]

    @property
    def publisher(self):
        if "publisher" not in self._modules:
            from .postbridge_publisher import PostBridgePublisher

            self._modules["publisher"] = PostBridgePublisher(self.config)
        return self._modules["publisher"]

    # ── Status ────────────────────────────────────────────────────────────

    def status(self) -> dict:
        """Return system status: config loaded, modules initialised, API health."""
        loaded = list(self._modules.keys())
        health = None
        if "publisher" in self._modules:
            health = self._modules["publisher"].health_check()
        return {
            "config_loaded": bool(self.config),
            "brand": self.config.get("brand", "unknown"),
            "modules_loaded": loaded,
            "postbridge_health": health,
        }
