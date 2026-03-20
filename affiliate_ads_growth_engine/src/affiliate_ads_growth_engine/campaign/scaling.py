class ScalingStrategy:
 def recommend(self, performance: str):
 if performance == "winner":
 return ["Scale budget +20%", "Duplicate into new audience"]
 if performance == "loser":
 return ["Kill ad", "Reallocate budget"]
 return ["Monitor24h"]
