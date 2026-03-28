#!/usr/bin/env bash
# add_skill.sh - Create a new skill skeleton
# Usage: add_skill.sh <skill-name> <category>
# Category one of: automation marketing content trading research utils
set -e
if [ $# -ne 2 ]; then
  echo "Usage: $0 <skill-name> <category>"
  exit 1
fi
SKILL=$1
CAT=$2
TARGET="$BASE/$CAT/$SKILL"
if [ -e "$TARGET" ]; then
  echo "Skill $SKILL already exists in $CAT"
  exit 1
fi
mkdir -p "$TARGET"
cat > "$TARGET/SKILL.md" <<MD
# $SKILL – Skill description

## Overview
Describe what this skill does.

## Usage
```
openclaw skill run $SKILL "<args>"
```
MD
chmod +x "$BASE/utils/add_skill.sh"
