import os
import sys
import json
import shutil
from pathlib import Path


def get_skill_index():
    skill_index_path = Path(__file__).parent / "skill-index.json"
    if skill_index_path.exists():
        with open(skill_index_path, "r") as f:
            return json.load(f)
    return {"skills": [], "teams": []}


def get_target_directory():
    home = os.path.expanduser("~")
    candidates = [
        os.path.join(home, ".opencode", "skills"),
        os.path.join(home, ".claude", "skills"),
        os.path.join(home, ".openclaw", "workspace", "skills"),
        os.path.join(os.getcwd(), "skills"),
    ]

    for candidate in candidates:
        parent = os.path.dirname(candidate)
        if os.path.exists(parent) or candidate == candidates[-1]:
            return candidate

    return candidates[0]


def get_local_skills():
    root = Path(__file__).parent.parent
    categories = [
        "core",
        "development",
        "marketing",
        "sales",
        "content",
        "research",
        "operations",
        "productivity",
        "automation",
        "trading",
        "growth",
    ]
    skills = []

    for cat in categories:
        cat_path = root / cat
        if cat_path.exists():
            for entry in cat_path.iterdir():
                if entry.is_dir():
                    skill_md = entry / "SKILL.md"
                    if skill_md.exists():
                        skills.append(
                            {
                                "name": entry.name,
                                "path": str(entry),
                                "category": cat,
                                "source": "local",
                            }
                        )

    return skills


def copy_directory(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest, exist_ok=True)

    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dest_item = os.path.join(dest, item)

        if os.path.isdir(src_item):
            copy_directory(src_item, dest_item)
        else:
            shutil.copy2(src_item, dest_item)


def install_skills():
    print("Loading skill index...")
    skill_index = get_skill_index()
    local_skills = [
        s for s in skill_index.get("skills", []) if s.get("source") == "local"
    ]
    external_skills = [
        s for s in skill_index.get("skills", []) if s.get("source") == "external"
    ]

    print(
        f"Found {len(local_skills)} local skills and {len(external_skills)} external skills"
    )
    print("")

    target_dir = get_target_directory()
    print(f"Target directory: {target_dir}")
    print("")

    if not os.path.exists(target_dir):
        print("Creating skills directory...")
        os.makedirs(target_dir, exist_ok=True)

    skills = get_local_skills()
    print(f"Installing {len(skills)} local skills...\n")

    installed = 0
    skipped = 0

    for skill in skills:
        cat_dir = os.path.join(target_dir, skill["category"])
        dest_path = os.path.join(cat_dir, skill["name"])

        try:
            if not os.path.exists(cat_dir):
                os.makedirs(cat_dir, exist_ok=True)

            if not os.path.exists(dest_path):
                copy_directory(skill["path"], dest_path)
                print(f"[+] {skill['category']}/{skill['name']}")
                installed += 1
            else:
                print(f"[=] {skill['category']}/{skill['name']} (already exists)")
                skipped += 1
        except Exception as e:
            print(f"[-] {skill['category']}/{skill['name']} - {str(e)}")

    print("")
    print("Installation complete!")
    print(f"Installed: {installed} skills")
    print(f"Skipped: {skipped} skills (already installed)")
    print("")
    print(f"Skills installed to: {target_dir}")
    print("")
    print("Usage: Reference skills by name in your AI agent")
    print("Example: 'Use the brainstorming skill to plan this project'")
    print("")


def list_skills():
    skill_index = get_skill_index()
    skills = skill_index.get("skills", [])
    teams = skill_index.get("teams", [])

    print("1ai-skills-bundle")
    print("=" * 40)
    print(f"Total Skills: {len(skills)}")

    local_skills = [s for s in skills if s.get("source") == "local"]
    external_skills = [s for s in skills if s.get("source") == "external"]

    print(f"  Local: {len(local_skills)}")
    print(f"  External: {len(external_skills)}")
    print("")

    categories = {}
    for skill in skills:
        domains = skill.get("domains", [])
        if domains:
            domain = domains[0]
        else:
            domain = "other"

        if domain not in categories:
            categories[domain] = []
        categories[domain].append(skill)

    print("Skills by Category:")
    print("")

    for category in sorted(categories.keys()):
        print(f"  {category.upper()}")
        for skill in categories[category]:
            source = "(local)" if skill.get("source") == "local" else "(external)"
            print(f"    - {skill['name']} {source}")
        print("")


def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "list":
            list_skills()
        elif command == "install":
            install_skills()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python install.py [list|install]")
    else:
        install_skills()


if __name__ == "__main__":
    main()
