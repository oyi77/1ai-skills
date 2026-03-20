#!/usr/bin/env python3
"""Project State Manager - YAML-based project and task tracking."""
import sys, os, json
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    # Fallback: minimal YAML handling without pyyaml
    yaml = None

WORKSPACE = Path(__file__).resolve().parents[3]
PROJECTS_DIR = Path(__file__).resolve().parents[1] / "projects"
STATE_FILE = PROJECTS_DIR / "STATE.yaml"


def _load_state():
    """Load the STATE.yaml file."""
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    if not STATE_FILE.exists():
        return {"projects": {}}
    content = STATE_FILE.read_text()
    if yaml:
        return yaml.safe_load(content) or {"projects": {}}
    else:
        return json.loads(content) if content.strip() else {"projects": {}}


def _save_state(state):
    """Save state to STATE.yaml."""
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    if yaml:
        STATE_FILE.write_text(yaml.dump(state, default_flow_style=False, allow_unicode=True))
    else:
        STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def create_project(name):
    """Create a new project."""
    state = _load_state()
    if name in state["projects"]:
        return f"Project '{name}' already exists."
    state["projects"][name] = {
        "created": datetime.now().isoformat(),
        "status": "active",
        "tasks": [],
    }
    _save_state(state)
    return f"Project '{name}' created."


def add_task(project, task, owner="unassigned", deadline=None):
    """Add a task to a project."""
    state = _load_state()
    if project not in state["projects"]:
        return f"Project '{project}' not found."
    task_entry = {
        "task": task,
        "owner": owner,
        "deadline": deadline,
        "status": "todo",
        "created": datetime.now().isoformat(),
    }
    state["projects"][project]["tasks"].append(task_entry)
    _save_state(state)
    return f"Task added to '{project}': {task}"


def update_status(project, task_name, status):
    """Update a task's status."""
    state = _load_state()
    if project not in state["projects"]:
        return f"Project '{project}' not found."
    for task in state["projects"][project]["tasks"]:
        if task["task"] == task_name:
            task["status"] = status
            task["updated"] = datetime.now().isoformat()
            _save_state(state)
            return f"Task '{task_name}' → {status}"
    return f"Task '{task_name}' not found in '{project}'."


def get_summary(project):
    """Get project summary."""
    state = _load_state()
    if project not in state["projects"]:
        return f"Project '{project}' not found."
    proj = state["projects"][project]
    tasks = proj.get("tasks", [])
    total = len(tasks)
    done = sum(1 for t in tasks if t["status"] == "done")
    in_progress = sum(1 for t in tasks if t["status"] == "in_progress")
    todo = sum(1 for t in tasks if t["status"] == "todo")
    summary = f"Project: {project}\nStatus: {proj['status']}\nTasks: {total} total — {done} done, {in_progress} in progress, {todo} todo\n"
    for t in tasks:
        summary += f"  [{t['status']}] {t['task']} (owner: {t['owner']})\n"
    return summary


def list_projects():
    """List all projects."""
    state = _load_state()
    if not state["projects"]:
        return "No projects found."
    output = "Projects:\n"
    for name, proj in state["projects"].items():
        task_count = len(proj.get("tasks", []))
        output += f"  - {name} [{proj['status']}] ({task_count} tasks)\n"
    return output


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Project State Manager")
    parser.add_argument("--action", choices=["create", "add_task", "update", "summary", "list"], required=True)
    parser.add_argument("--project", help="Project name")
    parser.add_argument("--task", help="Task description")
    parser.add_argument("--owner", default="unassigned", help="Task owner")
    parser.add_argument("--deadline", help="Task deadline (YYYY-MM-DD)")
    parser.add_argument("--status", help="New status for update action")
    args = parser.parse_args()

    if args.action == "create":
        print(create_project(args.project))
    elif args.action == "add_task":
        print(add_task(args.project, args.task, args.owner, args.deadline))
    elif args.action == "update":
        print(update_status(args.project, args.task, args.status))
    elif args.action == "summary":
        print(get_summary(args.project))
    elif args.action == "list":
        print(list_projects())
