#!/usr/bin/env python3
"""
Vidabot Intelligence Analysis - Part 3 Deliverables
Runs all bot_extractor v2 analysis functions on the vidabot architecture JSON.
"""

import json
import sys
import os
import re
import time

# Add bot_extractor to path
sys.path.insert(
    0, "/mnt/data/berkahkarya/skills/1ai-skills/development/bot-extractor/scripts"
)

from bot_extractor import (
    build_state_machine,
    analyze_payload_patterns,
    analyze_message_formats,
    detect_bot_personality,
    generate_weakness_report,
    estimate_clone_difficulty,
    generate_flowchart,
)

INPUT_JSON = "/mnt/data/berkahkarya/skills/1ai-skills/development/bot-extractor/references/vidabot_generator_bot_arch_v2.json"
OUTPUT_INTEL = "/mnt/data/berkahkarya/skills/1ai-skills/research/competitor-intel/reports/vidabot_full_intel.json"
OUTPUT_FLOWCHART = "/mnt/data/berkahkarya/skills/1ai-skills/development/bot-extractor/references/vidabot_flowchart.md"


def main():
    print(f"[*] Loading vidabot architecture from {INPUT_JSON}")
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        arch = json.load(f)

    print(f'[*] Bot: {arch["bot"]}')
    print(f'[*] Extracted at: {arch["extracted_at"]}')
    print()

    # 1. Build state machine
    print("[1/7] Building state machine...")
    arch["state_machine"] = build_state_machine(arch)
    sm = arch["state_machine"]
    print(f'      States: {sm["total_states"]}')
    print(f'      Dead ends: {sm["issues"]["dead_ends"]}')
    print(f'      Missing cancel: {sm["issues"]["missing_cancel_handlers"]}')
    print(f'      Circular states: {sm["issues"]["circular_states"]}')
    print()

    # 2. Analyze payload patterns
    print("[2/7] Analyzing payload patterns...")
    arch["input_flows"] = analyze_payload_patterns(arch)
    for flow in arch["input_flows"]:
        reqs = flow.get("requirements", [])
        print(f'      {flow["trigger"]}: {flow["state"]} | reqs: {reqs}')
    print()

    # 3. Analyze message formats
    print("[3/7] Analyzing message formats...")
    arch["format_analysis"] = analyze_message_formats(arch)
    for key, analysis in arch["format_analysis"].items():
        print(
            f'      {key[:50]}: {analysis["format_type"]} | {analysis["length"]} chars | emojis: {analysis["emojis_used"]}'
        )
    print()

    # 4. Detect bot personality
    print("[4/7] Detecting bot personality...")
    arch["bot_personality"] = detect_bot_personality(arch)
    bp = arch["bot_personality"]
    print(f'      Language: {bp["language"]}')
    print(
        f'      Language ratio: ID={bp["language_ratio"]["indonesian"]}, EN={bp["language_ratio"]["english"]}'
    )
    print(f'      Formality: {bp["formality"]}')
    print(f'      Tone: {bp["tone"]}')
    print(
        f'      Emoji density: {bp["emoji_density"]} ({bp["emoji_per_message"]} per msg)'
    )
    print(f'      Avg message length: {bp["avg_message_length"]} words')
    print()

    # 5. Generate weakness report
    print("[5/7] Generating weakness report...")
    arch["weakness_report"] = generate_weakness_report(arch)
    wr = arch["weakness_report"]
    print(f"      Total weaknesses: {len(wr)}")
    for w in wr:
        print(f'      [{w["severity"].upper()}] {w["detail"]}')
    print()

    # 6. Estimate clone difficulty
    print("[6/7] Estimating clone difficulty...")
    arch["clone_difficulty"] = estimate_clone_difficulty(arch)
    cd = arch["clone_difficulty"]
    print(f'      Score: {cd["score"]}/{cd["max_score"]}')
    print(
        f'      Estimated hours: {cd["estimated_hours"]}h ({cd["estimated_days"]} days)'
    )
    print(f'      Breakdown: {cd["breakdown"]}')
    print(f'      Challenges: {cd["key_challenges"]}')
    print()

    # 7. Generate flowchart
    print("[7/7] Generating mermaid flowchart...")
    arch["mermaid_flowchart"] = generate_flowchart(arch)
    flowchart = arch["mermaid_flowchart"]
    line_count = flowchart.count("\n") + 1
    print(f"      Flowchart lines: {line_count}")
    print()

    # Save enriched architecture
    os.makedirs(os.path.dirname(OUTPUT_INTEL), exist_ok=True)
    with open(OUTPUT_INTEL, "w", encoding="utf-8") as f:
        json.dump(arch, f, indent=2, ensure_ascii=False)
    print(f"[+] Saved enriched intel to {OUTPUT_INTEL}")

    # Save flowchart
    os.makedirs(os.path.dirname(OUTPUT_FLOWCHART), exist_ok=True)
    with open(OUTPUT_FLOWCHART, "w", encoding="utf-8") as f:
        f.write(f'# Flowchart: {arch["bot"]}\n\n```mermaid\n{flowchart}\n```\n')
    print(f"[+] Saved flowchart to {OUTPUT_FLOWCHART}")

    print()
    print("=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
