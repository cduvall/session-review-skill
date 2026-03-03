#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SKILLS_ROOT="$HOME/.claude/skills"

echo "Deploying session-review skill..."

# --- session-review ---
SESSION_DIR="$SKILLS_ROOT/session-review"
SESSION_SRC="$PROJECT_ROOT/skills/session-review"
mkdir -p "$SESSION_DIR/scripts"

cp "$SESSION_SRC/SKILL.md" "$SESSION_DIR/"
cp "$SESSION_SRC/scripts/find_transcript.py" "$SESSION_DIR/scripts/"

echo "  Installed session-review skill to $SESSION_DIR"

# --- Add permissions to ~/.claude/settings.json ---
python3 - <<'PYEOF'
import json
from pathlib import Path

settings_path = Path.home() / ".claude" / "settings.json"
settings_path.parent.mkdir(parents=True, exist_ok=True)

settings = {}
if settings_path.exists():
    try:
        settings = json.loads(settings_path.read_text())
    except json.JSONDecodeError:
        pass

allow = settings.setdefault("permissions", {}).setdefault("allow", [])
entries = [
    "Bash(python3 */.claude/skills/session-review/scripts/*)",
]
changed = False
for entry in entries:
    if entry not in allow:
        allow.append(entry)
        changed = True
        print(f"  Added to settings.json: {entry}")
    else:
        print(f"  Already in settings.json: {entry}")

if changed:
    settings_path.write_text(json.dumps(settings, indent=2) + "\n")
PYEOF

echo ""
echo "Done. Available skills:"
echo "  /session-review"
