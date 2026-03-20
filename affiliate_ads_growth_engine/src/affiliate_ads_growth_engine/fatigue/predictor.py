from typing import List

class FatiguePredictor:
    def check_fatigue(self, ctr_history: List[float]):
        """Detect if CTR is declining over time."""
        if len(ctr_history) < 3:
            return False, "Not enough data"
        
        # Check if last 3 entries are strictly descending
        if ctr_history[-1] < ctr_history[-2] < ctr_history[-3]:
            return True, "CTR declining 3 days in a row"
            
        avg = sum(ctr_history[:-1]) / (len(ctr_history) - 1)
        if ctr_history[-1] < (avg * 0.7):
            return True, "Current CTR >30% below average"
            
        return False, "Steady performance"
