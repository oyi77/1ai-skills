#!/usr/bin/env python3
"""
Auto-add missing anatomy sections to SKILL.md files.
Adds: When NOT to Use, Common Rationalizations, Red Flags, Verification
"""
import os
import re
from pathlib import Path

SKILLS_DIR = Path("/home/openclaw/projects/1ai-skills")

def has_section(content, section_name):
    """Check if section exists in content."""
    pattern = rf"^## {re.escape(section_name)}$"
    return re.search(pattern, content, re.MULTILINE) is not None

def add_missing_sections(file_path):
    """Add missing sections to a SKILL.md file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find where to insert sections (before last --- or Related Skills)
    sections_to_add = []
    
    if not has_section(content, "When NOT to Use"):
        sections_to_add.append(("When NOT to Use", """## When NOT to Use

- [TODO: Add specific exclusion cases for this skill]
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

"""))
    
    if not has_section(content, "Common Rationalizations"):
        sections_to_add.append(("Common Rationalizations", """## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

"""))
    
    if not has_section(content, "Red Flags"):
        sections_to_add.append(("Red Flags", """## Red Flags

- [TODO: Add behavioral signs the skill is being violated]
- Watch for shortcuts and skipped steps

"""))
    
    if not has_section(content, "Verification"):
        sections_to_add.append(("Verification", """## Verification

After completing this skill, confirm:

- [ ] [TODO: Add specific evidence-based checklist items]
- [ ] All required outputs generated
- [ ] Success criteria met

"""))
    
    if not sections_to_add:
        return False
    
    # Insert before "## Related Skills" or end of file
    insert_marker = "## Related Skills"
    if insert_marker in content:
        idx = content.index(insert_marker)
        insert_text = "\n" + "".join(s[1] for s in sections_to_add)
        content = content[:idx] + insert_text + content[idx:]
    else:
        # Append at end
        content += "\n" + "".join(s[1] for s in sections_to_add)
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    return True

def main():
    updated = 0
    skipped = 0
    
    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        try:
            if add_missing_sections(skill_md):
                print(f"✓ Updated: {skill_md.relative_to(SKILLS_DIR)}")
                updated += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"✗ Error: {skill_md}: {e}")
    
    print(f"\nDone: {updated} updated, {skipped} already complete.")

if __name__ == "__main__":
    main()
