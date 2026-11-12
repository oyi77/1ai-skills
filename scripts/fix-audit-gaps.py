#!/usr/bin/env python3
"""Fix audit gaps:
1) Prepend "Use when..." to descriptions lacking a trigger phrase in first 60 chars.
2) Append Anti-Rationalization Table to 3 skills missing it.

Idempotent: skips skills already compliant.
"""
from __future__ import annotations
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TRIGGER_PHRASES = [
    "use when", "triggers on", "covers", "activates for",
    "use for", "automated", "generates",
]

# Skills missing trigger phrase -> trigger tail to append (specific, per-skill)
# Derived from each skill's actual purpose by reading them.
TRIGGER_TAILS: dict[str, str] = {
    # content/hyperframes
    "hyperframes-embedded-captions": "adding captions or subtitles to talking-head or launch videos",
    "video-strategy-orchestrator": "deciding which video pipeline (Remotion, HyperFrames, AI generation) fits a brief",
    "video-production-orchestrator": "coordinating all video generation and editing under one entry point",
    "image-director": "managing visual design production across multiple image skills",
    "hyperframes-slideshow": "building a presentation, pitch deck, or interactive deck as video",
    "company-handbook": "coordinating cross-director work across the 1ai business kingdom",
    "hyperframes-faceless-explainer": "turning text (article, notes, topic) into a faceless explainer video",
    "video-director": "managing end-to-end video production under a single director role",
    "vilona-gm": "acting as the General Manager AI coordinating the 1ai business kingdom",
    "hyperframes-motion-graphics": "creating short, unnarrated design-led motion graphics under 10s",
    "hyperframes-general-video": "any HyperFrames video brief that does not fit a specific template",
    "hyperframes-oversized-cursor": "applying the oversized macOS cursor technique in HyperFrames videos",
    "hyperframes-music-to-video": "turning a music track into a beat-synced video with lyrics or slides",
    "sales-director": "managing all sales activities across the 1ai business kingdom",
    "hyperframes-talking-head-recut": "packaging an existing talking-head, interview, or podcast video",
    "hyperframes-product-launch-video": "creating product launch videos from a URL, brief, or script",
    "banner-design": "designing banners for social media, ads, web, or print",
    "marketing-director": "managing all marketing activities across the 1ai business kingdom",
    "ui-ux-pro-max": "designing UI/UX for web, mobile, or desktop",
    "content-director": "orchestrating content production across the 1ai business kingdom",
    "hyperframes-pr-to-video": "turning a GitHub pull request into a changelog or feature-reveal video",
    "hyperframes-seam-craft": "assembling scene-to-scene seams in HyperFrames video timelines",
    "hyperframes-changelog-video": "turning a weekly changelog markdown into a branded video",
    "vicestudio": "running a local-first AI voice studio for cloning, design, dubbing, or dictation",
    # development/*-audit + tdd-bug-reproduction + godfile-ratchet + dead-code
    "dead-code-graveyard": "auditing and safely pruning dead code, unreachable branches, and unused exports",
    "tdd-bug-reproduction": "isolating a bug and writing a failing minimal reproduction test first",
    "concurrency-race-audit": "auditing concurrent async code for thread safety and shared-state races",
    "api-contract-drift-audit": "auditing client-server API contracts and schema parity",
    "godfile-ratchet-split": "carving monolithic god-files into decoupled domain modules",
    "ast-architectural-guard": "enforcing architectural layer boundaries, import rules, and cycle checks",
    "type-narrowing-audit": "auditing and replacing unsafe `any` types and untyped catch blocks",
    "zero-downtime-migration-audit": "auditing DB migrations for backward/forward compatibility",
}

# Skills missing Anti-Rationalization Table -> tailored content
ANTI_RAT = {
    "content/hallmark": [
        ("We'll add the verification evidence later", "Claims without evidence are opinions. Every hallmark must ship with reproducible proof (output, screenshot, test)."),
        ("The code looks right", "Visual review misses regressions. Run the checklist and paste the terminal output."),
        ("It passed once, we're done", "Hallmarks must hold on the current head. Re-run on the latest commit before publishing."),
        ("Skipping the checklist saves time", "The checklist is the deliverable, not overhead. Skipping it ships unverifiable claims."),
        ("Edge cases are out of scope", "Hallmarks without edge cases are demos. Cover the boundaries or mark the limits explicitly."),
    ],
    "cybersecurity/cloudflare-security-audit": [
        ("We'll document the findings later", "Undocumented findings are unfixable findings. Record every misconfiguration with a reproduction path."),
        ("The WAF is enabled, so we're covered", "WAF rules drift and miss application logic. Verify each rule against the current traffic and config."),
        ("Cloudflare handles security for us", "Shared responsibility: Cloudflare protects the edge, you own origin, IAM, and app logic."),
        ("No CVEs means no findings", "Most Cloudflare issues are misconfigurations, not CVEs. Audit settings, not just patch level."),
        ("Skipping the origin check saves time", "Origin bypass is a classic Cloudflare failure mode. Always verify origin reachability and auth."),
    ],
    "research/scientific-agent-skills": [
        ("The LLM output is authoritative", "Model output is a draft, not evidence. Verify every factual claim against a primary source."),
        ("We'll add citations later", "Uncited research is unverifiable. Attach sources as you produce each claim."),
        ("One source is enough", "Single-source claims fail triangulation. Cross-check across independent references."),
        ("Skipping the hypothesis step saves time", "Without a pre-registered hypothesis you cannot tell signal from noise."),
        ("The paper is recent, so it's right", "Recency is not validity. Check methodology, sample size, and replication status."),
    ],
}


def add_trigger_phrase(path: Path, name: str) -> bool:
    """Rewrite description to start with 'Use when ...' by appending a tail."""
    text = path.read_text()
    # Locate description line(s). YAML can be single-line, multi-line (>), or block (|).
    # Simplest robust approach: parse frontmatter, mutate description, re-serialize FM.
    if not text.startswith("---\n"):
        return False
    end_idx = text.find("\n---\n", 3)
    if end_idx == -1:
        return False
    fm_raw = text[4:end_idx]
    body = text[end_idx + 5:]

    try:
        import yaml
        fm = yaml.safe_load(fm_raw) or {}
    except Exception:
        return False

    desc = str(fm.get("description", ""))
    first60 = desc.lower()[:60]
    if any(ph in first60 for ph in TRIGGER_PHRASES):
        return False  # already compliant

    tail = TRIGGER_TAILS.get(name)
    if not tail:
        return False  # unknown; skip (report below)

    # Capitalize first letter of original desc for the compound sentence
    desc_stripped = desc.rstrip(".")
    new_desc = f"Use when {tail}. {desc_stripped}."
    fm["description"] = new_desc

    # Re-dump frontmatter, preserve key order where possible (safe_load loses order;
    # acceptable for these 32 files — original order is not semantically meaningful).
    new_fm = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, default_flow_style=False, width=400)
    new_text = f"---\n{new_fm}---\n{body}"
    path.write_text(new_text)
    return True


def add_anti_rat_table(path: Path, name: str) -> bool:
    text = path.read_text()
    if "## Anti-Rationalization Table" in text:
        return False
    rows = ANTI_RAT.get(name)
    if not rows:
        return False
    table_lines = ["", "## Anti-Rationalization Table", "", "| Rationalization | Reality |", "|---|---|"]
    for rat, reality in rows:
        table_lines.append(f"| \"{rat}\" | {reality} |")
    table_lines.append("")
    # Append at end (tables must come after body; audit scans whole body)
    new_text = text.rstrip() + "\n" + "\n".join(table_lines) + "\n"
    path.write_text(new_text)
    return True


def main():
    import yaml  # noqa: F401  (ensures import error surfaces early)
    fixed_trig = []
    fixed_arat = []
    skipped = []

    # 1. Trigger phrase fixes
    for skill_dir in sorted({p.parent for p in ROOT.rglob("SKILL.md") if "_demoted" not in p.parts}):
        path = skill_dir / "SKILL.md"
        name = skill_dir.name
        if name not in TRIGGER_TAILS:
            continue
        if add_trigger_phrase(path, name):
            fixed_trig.append(name)
        else:
            skipped.append(f"trig:{name}")

    # 2. Anti-Rat table fixes
    for name in ANTI_RAT:
        path = ROOT / name / "SKILL.md"
        if add_anti_rat_table(path, name):
            fixed_arat.append(name)
        else:
            skipped.append(f"arat:{name}")

    print(f"trigger fixed: {len(fixed_trig)}")
    for n in fixed_trig: print(" ", n)
    print(f"anti-rat fixed: {len(fixed_arat)}")
    for n in fixed_arat: print(" ", n)
    print(f"skipped: {len(skipped)}")
    for s in skipped: print(" ", s)


if __name__ == "__main__":
    main()
