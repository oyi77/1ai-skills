#!/usr/bin/env python3
from affiliate_ads_growth_engine.creative.idea_generator import IdeaGenerator
from affiliate_ads_growth_engine.creative.script_generator import ScriptGenerator

ideas = IdeaGenerator(["Shopee Affiliate", "Facebook Ads Scaling", "Winning Creative"])
print(ideas.generate(5))

script = ScriptGenerator().generate("Facebook Ads", ["Hook", "Problem", "Solution", "CTA"])
print(script)
