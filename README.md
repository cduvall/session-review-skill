# session-review-skill

A Claude Code skill that reviews the most recent prior session transcript and produces a structured review covering outcomes, failures, patterns, and rule proposals.

## Usage

After deploying, invoke in any Claude Code session:

```
/session-review
```

## Deploying

```
make deploy
```

This copies the skill files to `~/.claude/skills/session-review/` and registers the necessary permissions in `~/.claude/settings.json`.

## Structure

```
skills/session-review/
  SKILL.md              # Skill definition and instructions
  scripts/
    find_transcript.py  # Locates the latest prior session transcript
scripts/
  deploy.sh             # Installs skill to ~/.claude/skills/
```
