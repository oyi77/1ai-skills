---
name: long-form
description: Use when writing long-form content — SEO blog articles, thought leadership pieces, guides with structured outlines, word targeting, and reading time estimation.
domain: content
tags: [content-creation, long-form]
version: 1.0.0
---

# Long Form

Quick Reference — for full workflow see [../SKILL.md](../SKILL.md).

Long-form content (1,500-3,000 words) drives 5-10x more organic traffic than short posts and commands the highest per-word rates from content clients. This sub-skill covers SEO-optimized article outlining, section-by-section word targeting, and reading time estimation.

## Quick Start

1. **Define the topic & keywords** — Pick one primary topic + 3-5 secondary keywords from keyword research. The topic must answer a real search intent (informational, commercial, or transactional).
2. **Generate outline** — Use `generate_article_outline()` to build a 6-8 section structure with word targets per section (intro: 250, body sections: 350 each, conclusion: 200).
3. **Draft section-by-section** — Write each section against its word target. Keep total reading time under 15 minutes (3,000 words @ 200 wpm).

## Key Function: SEO Article Outline Generator

```python
def generate_article_outline(
    topic: str,
    audience: str,
    keywords: list[str],
    sections: int = 6,
) -> list[dict]:
    """
    Generate an SEO-optimized long-form article outline.
    Returns list of { heading, sub_points, word_target, keywords }.
    """
    outline = [
        {
            "heading": f"Introduction: Why {topic} Matters for {audience}",
            "sub_points": [
                f"The current state of {topic}",
                f"Why {audience} should care",
                "What you will learn",
            ],
            "word_target": 250,
            "keywords": [topic, f"{topic} guide"],
        },
    ]
    for i in range(1, sections):
        outline.append({
            "heading": f"Section {i}: {'Key ' if i > 1 else ''}Strategy — "
                       f"{' '.join(topic.split()[:3])}",
            "sub_points": [
                f"Understanding {topic} from {audience} perspective",
                "Step-by-step implementation",
                "Common mistakes to avoid",
            ],
            "word_target": 350,
            "keywords": [f"{topic} strategy", f"{topic} tips"],
        })
    outline.append({
        "heading": "Conclusion: Your Next Steps",
        "sub_points": [
            "Recap of key takeaways",
            "Immediate action items",
            "Further reading",
        ],
        "word_target": 200,
        "keywords": [f"{topic} summary", f"{topic} next steps"],
    })
    return outline


def extract_headings(outline: list[dict]) -> str:
    """Extract markdown headings + sub-points from an outline."""
    lines = ["# " + outline[0]["heading"].replace("Introduction: ", "")]
    for sec in outline[1:]:
        lines.append(f"\n## {sec['heading']}")
        for sp in sec["sub_points"]:
            lines.append(f"- {sp}")
    total_words = sum(s["word_target"] for s in outline)
    lines.append(f"\n---\n*Reading time: {max(1, round(total_words / 200))} min*")
    return "\n".join(lines)


# Outline structure rule: problem → solution → implementation → results → next steps.
# Each section answers one user question. Never write a section without knowing
# what question it answers.
```

## Verification Checklist

- [ ] Outline has clear introduction, 6-8 body sections, and conclusion
- [ ] Word targets assigned per section, total 1,500-3,000 words
- [ ] Primary keyword in H1; secondary keywords in H2s (natural, not stuffed)
- [ ] Reading time estimated: 200 wpm, ≤15 minutes
- [ ] Each section answers one specific user question (search intent)
- [ ] Headings scannable — a reader should get the gist from headings alone
- [ ] CTA placed within the last 300 words, tying back to the intro promise

## Workflow

Execute these steps sequentially:

1. **Define the topic & keywords** — Pick one primary topic + 3-5 secondary keywords from keyword research. The topic must answer a real search intent (informational, commercial, or transactional).
2. **Generate outline** — Use `generate_article_outline()` to build a 6-8 section structure with word targets per section (intro: 250, body sections: 350 each, conclusion: 200).
3. **Draft section-by-section** — Write each section against its word target. Keep total reading time under 15 minutes (3,000 words @ 200 wpm).

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Word count is what matters" | A 3,000-word article that doesn't answer the reader's question gets zero conversions. Intent beats volume. |
| "Write the whole thing, then SEO" | SEO keywords need to be baked into the outline. Retro-fitting keywords always sounds stuffed. |
| "Sections are arbitrary" | Each section must answer one specific user question. If you can't name the question, the section is filler. |
| "Longer = more authoritative" | 2,000 tight words outperform 4,000 rambling words every time. Edit ruthlessly — cut everything that doesn't serve the core promise. |

## When to Use
Use this skill when writing long-form articles for SEO blogs, thought leadership pieces, content marketing assets, client deliverables in agency workflows, or anything needing structured 1,500-3,000 word content.
