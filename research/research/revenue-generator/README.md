# Revenue Generator

Takes BerkahKarya's current assets and generates a ranked revenue playbook with week-by-week action plans.

## Features
- Analyzes current tools, audience, products, skills, budget
- Generates opportunities matrix using LLM (OmniRoute, gpt-4o-mini)
- Scores each opportunity: revenue_speed x potential x effort_inverse
- Outputs ranked playbook with IMMEDIATE / SHORT-TERM / MEDIUM-TERM categories

## Quick Start
```bash
python3 scripts/revenue_generator.py
```

## Output
- Markdown playbook: `reports/berkahkarya_playbook.md`
- JSON data: `reports/berkahkarya_playbook.json`
