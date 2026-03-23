from typing import List
import random

HOOK_TEMPLATES = [
    "Rahasia {topic} yang tidak pernah dibahas",
    "Cara hemat {topic} tanpa ribet",
    "Kenapa 90% orang gagal di {topic}?",
    "Ini alasan kenapa {topic} ...",
    "Framework 3 langkah untuk {topic}",
    "Gimana kalau {topic} bisa 10x lebih cepat?",
    "Fakta {topic} yang bikin mindblown",
    "#1 kesalahan saat {topic}",
]

CREATIVE_PATTERNS = [
    "testimonial",
    "before_after",
    "problem_solution",
    "lifestyle",
]

ANGLES = [
    "Pain point",
    "Desire",
    "Social proof",
    "Time saving",
    "Budget friendly",
    "Community",
    "Scarcity"
]

class IdeaGenerator:
    def __init__(self, topic_library: List[str]):
        self.topic_library = topic_library

    def generate_daily(self, count: int = 20):
        ideas = []
        for _ in range(count):
            topic = random.choice(self.topic_library)
            hook = random.choice(HOOK_TEMPLATES).format(topic=topic)
            angle = random.choice(ANGLES)
            pattern = random.choice(CREATIVE_PATTERNS)
            ideas.append({
                "topic": topic,
                "hook": hook,
                "angle": angle,
                "pattern": pattern
            })
        return ideas
