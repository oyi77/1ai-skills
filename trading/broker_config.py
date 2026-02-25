"""
Cross-platform broker configuration for trading skills.

Auto-detects platform and provides appropriate broker paths.
Supports Windows (direct MT5), Linux (Docker/Wine), and macOS.
"""

import os
import sys
import platform
from pathlib import Path
from typing import Optional, Dict, Any
import json


class BrokerConfig:
    """Cross-platform broker configuration."""

    # Default MT5 paths by platform
    MT5_PATHS = {
        "windows": [
            r"C:\Program Files\MetaTrader 5\terminal64.exe",
            r"C:\Program Files (x86)\MetaTrader 5\terminal64.exe",
            r"C:\Program Files\MetaTrader 4\terminal64.exe",
            r"C:\Program Files (x86)\MetaTrader 4\terminal64.exe",
        ],
        "linux": [
            # Docker-based MT5 (mt5linux)
            "/opt/mt5linux/terminal64",
            "/usr/local/bin/mt5terminal",
            # Wine-based (less reliable)
            os.path.expanduser(
                "~/.wine/drive_c/Program Files/MetaTrader 5/terminal64.exe"
            ),
        ],
        "darwin": [
            "/Applications/MetaTrader 5.app/Contents/SharedSupport/terminal",
            "/Applications/MetaTrader 4.app/Contents/SharedSupport/terminal",
            os.path.expanduser("~/MetaTrader5/terminal"),
        ],
    }

    # Docker configuration for Linux
    DOCKER_MT5_IMAGE = "ghcr.io/eycm/MT5-Docker:latest"
    DOCKER_MT5_CONTAINER_NAME = "mt5-trading"

    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize broker configuration.

        Args:
            config_dir: Optional custom config directory.
                       Defaults to ~/.openclaw/trading-config/
        """
        if config_dir is None:
            config_dir = Path.home() / ".openclaw" / "trading-config"

        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / "brokers.json"
        self._config: Dict[str, Any] = {}
        self._platform = platform.system().lower()

        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    self._config = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._config = {}

    def _save_config(self) -> None:
        """Save configuration to file."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "w") as f:
            json.dump(self._config, f, indent=2)

    @property
    def platform(self) -> str:
        """Get current platform."""
        return self._platform

    def get_mt5_path(self, broker: str = "default") -> Optional[str]:
        """
        Get MT5 terminal path for the current platform.

        Args:
            broker: Optional broker-specific path key.

        Returns:
            Path to MT5 terminal if found, None otherwise.
        """
        # Check broker-specific config first
        if broker in self._config.get("mt5_paths", {}):
            path = self._config["mt5_paths"][broker]
            if os.path.exists(path):
                return path

        # Check custom path
        custom_path = self._config.get("custom_mt5_path")
        if custom_path and os.path.exists(custom_path):
            return custom_path

        # Auto-detect from default paths
        for path in self.MT5_PATHS.get(self._platform, []):
            if os.path.exists(path):
                return path

        # Try to find MT5 in common locations
        return self._find_mt5_in_common_locations()

    def _find_mt5_in_common_locations(self) -> Optional[str]:
        """Try to find MT5 in common installation locations."""
        # Linux: check if Docker container is running
        if self._platform == "linux":
            import subprocess

            try:
                result = subprocess.run(
                    ["docker", "ps", "--format", "{{.Names}}"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if self.DOCKER_MT5_CONTAINER_NAME in result.stdout:
                    # MT5 is running in Docker
                    return "docker:" + self.DOCKER_MT5_CONTAINER_NAME
            except (subprocess.SubprocessError, FileNotFoundError):
                pass

        return None

    def set_mt5_path(self, path: str, broker: str = "default") -> None:
        """
        Set custom MT5 path.

        Args:
            path: Path to MT5 terminal.
            broker: Optional broker-specific identifier.
        """
        if "mt5_paths" not in self._config:
            self._config["mt5_paths"] = {}

        self._config["mt5_paths"][broker] = path
        self._save_config()

    def set_docker_config(self, image: str = None, container: str = None) -> None:
        """
        Configure Docker-based MT5 for Linux.

        Args:
            image: Docker image name.
            container: Container name.
        """
        if "docker" not in self._config:
            self._config["docker"] = {}

        if image:
            self._config["docker"]["image"] = image
        if container:
            self._config["docker"]["container"] = container

        self._save_config()

    def is_docker_mode(self) -> bool:
        """Check if running in Docker mode (Linux without native MT5)."""
        if self._platform != "linux":
            return False

        mt5_path = self.get_mt5_path()
        return mt5_path is None or mt5_path.startswith("docker:")

    def get_connection_params(self, broker: str = "default") -> Dict[str, Any]:
        """
        Get connection parameters for a broker.

        Args:
            broker: Broker identifier.

        Returns:
            Dict with connection parameters including:
            - path: MT5 terminal path (or docker container name)
            - is_docker: Whether using Docker
            - platform: Current platform
        """
        mt5_path = self.get_mt5_path(broker)

        params = {
            "platform": self._platform,
            "is_docker": self.is_docker_mode(),
            "path": mt5_path,
        }

        # Add Docker-specific params
        if params["is_docker"]:
            docker_config = self._config.get("docker", {})
            params["docker_image"] = docker_config.get("image", self.DOCKER_MT5_IMAGE)
            params["docker_container"] = docker_config.get(
                "container", self.DOCKER_MT5_CONTAINER_NAME
            )

        return params

    def detect_broker(self) -> str:
        """
        Attempt to detect connected broker from MT5 terminal.

        Returns:
            Broker name if detected, "unknown" otherwise.
        """
        # This would require MT5 Python library to be installed
        # and connection to be active
        return "unknown"

    @classmethod
    def get_default_config_example(cls) -> Dict[str, Any]:
        """Get example configuration."""
        return {
            "mt5_paths": {
                "default": "C:\\Program Files\\MetaTrader 5\\terminal64.exe",
                "exness": "C:\\Program Files\\Exness\\MetaTrader5\\terminal64.exe",
            },
            "custom_mt5_path": None,
            "docker": {
                "image": cls.DOCKER_MT5_IMAGE,
                "container": cls.DOCKER_MT5_CONTAINER_NAME,
            },
            "default_broker": "default",
        }


# Convenience function for quick access
_config: Optional[BrokerConfig] = None


def get_broker_config() -> BrokerConfig:
    """Get global broker config instance."""
    global _config
    if _config is None:
        _config = BrokerConfig()
    return _config


if __name__ == "__main__":
    # CLI for testing
    config = BrokerConfig()
    print(f"Platform: {config.platform}")
    print(f"MT5 Path: {config.get_mt5_path()}")
    print(f"Docker Mode: {config.is_docker_mode()}")
    print(f"Connection Params: {config.get_connection_params()}")
