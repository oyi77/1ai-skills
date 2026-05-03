"""State management for content generation with resume capability."""

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Any


@dataclass
class GenerationState:
    """Represents the state of a content generation process."""

    state_id: str
    prompt: str
    current_step: int = 0
    step_results: dict[str, Any] = field(default_factory=dict)
    failed_step: Optional[int] = None
    error_message: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Convert state to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GenerationState":
        """Create state from dictionary."""
        return cls(
            state_id=data["state_id"],
            prompt=data["prompt"],
            current_step=data.get("current_step", 0),
            step_results=data.get("step_results", {}),
            failed_step=data.get("failed_step"),
            error_message=data.get("error_message"),
            created_at=data.get("created_at", datetime.now().isoformat()),
            updated_at=data.get("updated_at", datetime.now().isoformat()),
        )


class StateManager:
    """Manages persistence and resume of generation state."""

    def __init__(self, state_dir: str = ".state"):
        """Initialize state manager with directory for state files."""
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def _get_state_path(self, state_id: str) -> Path:
        """Get file path for a state ID."""
        return self.state_dir / f"{state_id}.json"

    def save_state(self, state: GenerationState) -> None:
        """Persist state to disk as JSON."""
        state.updated_at = datetime.now().isoformat()
        state_path = self._get_state_path(state.state_id)
        with open(state_path, "w") as f:
            json.dump(state.to_dict(), f, indent=2)

    def load_state(self, state_id: str) -> Optional[GenerationState]:
        """Restore state from disk. Returns None if not found."""
        state_path = self._get_state_path(state_id)
        if not state_path.exists():
            return None
        with open(state_path, "r") as f:
            data = json.load(f)
        return GenerationState.from_dict(data)

    def resume_generation(self, state_id: str) -> Optional[GenerationState]:
        """Load state and prepare for resuming from failure point."""
        state = self.load_state(state_id)
        if state is None:
            return None

        # Clear failure state to allow continuation
        state.failed_step = None
        state.error_message = None
        return state

    def delete_state(self, state_id: str) -> bool:
        """Delete state file. Returns True if deleted, False if not found."""
        state_path = self._get_state_path(state_id)
        if state_path.exists():
            state_path.unlink()
            return True
        return False

    def list_states(self) -> list[str]:
        """List all available state IDs."""
        return [p.stem for p in self.state_dir.glob("*.json")]
