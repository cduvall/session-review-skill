#!/usr/bin/env python3
"""Find the latest Claude Code session transcript for the current project.

Locates the most recent .jsonl transcript in ~/.claude/projects/<project-dir>/,
skipping the currently-active session, copies it to .claude/reviews/, and prints
JSON with the paths.
"""

import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


def project_dir_name(project_path: str) -> str:
    """Convert an absolute path to Claude's dash-separated directory name.

    /Users/xian/Documents/dev -> -Users-xian-Documents-dev
    """
    return project_path.replace("/", "-")


def find_latest_transcript(project_path: str) -> dict:
    projects_root = Path.home() / ".claude" / "projects"
    dir_name = project_dir_name(project_path)
    project_dir = projects_root / dir_name

    if not project_dir.is_dir():
        return {"error": f"No Claude project directory found: {project_dir}"}

    # Collect all .jsonl transcript files
    transcripts = sorted(
        project_dir.glob("*.jsonl"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if not transcripts:
        return {"error": f"No transcripts found in {project_dir}"}

    # Skip the most recently modified file — it's the current active session
    if len(transcripts) < 2:
        return {"error": "Only one transcript found (current session). No prior session to review."}

    latest = transcripts[1]

    # Set up review directory
    review_dir = Path(project_path) / ".claude" / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    transcript_copy = review_dir / f"transcript-{timestamp}.jsonl"
    review_path = review_dir / f"review-{timestamp}.md"

    shutil.copy2(latest, transcript_copy)

    return {
        "transcript_path": str(transcript_copy),
        "review_path": str(review_path),
        "timestamp": timestamp,
    }


def main():
    project_path = os.environ.get("PWD", os.getcwd())
    result = find_latest_transcript(project_path)

    if "error" in result:
        print(json.dumps(result))
        sys.exit(1)

    print(json.dumps(result))


if __name__ == "__main__":
    main()
