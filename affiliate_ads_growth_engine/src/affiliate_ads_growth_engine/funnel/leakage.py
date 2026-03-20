class LeakageAnalyzer:
    def analyze(self, fb_clicks: int, shopee_clicks: int):
        if fb_clicks == 0:
            return 0.0, "No FB traffic"
        
        leakage = (fb_clicks - shopee_clicks) / fb_clicks
        status = "Healthy"
        if leakage > 0.4: status = "CRITICAL LEAKAGE (Check Redirect)"
        elif leakage > 0.2: status = "Warning (High Drop-off)"
        
        return leakage, status
