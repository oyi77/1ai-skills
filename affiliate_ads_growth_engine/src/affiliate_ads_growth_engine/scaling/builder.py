class ScalingBlueprint:
    def suggest_scaling(self, current_budget: float, roas: float, orders: int):
        if roas >= 3.0 and orders >= 10:
            increase = current_budget * 0.2
            return {
                "action": "Scale Up (Horizontal/Vertical)",
                "budget_increase": increase,
                "new_budget": current_budget + increase,
                "strategy": "Increase budget by 20% every 48h while ROAS > 2.5."
            }
        elif roas < 1.0:
            return {
                "action": "Kill / Pivot",
                "strategy": "ROAS below breakeven. Check creative fatigue or offer appeal."
            }
        return {"action": "Hold / Optimize", "strategy": "Monitor performance for 24h."}
