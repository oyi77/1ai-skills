#!/usr/bin/env python3
"""
Agent Team Orchestrator — Route tasks to specialized agent roles via OmniRoute.

Detects required roles from task description, assigns specialized system prompts,
routes through OmniRoute, and combines outputs.

Usage:
    python team_orchestrator.py --task "Research and write analysis of BTC market this week"
    python team_orchestrator.py --task "Build a landing page for product X" --roles researcher,coder
    python team_orchestrator.py --task "..." --output json
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime

ROLE_DEFINITIONS = {
    "researcher": {
        "name": "Researcher",
        "description": "Gathers facts, data, and context",
        "system_prompt": (
            "You are a research specialist. Your job is to gather relevant facts, data, "
            "statistics, and context about the given topic. Be thorough and cite sources "
            "where possible. Focus on accuracy and recency. Output structured findings."
        ),
        "keywords": ["research", "analyze", "data", "find", "investigate", "market",
                      "trend", "compare", "study", "report"]
    },
    "writer": {
        "name": "Writer",
        "description": "Produces polished written content",
        "system_prompt": (
            "You are a professional content writer. Your job is to produce clear, engaging, "
            "well-structured written content. Adapt tone to the audience. Use headings, "
            "bullet points, and concise paragraphs. Output publication-ready text."
        ),
        "keywords": ["write", "article", "blog", "content", "copy", "draft",
                      "summary", "newsletter", "post", "essay"]
    },
    "analyst": {
        "name": "Analyst",
        "description": "Interprets data and provides insights",
        "system_prompt": (
            "You are a data analyst. Your job is to interpret information, identify patterns, "
            "assess risks and opportunities, and provide actionable insights. Use numbers "
            "and evidence. Output structured analysis with recommendations."
        ),
        "keywords": ["analysis", "insight", "evaluate", "assess", "forecast",
                      "opportunity", "risk", "strategy", "recommendation", "metrics"]
    },
    "coder": {
        "name": "Coder",
        "description": "Writes and reviews code",
        "system_prompt": (
            "You are a senior software engineer. Your job is to write clean, functional code "
            "that solves the given problem. Follow best practices, include error handling, "
            "and add brief comments. Output working code with usage instructions."
        ),
        "keywords": ["code", "build", "implement", "script", "api", "function",
                      "debug", "fix", "develop", "program", "app", "page"]
    }
}


def detect_roles(task_text):
    """Detect which roles are needed based on task keywords."""
    task_lower = task_text.lower()
    scores = {}

    for role_id, role in ROLE_DEFINITIONS.items():
        score = sum(1 for kw in role["keywords"] if kw in task_lower)
        if score > 0:
            scores[role_id] = score

    if not scores:
        # Default: researcher + writer
        return ["researcher", "writer"]

    # Return roles sorted by relevance, at least 2
    sorted_roles = sorted(scores, key=scores.get, reverse=True)
    if len(sorted_roles) < 2:
        # Add a complementary role
        if "researcher" not in sorted_roles:
            sorted_roles.append("researcher")
        elif "writer" not in sorted_roles:
            sorted_roles.append("writer")

    return sorted_roles


def call_omniroute(prompt, system_prompt, model=None):
    """Call OmniRoute to get a response from a specialized agent."""
    omniroute = os.path.expanduser("~/.openclaw/workspace/scripts/omniroute")

    if not os.path.exists(omniroute):
        # Fallback: try omniroute in PATH
        omniroute = "omniroute"

    cmd = [omniroute, "--prompt", prompt]
    if system_prompt:
        cmd.extend(["--system", system_prompt])
    if model:
        cmd.extend(["--model", model])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"[OmniRoute error: {result.stderr.strip()}]"
    except FileNotFoundError:
        return "[OmniRoute not found — install or configure omniroute path]"
    except subprocess.TimeoutExpired:
        return "[OmniRoute timeout — task may be too complex for single call]"


def orchestrate(task, roles=None, output_format="markdown"):
    """Orchestrate a team of agents to handle the task."""
    if roles is None:
        roles = detect_roles(task)

    results = {
        "task": task,
        "timestamp": datetime.now().isoformat(),
        "team": [],
        "outputs": {}
    }

    print(f"Task: {task}", file=sys.stderr)
    print(f"Detected roles: {', '.join(roles)}", file=sys.stderr)
    print(f"Orchestrating {len(roles)} agents...\n", file=sys.stderr)

    for role_id in roles:
        role = ROLE_DEFINITIONS.get(role_id)
        if not role:
            print(f"Unknown role: {role_id}, skipping", file=sys.stderr)
            continue

        print(f"  → {role['name']}: working...", file=sys.stderr)

        role_prompt = (
            f"Task: {task}\n\n"
            f"Your role: {role['description']}\n"
            f"Provide your contribution to this task from your specialist perspective."
        )

        output = call_omniroute(role_prompt, role["system_prompt"])

        results["team"].append({
            "role": role_id,
            "name": role["name"],
            "description": role["description"]
        })
        results["outputs"][role_id] = output
        print(f"  ✓ {role['name']}: done", file=sys.stderr)

    # Combine outputs
    print(f"\n  → Synthesizing final output...", file=sys.stderr)
    synthesis_prompt = (
        f"You are a team lead synthesizing specialist outputs into a cohesive deliverable.\n\n"
        f"Original task: {task}\n\n"
    )
    for role_id, output in results["outputs"].items():
        role_name = ROLE_DEFINITIONS[role_id]["name"]
        synthesis_prompt += f"--- {role_name} Output ---\n{output}\n\n"
    synthesis_prompt += (
        "Combine these specialist contributions into a single, coherent, "
        "well-structured deliverable. Resolve any conflicts. Remove redundancy."
    )

    final = call_omniroute(synthesis_prompt, "You are a senior team lead producing final deliverables.")
    results["final_output"] = final

    return results


def main():
    parser = argparse.ArgumentParser(description="Orchestrate multi-agent team for complex tasks")
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument("--roles", help="Comma-separated roles (auto-detected if omitted)")
    parser.add_argument("--output", choices=["json", "markdown"], default="markdown",
                        help="Output format (default: markdown)")
    args = parser.parse_args()

    roles = args.roles.split(",") if args.roles else None
    results = orchestrate(args.task, roles, args.output)

    if args.output == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"# Team Output: {results['task']}\n")
        print(f"**Team**: {', '.join(r['name'] for r in results['team'])}")
        print(f"**Time**: {results['timestamp']}\n")

        for member in results["team"]:
            role_id = member["role"]
            print(f"## {member['name']} ({member['description']})\n")
            print(results["outputs"].get(role_id, "[no output]"))
            print()

        print("## Final Synthesis\n")
        print(results.get("final_output", "[no synthesis]"))


if __name__ == "__main__":
    main()
