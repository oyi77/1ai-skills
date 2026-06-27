# /find — Discover and activate the right skill

Search the 1ai-skills library for the skill matching the user's request.

## Steps

1. Parse the user's request for domain keywords (security, trading, marketing, devops, etc.)
2. Search `SKILLS.json` for matching skills by name, description, tags, and domain
3. Present the top 3 matches with:
   - Skill name and category
   - Description (first sentence)
   - Trigger conditions ("When to Use")
4. Let the user confirm which skill to activate
5. Load the confirmed skill via the `skill` tool

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I'll just guess the right skill" | Wrong skill = wrong workflow. Always search first. |
| "The skill name is obvious" | Many skills overlap. Description matching is more reliable. |
| "I don't need a skill for this" | If a skill exists, it has tested workflows. Use it. |
