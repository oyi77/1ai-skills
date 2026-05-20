import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the directory containing pipeline.py to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Mock 'skills' module before it's imported in pipeline.py
mock_skills = MagicMock()
sys.modules["skills"] = mock_skills
sys.modules["skills.trading"] = MagicMock()
sys.modules["skills.trading.guardrails"] = MagicMock()
sys.modules["skills.revenue_dashboard"] = MagicMock()
sys.modules["skills.revenue_dashboard.dashboard"] = MagicMock()

from pipeline import TradingPipeline


@pytest.fixture
def pipeline():
    with patch("pipeline.TradingGuardrails"), patch("pipeline.RevenueDashboard"):
        return TradingPipeline()


def test_check_risk_valid_signal(pipeline):
    signal = {
        "symbol": "EURUSD",
        "direction": "buy",
        "entry": 1.0850,
        "stop_loss": 1.0830,
        "take_profit": 1.0900,
        "size": 0.5,
    }
    result = pipeline._check_risk(signal)
    assert result["valid"] is True


def test_check_risk_exceeds_max_size(pipeline):
    signal = {
        "symbol": "EURUSD",
        "direction": "buy",
        "entry": 1.0850,
        "stop_loss": 1.0830,
        "take_profit": 1.0900,
        "size": 1.5,  # Exceeds max_size = 1.0
    }
    result = pipeline._check_risk(signal)
    assert result["valid"] is False
    assert "exceeds max" in result["reason"]


def test_check_risk_missing_stop_loss(pipeline):
    signal = {
        "symbol": "EURUSD",
        "direction": "buy",
        "entry": 1.0850,
        "take_profit": 1.0900,
        "size": 0.5,
    }
    result = pipeline._check_risk(signal)
    assert result["valid"] is False
    assert "Stop loss required" in result["reason"]


def test_check_risk_boundary_size(pipeline):
    # Boundary case: exactly 1.0
    signal = {
        "symbol": "EURUSD",
        "direction": "buy",
        "entry": 1.0850,
        "stop_loss": 1.0830,
        "take_profit": 1.0900,
        "size": 1.0,
    }
    result = pipeline._check_risk(signal)
    assert result["valid"] is True

    # Boundary case: just over 1.0
    signal["size"] = 1.00001
    result = pipeline._check_risk(signal)
    assert result["valid"] is False
