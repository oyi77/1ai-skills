#!/usr/bin/env python3
"""
skill-graph.py — Skill Dependency Graph Generator

Reads `depends_on` from SKILL.md frontmatter across the repo, builds a
directed dependency graph, detects cycles, and writes reports.

Usage:
    python3 scripts/skill-graph.py                            # Build graph, detect cycles
    python3 scripts/skill-graph.py --json                     # Output as JSON only
    python3 scripts/skill-graph.py --topo                     # Topological order only
    python3 scripts/skill-graph.py --validate                 # Validate all deps exist
"""

import json
import os
import re
import sys
from argparse import ArgumentParser
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_JSON = REPO_ROOT / "SKILLS.json"
REPORTS_DIR = REPO_ROOT / "reports"


def find_skill_dirs() -> list[Path]:
    """Find all directories containing a SKILL.md file."""
    return sorted(REPO_ROOT.rglob("SKILL.md"))


def parse_frontmatter(path: Path) -> dict[str, Any]:
    """Parse YAML frontmatter using PyYAML (already a project dependency)."""
    content = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return {}
    try:
        result = yaml.safe_load(m.group(1))
        return result if isinstance(result, dict) else {}
    except (yaml.YAMLError,):
        return {}


def validate_deps_exist(
    graph: dict[str, list[str]],
    all_skills: set[str],
) -> list[dict[str, Any]]:
    """Validate that all depends_on references point to real skills."""
    issues = []
    for skill, deps in graph.items():
        for dep in deps:
            if dep not in all_skills:
                issues.append({
                    "skill": skill,
                    "depends_on": dep,
                    "type": "missing_dependency",
                    "message": f"Skill '{skill}' depends on '{dep}' which does not exist in SKILLS.json",
                })
    return issues


def detect_cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    """Detect cycles in directed graph using DFS coloring."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {s: WHITE for s in graph}
    parent: dict[str, str | None] = {s: None for s in graph}
    cycles: list[list[str]] = []

    def dfs(node: str, path: list[str]) -> None:
        color[node] = GRAY
        path.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in color:
                color[neighbor] = WHITE
                parent[neighbor] = node
            if color[neighbor] == GRAY:
                # Found a cycle
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles.append(cycle)
            elif color[neighbor] == WHITE:
                dfs(neighbor, path)
        path.pop()
        color[node] = BLACK

    for node in list(graph.keys()):
        if color[node] == WHITE:
            dfs(node, [])

    return cycles


def topological_sort(graph: dict[str, list[str]]) -> list[str]:
    """Kahn's algorithm for topological ordering. Returns empty list if cycles exist."""
    in_degree: dict[str, int] = {s: 0 for s in graph}
    for deps in graph.values():
        for dep in deps:
            if dep in in_degree:
                in_degree[dep] += 1

    queue = deque([s for s, d in in_degree.items() if d == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for dep in graph.get(node, []):
            if dep in in_degree:
                in_degree[dep] -= 1
                if in_degree[dep] == 0:
                    queue.append(dep)

    if len(order) != len(graph):
        return []  # Cycle detected
    return order


def build_graph() -> tuple[dict[str, list[str]], set[str]]:
    """Read all SKILL.md files and build dependency graph from depends_on field."""
    # Load all skill names from SKILLS.json for validation
    with open(SKILLS_JSON) as f:
        data = json.load(f)
    all_skills: set[str] = {s["name"] for s in data["skills"]}

    skill_dirs = find_skill_dirs()
    graph: dict[str, list[str]] = {s: [] for s in all_skills}

    files_with_deps = 0
    total_deps = 0

    for sk_path in skill_dirs:
        fm = parse_frontmatter(sk_path)
        skill_name = fm.get("name", sk_path.parent.name)
        if skill_name not in graph:
            graph[skill_name] = []

        deps = fm.get("depends_on", [])
        if isinstance(deps, str):
            deps = [deps]
        if deps:
            graph[skill_name] = deps
            files_with_deps += 1
            total_deps += len(deps)

    print(f"Skills scanned: {len(skill_dirs)}")
    print(f"Skills with depends_on: {files_with_deps}")
    print(f"Total dependency edges: {total_deps}")
    return graph, all_skills


def main() -> None:
    parser = ArgumentParser(description="Skill Dependency Graph Generator")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output only")
    parser.add_argument("--topo", "-t", action="store_true", help="Topological order only")
    parser.add_argument("--validate", "-v", action="store_true", help="Validate dependencies exist")
    parser.add_argument("--output", "-o", help="Write graph JSON to file (default: reports/skill-graph.json)")
    args = parser.parse_args()

    graph, all_skills = build_graph()

    if args.validate:
        issues = validate_deps_exist(graph, all_skills)
        if issues:
            print(f"\nDependency validation: {len(issues)} issues")
            for iss in issues:
                print(f"  [{iss['type']}] {iss['message']}")
        else:
            print("\nDependency validation: All references resolve to existing skills ✅")
        return

    cycles = detect_cycles(graph)
    topo = topological_sort(graph)

    if args.topo:
        if topo:
            for s in topo:
                print(s)
        else:
            print("ERROR: Cycle detected — topological sort not possible")
        return

    result = {
        "meta": {
            "total_skills": len(graph),
            "skills_with_deps": sum(1 for d in graph.values() if d),
            "total_edges": sum(len(d) for d in graph.values()),
            "has_cycles": len(cycles) > 0,
            "cycle_count": len(cycles),
        },
        "graph": {s: deps for s, deps in graph.items() if deps},
        "cycles": cycles,
        "topological_order": topo if not cycles else None,
    }

    if args.json:
        print(json.dumps(result, indent=2))
        return

    # Default: pretty print
    print(f"\n{'='*60}")
    print(f"Skill Dependency Graph Report")
    print(f"{'='*60}")
    print(f"Total skills:          {result['meta']['total_skills']}")
    print(f"Skills with deps:      {result['meta']['skills_with_deps']}")
    print(f"Total dependency edges: {result['meta']['total_edges']}")
    print(f"Cycles detected:       {result['meta']['cycle_count']}")

    if cycles:
        print(f"\n{'!'*60}")
        print(f"CYCLE DETECTED — {len(cycles)} cycle(s)")
        print(f"{'!'*60}")
        for i, cycle in enumerate(cycles):
            print(f"  Cycle {i+1}: {' → '.join(cycle)}")
    else:
        print("\nNo cycles detected ✅")

    if topo:
        print(f"\nTopological start (first 10): {', '.join(topo[:10])}")
        print(f"Topological end   (last 10):  {', '.join(topo[-10:])}")
    else:
        print("\nTopological sort: NOT AVAILABLE (cycle present)")

    # Write to file
    output_path = args.output or str(REPORTS_DIR / "skill-graph.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nReport written to: {output_path}")


if __name__ == "__main__":
    main()
