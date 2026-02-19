"""
Unit tests for Risk Management Module.

Tests all risk calculation methods including:
- Fixed lot sizing
- Risk percent sizing
- Kelly Criterion sizing
- Max drawdown protection
- Portfolio heat calculation
"""

import pytest
from trading.risk.manager import RiskManager, RiskConfig


class TestRiskManager:
    """Test cases for RiskManager class."""

    def setup_method(self):
        """Setup fresh RiskManager for each test."""
        self.config = RiskConfig(
            risk_mode="fixed_risk_percent",
            fixed_lot=0.01,
            risk_percent=1.0,
            rr_ratio=2.0,
            leverage=200,
            max_spread_points=30.0,
            max_drawdown_percent=10.0,
            max_daily_trades=1,
        )
        self.risk_manager = RiskManager(self.config)

    # ========== Fixed Lot Sizing Tests ==========

    def test_calculate_fixed_lot_default(self):
        """Test fixed lot sizing with default config."""
        result = self.risk_manager.calculate_fixed_lot(account_balance=10000)
        assert result == 0.01

    def test_calculate_fixed_lot_custom(self):
        """Test fixed lot sizing with custom lot size."""
        result = self.risk_manager.calculate_fixed_lot(
            account_balance=10000,
            lot_size=0.05
        )
        assert result == 0.05

    def test_calculate_fixed_lot_minimum(self):
        """Test fixed lot sizing enforces minimum."""
        result = self.risk_manager.calculate_fixed_lot(
            account_balance=10000,
            lot_size=0.005  # Below minimum
        )
        assert result == 0.01  # Should be clamped to minimum

    def test_calculate_fixed_lot_rounding(self):
        """Test fixed lot sizing rounds to 2 decimals."""
        result = self.risk_manager.calculate_fixed_lot(
            account_balance=10000,
            lot_size=0.12345
        )
        assert result == 0.12

    # ========== Risk Percent Sizing Tests ==========

    def test_calculate_risk_percent_basic(self):
        """Test risk percent sizing calculation."""
        # With 1% risk on $10,000 = $100 risk
        # Entry: 2000, SL: 1990 = 1000 points (10 / 0.01)
        # Risk = lot_size * 1000 * 0.01 * 100 = $100 * lot_size
        # For $100 risk: lot_size = 100 / (1000 * 0.01 * 100) = 0.1
        result = self.risk_manager.calculate_risk_percent(
            account_balance=10000,
            entry_price=2000.0,
            sl_price=1990.0,
            risk_percent=1.0,
            point_value=0.01,
            contract_size=100,
        )
        assert result == 0.1

    def test_calculate_risk_percent_high_risk(self):
        """Test risk percent sizing with higher risk percentage."""
        # With 2% risk on $10,000 = $200 risk
        result = self.risk_manager.calculate_risk_percent(
            account_balance=10000,
            entry_price=2000.0,
            sl_price=1990.0,
            risk_percent=2.0,
            point_value=0.01,
            contract_size=100,
        )
        assert result == 0.2

    def test_calculate_risk_percent_wide_sl(self):
        """Test risk percent sizing with wider stop loss."""
        # Entry: 2000, SL: 1980 = 2000 points
        # For $100 risk: lot_size = 100 / (2000 * 0.01 * 100) = 0.05
        result = self.risk_manager.calculate_risk_percent(
            account_balance=10000,
            entry_price=2000.0,
            sl_price=1980.0,
            risk_percent=1.0,
            point_value=0.01,
            contract_size=100,
        )
        assert result == 0.05

    def test_calculate_risk_percent_zero_sl_distance(self):
        """Test risk percent sizing handles zero SL distance."""
        result = self.risk_manager.calculate_risk_percent(
            account_balance=10000,
            entry_price=2000.0,
            sl_price=2000.0,  # Same as entry
            risk_percent=1.0,
            point_value=0.01,
            contract_size=100,
        )
        assert result == 0.01  # Should return default lot size

    def test_calculate_risk_percent_uses_config(self):
        """Test risk percent sizing uses config when risk_percent not provided."""
        result = self.risk_manager.calculate_risk_percent(
            account_balance=10000,
            entry_price=2000.0,
            sl_price=1990.0,
            point_value=0.01,
            contract_size=100,
        )
        # Should use config.risk_percent = 1.0
        assert result == 0.1

    # ========== Kelly Criterion Tests ==========

    def test_calculate_kelly_basic(self):
        """Test Kelly Criterion calculation with favorable edge."""
        # Win rate: 60%, Avg win: $200, Avg loss: $100
        # b = 200/100 = 2.0 (payoff ratio)
        # f* = (0.6 * 2 - 0.4) / 2 = (1.2 - 0.4) / 2 = 0.4
        result = self.risk_manager.calculate_kelly(
            account_balance=10000,
            win_rate=0.6,
            avg_win=200.0,
            avg_loss=100.0,
        )

        assert result["kelly_fraction"] == 0.4
        assert result["payoff_ratio"] == 2.0
        assert result["full_kelly_amount"] == 4000.0  # 10000 * 0.4
        assert result["half_kelly_amount"] == 2000.0  # 4000 * 0.5

    def test_calculate_kelly_no_edge(self):
        """Test Kelly Criterion with no edge (negative Kelly)."""
        # Win rate: 40%, Avg win: $100, Avg loss: $100
        # b = 100/100 = 1.0
        # f* = (0.4 * 1 - 0.6) / 1 = -0.2 (don't trade)
        result = self.risk_manager.calculate_kelly(
            account_balance=10000,
            win_rate=0.4,
            avg_win=100.0,
            avg_loss=100.0,
        )

        assert result["kelly_fraction"] == 0.0  # Clamped to 0
        assert result["full_kelly_amount"] == 0.0
        assert result["half_kelly_amount"] == 0.0

    def test_calculate_kelly_high_win_rate(self):
        """Test Kelly Criterion with high win rate."""
        # Win rate: 80%, Avg win: $150, Avg loss: $100
        # b = 150/100 = 1.5
        # f* = (0.8 * 1.5 - 0.2) / 1.5 = (1.2 - 0.2) / 1.5 = 0.67
        result = self.risk_manager.calculate_kelly(
            account_balance=10000,
            win_rate=0.8,
            avg_win=150.0,
            avg_loss=100.0,
        )

        assert round(result["kelly_fraction"], 2) == 0.67
        assert result["payoff_ratio"] == 1.5

    def test_calculate_kelly_quarter_kelly(self):
        """Test Kelly Criterion with custom fraction."""
        result = self.risk_manager.calculate_kelly(
            account_balance=10000,
            win_rate=0.6,
            avg_win=200.0,
            avg_loss=100.0,
            max_kelly_fraction=0.25,  # Quarter Kelly
        )

        assert result["kelly_fraction"] == 0.4
        assert result["half_kelly_amount"] == 1000.0  # 4000 * 0.25

    def test_calculate_kelly_invalid_win_rate(self):
        """Test Kelly Criterion raises error for invalid win rate."""
        with pytest.raises(ValueError, match="win_rate must be between 0 and 1"):
            self.risk_manager.calculate_kelly(
                account_balance=10000,
                win_rate=1.5,  # Invalid
                avg_win=100.0,
                avg_loss=100.0,
            )

    def test_calculate_kelly_invalid_avg_loss(self):
        """Test Kelly Criterion raises error for invalid avg_loss."""
        with pytest.raises(ValueError, match="avg_loss must be positive"):
            self.risk_manager.calculate_kelly(
                account_balance=10000,
                win_rate=0.6,
                avg_win=100.0,
                avg_loss=0.0,  # Invalid
            )

    def test_calculate_kelly_invalid_avg_win(self):
        """Test Kelly Criterion raises error for invalid avg_win."""
        with pytest.raises(ValueError, match="avg_win must be positive"):
            self.risk_manager.calculate_kelly(
                account_balance=10000,
                win_rate=0.6,
                avg_win=0.0,  # Invalid
                avg_loss=100.0,
            )

    # ========== Max Drawdown Tests ==========

    def test_check_max_drawdown_within_limit(self):
        """Test drawdown check returns True when within limits."""
        result = self.risk_manager.check_max_drawdown(
            current_drawdown=5.0,
            max_allowed=10.0,
        )
        assert result is True

    def test_check_max_drawdown_at_limit(self):
        """Test drawdown check returns True at exact limit."""
        result = self.risk_manager.check_max_drawdown(
            current_drawdown=10.0,
            max_allowed=10.0,
        )
        assert result is True

    def test_check_max_drawdown_exceeds_limit(self):
        """Test drawdown check returns False when exceeding limits."""
        result = self.risk_manager.check_max_drawdown(
            current_drawdown=15.0,
            max_allowed=10.0,
        )
        assert result is False

    def test_check_max_drawdown_uses_config(self):
        """Test drawdown check uses config when max_allowed not provided."""
        result = self.risk_manager.check_max_drawdown(
            current_drawdown=5.0,
        )
        # Should use config.max_drawdown_percent = 10.0
        assert result is True

    def test_check_max_drawdown_config_exceeded(self):
        """Test drawdown check with config default exceeded."""
        result = self.risk_manager.check_max_drawdown(
            current_drawdown=15.0,
        )
        # Should use config.max_drawdown_percent = 10.0
        assert result is False

    # ========== Portfolio Heat Tests ==========

    def test_calculate_portfolio_heat_empty(self):
        """Test portfolio heat calculation with no positions."""
        result = self.risk_manager.calculate_portfolio_heat(
            positions=[],
            account_balance=10000,
        )

        assert result["total_heat"] == 0.0
        assert result["heat_percent"] == 0.0
        assert result["positions_count"] == 0
        assert result["avg_heat_per_position"] == 0.0

    def test_calculate_portfolio_heat_single_position(self):
        """Test portfolio heat calculation with single position."""
        positions = [
            {
                "lot_size": 0.1,
                "entry_price": 2000.0,
                "sl_price": 1990.0,
                "point_value": 0.01,
                "contract_size": 100,
            }
        ]
        # Heat = 0.1 * 1000 points * 0.01 * 100 = $100
        result = self.risk_manager.calculate_portfolio_heat(
            positions=positions,
            account_balance=10000,
        )

        assert result["total_heat"] == 100.0
        assert result["heat_percent"] == 1.0  # 100 / 10000 * 100
        assert result["positions_count"] == 1
        assert result["avg_heat_per_position"] == 100.0

    def test_calculate_portfolio_heat_multiple_positions(self):
        """Test portfolio heat calculation with multiple positions."""
        positions = [
            {
                "lot_size": 0.1,
                "entry_price": 2000.0,
                "sl_price": 1990.0,
                "point_value": 0.01,
                "contract_size": 100,
            },
            {
                "lot_size": 0.2,
                "entry_price": 2010.0,
                "sl_price": 2000.0,
                "point_value": 0.01,
                "contract_size": 100,
            }
        ]
        # Position 1: 0.1 * 1000 * 0.01 * 100 = $100
        # Position 2: 0.2 * 1000 * 0.01 * 100 = $200
        # Total heat = $300
        result = self.risk_manager.calculate_portfolio_heat(
            positions=positions,
            account_balance=10000,
        )

        assert result["total_heat"] == 300.0
        assert result["heat_percent"] == 3.0  # 300 / 10000 * 100
        assert result["positions_count"] == 2
        assert result["avg_heat_per_position"] == 150.0

    def test_calculate_portfolio_heat_different_sl_distances(self):
        """Test portfolio heat with varying stop loss distances."""
        positions = [
            {
                "lot_size": 0.1,
                "entry_price": 2000.0,
                "sl_price": 1990.0,  # 10 point SL
                "point_value": 0.01,
                "contract_size": 100,
            },
            {
                "lot_size": 0.1,
                "entry_price": 2000.0,
                "sl_price": 1980.0,  # 20 point SL
                "point_value": 0.01,
                "contract_size": 100,
            }
        ]
        # Position 1: 0.1 * 1000 * 0.01 * 100 = $100
        # Position 2: 0.1 * 2000 * 0.01 * 100 = $200
        result = self.risk_manager.calculate_portfolio_heat(
            positions=positions,
            account_balance=10000,
        )

        assert result["total_heat"] == 300.0
        assert result["heat_percent"] == 3.0

    def test_calculate_portfolio_heat_zero_balance(self):
        """Test portfolio heat handles zero balance gracefully."""
        positions = [
            {
                "lot_size": 0.1,
                "entry_price": 2000.0,
                "sl_price": 1990.0,
                "point_value": 0.01,
                "contract_size": 100,
            }
        ]
        result = self.risk_manager.calculate_portfolio_heat(
            positions=positions,
            account_balance=0,
        )

        assert result["total_heat"] == 0.0
        assert result["heat_percent"] == 0.0
        assert result["positions_count"] == 1  # Still counts positions
        assert result["avg_heat_per_position"] == 0.0

    def test_calculate_portfolio_heat_default_values(self):
        """Test portfolio heat uses default values for missing params."""
        positions = [
            {
                "lot_size": 0.1,
                "entry_price": 2000.0,
                "sl_price": 1990.0,
                # Missing point_value and contract_size, should use defaults
            }
        ]
        result = self.risk_manager.calculate_portfolio_heat(
            positions=positions,
            account_balance=10000,
        )

        # Uses defaults: point_value=0.01, contract_size=100
        assert result["total_heat"] == 100.0

    # ========== Backward Compatibility Tests ==========

    def test_calculate_lot_size_exists(self):
        """Test that existing calculate_lot_size method still works."""
        result = self.risk_manager.calculate_lot_size(
            account_balance=10000,
            entry_price=2000.0,
            sl_price=1990.0,
            risk_percent=1.0,
            leverage=200,
            point_value=0.01,
        )

        assert "lot_size" in result
        assert "risk_amount" in result
        assert "max_lot" in result
        assert "margin_required" in result
        assert "sl_points" in result

    def test_calculate_position_size_exists(self):
        """Test that existing calculate_position_size method still works."""
        result = self.risk_manager.calculate_position_size(
            account_balance=10000,
            risk_percent=1.0,
            entry_price=2000.0,
            sl_price=1990.0,
            point_value=0.01,
        )

        assert isinstance(result, float)
        assert result > 0

    # ========== Integration Tests ==========

    def test_complete_risk_workflow(self):
        """Test a complete risk management workflow."""
        account_balance = 10000

        # 1. Check if we can trade (drawdown within limits)
        can_trade = self.risk_manager.check_max_drawdown(
            current_drawdown=5.0
        )
        assert can_trade is True

        # 2. Calculate position using risk percent method
        lot_size = self.risk_manager.calculate_risk_percent(
            account_balance=account_balance,
            entry_price=2000.0,
            sl_price=1990.0,
            risk_percent=1.0,
        )
        assert lot_size == 0.1

        # 3. Calculate portfolio heat with this position
        positions = [
            {
                "lot_size": lot_size,
                "entry_price": 2000.0,
                "sl_price": 1990.0,
                "point_value": 0.01,
                "contract_size": 100,
            }
        ]
        heat = self.risk_manager.calculate_portfolio_heat(
            positions=positions,
            account_balance=account_balance,
        )
        assert heat["heat_percent"] == 1.0

        # 4. Check Kelly Criterion for optimal sizing
        kelly = self.risk_manager.calculate_kelly(
            account_balance=account_balance,
            win_rate=0.6,
            avg_win=200.0,
            avg_loss=100.0,
        )
        assert kelly["kelly_fraction"] > 0

    def test_risk_manager_with_different_configs(self):
        """Test RiskManager with different configurations."""
        # High risk config
        high_risk_config = RiskConfig(
            risk_percent=5.0,
            max_drawdown_percent=20.0,
        )
        high_risk_manager = RiskManager(high_risk_config)

        lot_size = high_risk_manager.calculate_risk_percent(
            account_balance=10000,
            entry_price=2000.0,
            sl_price=1990.0,
        )
        # Should be 5x larger than 1% risk
        assert lot_size == 0.5

        # Check drawdown allows higher limit
        can_trade = high_risk_manager.check_max_drawdown(
            current_drawdown=15.0
        )
        assert can_trade is True


class TestRiskConfig:
    """Test cases for RiskConfig dataclass."""

    def test_default_config(self):
        """Test RiskConfig default values."""
        config = RiskConfig()

        assert config.risk_mode == "fixed_risk_percent"
        assert config.fixed_lot == 0.01
        assert config.risk_percent == 1.0
        assert config.rr_ratio == 2.0
        assert config.leverage == 200
        assert config.max_spread_points == 30.0
        assert config.max_drawdown_percent == 10.0
        assert config.max_daily_trades == 1

    def test_custom_config(self):
        """Test RiskConfig with custom values."""
        config = RiskConfig(
            risk_mode="fixed_lot",
            fixed_lot=0.05,
            risk_percent=2.0,
            rr_ratio=3.0,
            leverage=500,
            max_spread_points=20.0,
            max_drawdown_percent=5.0,
            max_daily_trades=3,
        )

        assert config.risk_mode == "fixed_lot"
        assert config.fixed_lot == 0.05
        assert config.risk_percent == 2.0
        assert config.rr_ratio == 3.0
        assert config.leverage == 500
        assert config.max_spread_points == 20.0
        assert config.max_drawdown_percent == 5.0
        assert config.max_daily_trades == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
