---
name: session-review
description: "Run a session review."
version: "1.0"
allowed-tools: "Bash, Read, Write"
user-invocable: true
---

# Session Review

Review the most recent prior session transcript and produce a structured review.

Follow these steps exactly:

**Step 1: Find the latest transcript**

Run:
```
python3 ~/.claude/skills/session-review/scripts/find_transcript.py
```

Parse the JSON output. If the script exits non-zero, stop and report the error to the user.

Extract `transcript_path`, `review_path`, and `timestamp` from the output.

**Step 2: Read the transcript**

Use the Read tool to read the file at `transcript_path`.

**Step 3: Read project CLAUDE.md**

If a `CLAUDE.md` file exists in the project root (`$PWD/CLAUDE.md`), read it. This provides context for rule proposals and removals.

**Step 4: Produce the review**

Analyze the session transcript and produce a structured review with these sections:

1. **Outcome**: Did the session achieve its goals? What's incomplete?
2. **Failures**: What went wrong? Root causes?
3. **Patterns**: Any recurring issues or effective approaches?
4. **Rule proposals**: Specific, actionable additions for CLAUDE.md. Format as exact text ready to append.
5. **Rule removals**: Specific CLAUDE.md rules that should be removed as they are not benefitting the success of the work being performed. Include rationale.
6. **Skill gaps**: Anything that should become a reusable skill?

**Step 5: Write the review**

Use the Write tool to write the review to the `review_path` from Step 1.

**Step 6: Confirm**

Output: `Review written to <review_path>`
