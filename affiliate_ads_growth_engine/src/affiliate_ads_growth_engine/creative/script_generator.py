from typing import List

SCRIPT_TEMPLATE = """Hook (0-3s): {hook}

Scene 1: {scene1}
Scene 2: {scene2}
Scene 3: {scene3}

Call To Action: {cta}
"""

class ScriptGenerator:
    def __init__(self, tone: str = "bold"):
        self.tone = tone

    def generate(self, hook: str, scenes: List[str], cta: str = "Swipe up sekarang!"):
        scenes = scenes + [""] * (3 - len(scenes))
        return SCRIPT_TEMPLATE.format(
            hook=hook,
            scene1=scenes[0],
            scene2=scenes[1],
            scene3=scenes[2],
            cta=cta
        )
