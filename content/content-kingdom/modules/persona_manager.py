"""
Module 1: PersonaManager
Brand voice, persona selection, caption generation, consistency checks.

Dual init: accepts either a pre-loaded config dict OR a config_path string
so both the Orchestrator facade (passes dict) and the root pipeline
(calls PersonaManager(config_path=...)) work without changes.
"""

import random
from typing import Optional

try:
    from .base import BaseModule, load_config
except ImportError:
    import sys, os

    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from base_module import BaseModule

    def load_config(p):
        import json

        return json.load(open(p))


class PersonaManager(BaseModule):

    def __init__(
        self, config: Optional[dict] = None, config_path: Optional[str] = None
    ):
        if config is None:
            config = load_config(config_path) if config_path else load_config()
        super().__init__(config)
        self._sync()

    def _sync(self):
        self.personas = {p["id"]: p for p in self.config.get("personas", [])}
        self.products = {p["id"]: p for p in self.config.get("products", [])}

    def load(self) -> dict:
        """Re-sync from config (useful after hot-reload)."""
        self._sync()
        return self.config

    def get_persona(self, persona_id: str) -> Optional[dict]:
        return self.personas.get(persona_id)

    def list_personas(self) -> list:
        return list(self.personas.keys())

    def generate_caption(
        self,
        product_id: str,
        persona_id: str,
        platform: str = "tiktok",
        style: str = "hook",
    ) -> str:
        """
        style: hook | story | cta | educational
        """
        persona = self.personas.get(persona_id)
        if not persona:
            raise ValueError(f"Persona not found: {persona_id}")
        product = self.products.get(product_id)
        if not product:
            raise ValueError(f"Product not found: {product_id}")

        hook = random.choice(product.get("hooks", [product["name"]]))
        pain = random.choice(product.get("pain_points", ["masalah ini"]))
        sig = persona.get("signature", "")
        tags = "#AI #DigitalProduct #Bisnis #Indonesia #JENDRALBOT"
        url = product.get("url", "")
        label = product.get("price_label", "FREE")

        templates = {
            "hook": f"{hook}\n\n✅ {product['name']} — {label}\n🔗 {url}\n\n{tags}\n\n{sig}",
            "story": f"Dulu aku juga pernah {pain}...\n\nSampai ketemu {product['name']} 🔥\n\n👉 {label} — {url}\n\n{tags}\n\n{sig}",
            "cta": f"⚡ JANGAN SKIP!\n\n{product['name']} — {label}\n\n{hook}\n\n🔥 {url}\n\n{tags}\n\n{sig}",
            "educational": f"{hook}\n\n💡 {product['name']} ({label})\n🔗 {url}\n\n{tags}\n\n{sig}",
        }
        return templates.get(style, templates["hook"])

    def check_consistency(self, caption: str, persona_id: str) -> dict:
        """
        Score caption against persona voice.
        Returns: {score (0-10), issues, suggestions, consistent}
        """
        persona = self.personas.get(persona_id)
        if not persona:
            return {
                "score": 0,
                "issues": [f"Unknown persona: {persona_id}"],
                "suggestions": [],
                "consistent": False,
            }

        issues, suggestions = [], []
        score = 10.0

        if len(caption) < 50:
            issues.append("Caption too short (< 50 chars)")
            score -= 2

        ctas = ["link", "klik", "daftar", "beli", "coba", "👉", "🔗", "bio"]
        if not any(c in caption.lower() for c in ctas):
            issues.append("Missing CTA")
            suggestions.append("Add a link or call-to-action")
            score -= 1.5

        if "#" not in caption:
            issues.append("No hashtags")
            suggestions.append("Add hashtags for discoverability")
            score -= 1.5

        sig = persona.get("signature", "")
        if sig and sig not in caption:
            suggestions.append(f"Add persona signature: {sig[:40]}")

        return {
            "score": round(max(0.0, score), 1),
            "issues": issues,
            "suggestions": suggestions,
            "persona": persona["name"],
            "consistent": score >= 7.0,
        }
