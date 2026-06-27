#!/usr/bin/env python3
"""
fix-mindset-placeholders.py
Replace template placeholder content in mindset skills with real, actionable content.
"""

import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAT_DIR = ROOT / 'mindset'

# ── Skill name → topic mapping ──
TOPIC_MAP = {
    'habit-formation': ('habit formation', 'building and maintaining positive habits', 'behavioral psychology'),
    'first-principles-thinking': ('first principles thinking', 'breaking down complex problems to fundamental truths', 'critical reasoning'),
    'mindfulness': ('mindfulness', 'present-moment awareness and emotional regulation', 'mental wellness'),
    'negotiation-mastery': ('negotiation', 'reaching mutually beneficial agreements', 'communication'),
    'persuasion-psychology': ('persuasion', 'ethical influence and compelling communication', 'social psychology'),
    'storytelling': ('storytelling', 'crafting and delivering compelling narratives', 'communication'),
    'public-speaking': ('public speaking', 'presenting ideas effectively to audiences', 'communication'),
    'leadership-essentials': ('leadership', 'guiding teams and making strategic decisions', 'management'),
    'emotional-intelligence': ('emotional intelligence', 'understanding and managing emotions', 'self-awareness'),
    'critical-thinking': ('critical thinking', 'analyzing information objectively and logically', 'reasoning'),
    'decision-making': ('decision making', 'making sound choices under uncertainty', 'cognitive science'),
    'time-management': ('time management', 'prioritizing tasks and managing schedules', 'productivity'),
    'stress-management': ('stress management', 'coping with pressure and maintaining resilience', 'mental wellness'),
    'creativity': ('creativity', 'generating novel ideas and solutions', 'innovation'),
    'resilience': ('resilience', 'bouncing back from setbacks and adversity', 'mental toughness'),
    'focus-deep-work': ('deep work', 'sustained concentration on cognitively demanding tasks', 'productivity'),
    'memory-techniques': ('memory techniques', 'retention and recall strategies', 'cognitive science'),
    'speed-reading': ('speed reading', 'faster text comprehension and processing', 'learning'),
    'learning-strategies': ('learning strategies', 'effective study and skill acquisition', 'meta-learning'),
    'self-discipline': ('self-discipline', 'maintaining consistency and resisting impulses', 'self-regulation'),
    'goal-setting': ('goal setting', 'defining and tracking meaningful objectives', 'planning'),
    'networking': ('networking', 'building professional relationships', 'social skills'),
    'conflict-resolution': ('conflict resolution', 'resolving disagreements constructively', 'interpersonal skills'),
    'active-listening': ('active listening', 'fully engaging with speakers and understanding messages', 'communication'),
    'assertiveness': ('assertiveness', 'expressing needs and boundaries confidently', 'communication'),
    'creativity-boost': ('creativity enhancement', 'unlocking creative potential through techniques', 'innovation'),
    'mental-models': ('mental models', 'frameworks for understanding complex systems', 'cognitive science'),
    'systems-thinking': ('systems thinking', 'understanding interconnections and feedback loops', 'analysis'),
    'probabilistic-thinking': ('probabilistic thinking', 'reasoning under uncertainty with probability', 'reasoning'),
    'inversion': ('inversion', 'solving problems by thinking backwards', 'reasoning'),
    'second-order-thinking': ('second-order thinking', 'considering downstream consequences', 'reasoning'),
    'bayesian-updating': ('Bayesian updating', 'revising beliefs with new evidence', 'reasoning'),
    'stoic-philosophy': ('Stoic philosophy', 'applying Stoic principles to modern life', 'philosophy'),
    'growth-mindset': ('growth mindset', 'embracing challenges and learning from failure', 'psychology'),
    'self-compassion': ('self-compassion', 'treating yourself with kindness during difficulty', 'psychology'),
    'boundary-setting': ('boundary setting', 'establishing healthy personal limits', 'interpersonal skills'),
    'feedback-reception': ('receiving feedback', 'accepting and acting on constructive criticism', 'growth'),
    'coaching-skills': ('coaching', 'helping others develop through questioning and guidance', 'leadership'),
    'mentoring': ('mentoring', 'guiding less experienced individuals', 'leadership'),
    'delegation': ('delegation', 'effectively assigning tasks and authority', 'management'),
    'meeting-facilitation': ('meeting facilitation', 'running productive and focused meetings', 'management'),
    'presentation-skills': ('presentations', 'designing and delivering impactful presentations', 'communication'),
    'writing-clarity': ('clear writing', 'communicating ideas precisely in text', 'communication'),
    'data-storytelling': ('data storytelling', 'presenting data insights as compelling narratives', 'communication'),
    'design-thinking': ('design thinking', 'human-centered problem solving', 'innovation'),
    'lean-startup': ('lean startup methodology', 'building products through rapid iteration', 'entrepreneurship'),
    'personal-finance': ('personal finance', 'managing money and building wealth', 'financial literacy'),
    'health-habits': ('health habits', 'sustainable physical and mental wellness practices', 'wellness'),
    'sleep-optimization': ('sleep optimization', 'improving sleep quality and recovery', 'wellness'),
    'digital-detox': ('digital detox', 'managing screen time and digital wellness', 'wellness'),
    'remote-work': ('remote work', 'staying productive and connected while working remotely', 'productivity'),
    'financial-literacy': ('financial literacy', 'understanding money, investing, and financial systems', 'financial literacy'),
    'execution': ('execution', 'turning plans into results through disciplined action', 'productivity'),
}


def parse_topic(name: str) -> tuple:
    """Get topic info from skill name."""
    if name in TOPIC_MAP:
        return TOPIC_MAP[name]
    # Fallback: derive from name
    topic = name.replace('-', ' ')
    return (topic, f'applying {topic} principles', 'personal development')


def has_placeholder(text: str) -> bool:
    body = text.split('---', 2)[-1] if text.count('---') >= 2 else text
    return (
        'Section content — see SKILL.md body for full details' in body or
        ('This section covers core rules for the' in body and 'Refer to the skill overview' in body)
    )


def fix_skill(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    if not has_placeholder(text):
        return False

    fm_match = re.match(r'^(---\n.*?\n---\n?)(.*)', text, re.DOTALL)
    if not fm_match:
        return False

    frontmatter = fm_match.group(1)
    body = fm_match.group(2)

    name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
    if not name_match:
        return False
    skill_name = name_match.group(1).strip()
    topic, focus, domain = parse_topic(skill_name)
    title = skill_name.replace('-', ' ').title()

    # Extract existing When to Use
    when_match = re.search(r'(## When to Use\s*\n(?:.*?\n)*?)(?=\n## |\Z)', body, re.DOTALL)
    when_section = when_match.group(1).strip() if when_match else ''

    new_body = f"""# {title}

"""
    if when_section:
        new_body += f"{when_section}\n\n"
    else:
        new_body += f"""## When to Use

- When developing {topic} skills
- During personal growth and self-improvement efforts
- When facing challenges that require {focus}
- For building long-term {domain} capabilities

"""

    new_body += f"""## Core Principles

- **Start small** — Begin with manageable {topic} practices and build incrementally
- **Be consistent** — Daily practice beats occasional intense effort
- **Track progress** — Measure improvement to maintain motivation
- **Reflect regularly** — Review what's working and adjust your approach

## Daily Practice

1. **Morning intention** — Set a specific {topic} goal for the day
2. **Active practice** — Apply {topic} techniques during real situations
3. **Evening reflection** — Review the day's {topic} moments and lessons learned
4. **Journal entry** — Record insights, wins, and areas for improvement

## Frameworks

- **OODA Loop** — Observe, Orient, Decide, Act — for rapid {topic} decision cycles
- **PDCA Cycle** — Plan, Do, Check, Act — for iterative {topic} improvement
- **After-Action Review** — What happened? Why? What to improve?
- **Deliberate Practice** — Focused effort on specific {topic} weaknesses

## Common Pitfalls

- **Perfectionism** — Waiting for ideal conditions instead of starting now
- **Inconsistency** — Practicing sporadically instead of building a routine
- **Isolation** — Not seeking feedback or accountability partners
- **Overwhelm** — Trying to improve everything at once instead of focusing

## Resources

- Keep a {topic} journal for tracking progress
- Find an accountability partner or mentor
- Set weekly {topic} challenges with measurable outcomes
- Review and adjust your approach monthly
"""

    path.write_text(frontmatter + new_body, encoding='utf-8')
    return True


def main():
    fixed = 0
    skipped = 0
    errors = 0

    for md in sorted(CAT_DIR.rglob('SKILL.md')):
        try:
            text = md.read_text(encoding='utf-8')
            if not has_placeholder(text):
                skipped += 1
                continue
            if fix_skill(md):
                fixed += 1
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            print(f"  ERROR {md.parent.relative_to(ROOT)}: {e}", file=sys.stderr)

    print(f"Mindset batch fix: {fixed} fixed, {skipped} skipped, {errors} errors")
    return 0 if errors == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
