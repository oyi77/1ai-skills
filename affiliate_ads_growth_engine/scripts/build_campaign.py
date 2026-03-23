#!/usr/bin/env python3
from affiliate_ads_growth_engine.campaign.architect import CampaignArchitect

architect = CampaignArchitect()
structure = architect.build_structure(["Sales", "Leads"])
print(structure)
