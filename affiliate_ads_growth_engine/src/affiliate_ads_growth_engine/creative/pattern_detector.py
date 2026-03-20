from typing import List, Dict

PATTERN_KEYWORDS = {
    "testimonial": ["testimoni", "review", "kata mereka"],
    "before_after": ["sebelum", "sesudah", "before", "after"],
    "problem_solution": ["masalah", "solusi", "problem", "solution"],
    "lifestyle": ["pagi", "malam", "rutinitas", "lifestyle"],
}

class CreativePatternDetector:
    def detect(self, caption: str) -> List[str]:
        caption_lower = caption.lower()
        patterns = []
        for pattern, keywords in PATTERN_KEYWORDS.items():
            if any(keyword in caption_lower for keyword in keywords):
                patterns.append(pattern)
        return patterns
