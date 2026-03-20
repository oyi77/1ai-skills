from typing import List, Dict

class StoryboardBuilder:
    def build(self, topic: str):
        return [
            {"scene": "Scene 1", "type": "problem", "description": f"Masalah utama: {topic}"},
            {"scene": "Scene 2", "type": "solution", "description": f"Solusi: {topic} fix"},
            {"scene": "Scene 3", "type": "product_detail", "description": "Highlight fitur/hasil"},
            {"scene": "Scene 4", "type": "cta", "description": "Call to action jelas"}
        ]
