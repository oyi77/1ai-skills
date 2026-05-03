"""
Cost Tracker Module for budget management.
Tracks API usage costs across different providers.
"""

from datetime import datetime
from typing import Optional


class CostTracker:
    """Tracks API usage costs and budgets across providers."""

    # Default cost per 1K tokens (can be customized per provider)
    DEFAULT_COSTS = {
        "openai": {
            "prompt": 0.0015,  # $1.50 per 1M tokens
            "completion": 0.002,  # $2.00 per 1M tokens
        },
        "anthropic": {
            "prompt": 0.0015,  # $1.50 per 1M tokens
            "completion": 0.002,  # $2.00 per 1M tokens
        },
        "google": {
            "prompt": 0.00025,  # $0.25 per 1M tokens
            "completion": 0.0005,  # $0.50 per 1M tokens
        },
    }

    def __init__(
        self, monthly_budget: float = 100.0, provider_costs: Optional[dict] = None
    ):
        """
        Initialize the CostTracker.

        Args:
            monthly_budget: Maximum budget for the month in dollars
            provider_costs: Optional custom costs per provider
        """
        self.monthly_budget = monthly_budget
        self.provider_costs = provider_costs or self.DEFAULT_COSTS
        self._usage: dict = {}  # {provider: {"prompt_tokens": int, "completion_tokens": int, "cost": float}}
        self._total_cost: float = 0.0
        self._current_month: str = datetime.now().strftime("%Y-%m")

    def log_cost(
        self,
        provider: str,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        custom_cost: Optional[float] = None,
    ) -> float:
        """
        Record API usage and calculate cost.

        Args:
            provider: Provider name (e.g., 'openai', 'anthropic')
            prompt_tokens: Number of prompt tokens used
            completion_tokens: Number of completion tokens used
            custom_cost: Optional custom cost override

        Returns:
            The cost for this API call
        """
        if provider not in self._usage:
            self._usage[provider] = {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "cost": 0.0,
            }

        if custom_cost is not None:
            cost = custom_cost
        else:
            prompt_cost = (prompt_tokens / 1_000_000) * self.provider_costs.get(
                provider, {}
            ).get("prompt", 0)
            completion_cost = (completion_tokens / 1_000_000) * self.provider_costs.get(
                provider, {}
            ).get("completion", 0)
            cost = prompt_cost + completion_cost

        self._usage[provider]["prompt_tokens"] += prompt_tokens
        self._usage[provider]["completion_tokens"] += completion_tokens
        self._usage[provider]["cost"] += cost
        self._total_cost += cost

        return cost

    def get_total_cost(self) -> float:
        """Get the total cost for the current billing period."""
        return self._total_cost

    def get_provider_cost(self, provider: str) -> float:
        """Get the total cost for a specific provider."""
        return self._usage.get(provider, {}).get("cost", 0.0)

    def get_all_usage(self) -> dict:
        """Get detailed usage breakdown for all providers."""
        return self._usage.copy()

    def check_limit(self) -> tuple[bool, float]:
        """
        Check if current spending is within budget.

        Returns:
            Tuple of (is_under_budget, remaining_budget)
        """
        remaining = self.monthly_budget - self._total_cost
        return (remaining > 0, remaining)

    def get_budget_status(self) -> dict:
        """Get detailed budget status."""
        is_under, remaining = self.check_limit()
        percent_used = (
            (self._total_cost / self.monthly_budget * 100)
            if self.monthly_budget > 0
            else 0
        )

        return {
            "total_cost": self._total_cost,
            "monthly_budget": self.monthly_budget,
            "remaining_budget": remaining,
            "percent_used": percent_used,
            "is_under_budget": is_under,
            "current_month": self._current_month,
        }

    def reset_monthly(self) -> None:
        """Reset the tracker for a new billing month."""
        self._usage = {}
        self._total_cost = 0.0
        self._current_month = datetime.now().strftime("%Y-%m")

    def should_reset(self) -> bool:
        """Check if the tracker should be reset for a new month."""
        current_month = datetime.now().strftime("%Y-%m")
        return current_month != self._current_month

    def auto_reset_if_needed(self) -> bool:
        """
        Automatically reset if a new month has started.

        Returns:
            True if reset was performed, False otherwise
        """
        if self.should_reset():
            self.reset_monthly()
            return True
        return False
