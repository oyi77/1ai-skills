from .idea_generator import IdeaGenerator
from .script_generator import ScriptGenerator
from .storyboard import StoryboardBuilder
from .pattern_detector import CreativePatternDetector

class CreativeIntelligenceEngine:
    def __init__(self, topics):
        self.idea_generator = IdeaGenerator(topics)
        self.script_generator = ScriptGenerator()
        self.storyboard_builder = StoryboardBuilder()
        self.pattern_detector = CreativePatternDetector()

    def daily_ideas(self):
        return self.idea_generator.generate_daily(20)

    def script_for_platform(self, hook, scenes):
        return self.script_generator.generate(hook, scenes)

    def storyboard(self, topic):
        return self.storyboard_builder.build(topic)

    def detect_patterns(self, caption):
        return self.pattern_detector.detect(caption)
