"""
BaseModule — common init pattern for all Content Kingdom modules.
Dependency Inversion: every module receives config dict, not a file path.
Caller loads config; modules stay testable without filesystem.
"""

import json
import os

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    "../../../../content-kingdom/config.json",
)


def load_config(path: str = CONFIG_PATH) -> dict:
    """Load and return config dict. Raises FileNotFoundError if missing."""
    with open(os.path.abspath(path)) as f:
        return json.load(f)


class BaseModule:
    """Shared base: stores config, exposes platform limits helper."""

    def __init__(self, config: dict):
        self.config = config

    def platform_cfg(self, platform: str) -> dict:
        return self.config.get("platforms", {}).get(platform, {})
