class BlendedFinance:
    def calculate_profit(self, ad_spend: float, shopee_revenue: float, recurring_costs: float = 0):
        """Total revenue - spend - base costs."""
        # Simple net logic
        net = shopee_revenue - ad_spend - recurring_costs
        margin = (net / shopee_revenue) if shopee_revenue > 0 else 0
        
        return {
            "net_profit": net,
            "margin": margin,
            "status": "PROFIT" if net > 0 else "LOSS"
        }
