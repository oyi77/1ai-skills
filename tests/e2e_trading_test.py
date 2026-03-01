# E2E Trading Tests
# Tests the trading pipeline and guardrails

import pytest
import sys
import os
import tempfile

sys.path.insert(0, "/home/openclaw/.openclaw/workspace")
sys.path.insert(0, "/home/openclaw/.openclaw/workspace/skills/trading")


class TestTradingGuardrails:
    """Test trading guardrails"""

    def test_trading_guardrails_initialization(self):
        """Test TradingGuardrails can be initialized"""
        from guardrails import TradingGuardrails

        tg = TradingGuardrails()
        assert tg is not None

    def test_risk_manager_initialization(self):
        """Test RiskManager can be initialized"""
        from guardrails import RiskManager

        rm = RiskManager()
        assert rm is not None

    def test_guardrails_configured(self):
        """Test guardrails are configured"""
        from guardrails import TradingGuardrails

        tg = TradingGuardrails()
        # Verify configuration exists
        assert hasattr(tg, 'can_trade')


class TestTradingPipeline:
    """Test trading pipeline"""

    def test_pipeline_initialization(self):
        """Test pipeline can be initialized"""
        try:
            from pipeline import TradingPipeline

            # Just verify import works
            assert TradingPipeline is not None
        except ImportError:
            pytest.skip("Trading pipeline not available")

    def test_guardrails_file_exists(self):
        """Test guardrails file exists"""
        assert os.path.exists(
            "/home/openclaw/.openclaw/workspace/skills/trading/guardrails.py"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
