---
name: sync-shared-skills
description: >
  Sync shared skills from the SharedSkillsLuke GitHub repo. Checks the repo for changes,
  pulls the latest, and copies any new or updated skill folders into ~/.claude/skills/.
  Also pushes any local skill changes (for skills tracked in the repo) back to GitHub.
  Designed to run daily as a scheduled task to keep Jesse and Luke in sync.
  Triggers on: "sync skills", "sync shared skills", "pull shared skills", "push shared skills",
  "update shared skills", "skill sync".
allowed-tools: Bash, Read, Write, Glob
---

# Sync Shared Skills

## What This Does

Keeps your local Claude Code skills in sync with the SharedSkillsLuke GitHub repo. This is a two-way sync:

1. **Pull**: Fetches the latest from GitHub and copies any new/updated shared skills into `~/.claude/skills/`
2. **Push**: If any of the locally-tracked shared skills have been modified, commits and pushes them back to the repo

This enables Jesse and Luke to share skills — either person can update a skill, push it, and the other picks it up automatically.

## Steps

### Step 1: Pull latest from GitHub

```bash
cd /Users/jesseanglen/SharedSkillsLuke
export PATH="/opt/homebrew/bin:$PATH"
git fetch origin
git pull origin main --rebase 2>/dev/null || git pull origin main
```

### Step 2: Identify shared skills

List all skill directories inside `/Users/jesseanglen/SharedSkillsLuke/skills/`. Each subdirectory is a shared skill.

### Step 3: Sync FROM repo TO local skills

For each skill directory found in `/Users/jesseanglen/SharedSkillsLuke/skills/`:

1. Compare the repo version with `~/.claude/skills/<skill-name>/`
2. If the repo version is newer (based on file content diff), copy it to `~/.claude/skills/<skill-name>/`
3. If the skill doesn't exist locally yet, copy the entire folder to `~/.claude/skills/`
4. Preserve any local files that don't exist in the repo version (don't delete extras)

Use this approach:
```bash
# For each skill dir in the repo
for skill_dir in /Users/jesseanglen/SharedSkillsLuke/skills/*/; do
  skill_name=$(basename "$skill_dir")
  # Skip the sync skill itself — it's managed separately
  local_dir="$HOME/.claude/skills/$skill_name"

  if [ ! -d "$local_dir" ]; then
    echo "NEW SKILL: Installing $skill_name"
    cp -R "$skill_dir" "$local_dir"
  else
    # Check if repo version differs from local
    if ! diff -rq "$skill_dir" "$local_dir" > /dev/null 2>&1; then
      echo "UPDATED: Syncing $skill_name"
      cp -R "$skill_dir"* "$local_dir/"
    else
      echo "UP TO DATE: $skill_name"
    fi
  fi
done
```

### Step 4: Sync FROM local skills TO repo (push changes)

For each skill that already exists in the repo's `skills/` directory, check if the local version in `~/.claude/skills/` has changes that aren't in the repo yet:

```bash
for skill_dir in /Users/jesseanglen/SharedSkillsLuke/skills/*/; do
  skill_name=$(basename "$skill_dir")
  local_dir="$HOME/.claude/skills/$skill_name"

  if [ -d "$local_dir" ]; then
    if ! diff -rq "$local_dir" "$skill_dir" > /dev/null 2>&1; then
      echo "LOCAL CHANGES: Pushing $skill_name back to repo"
      cp -R "$local_dir"/* "$skill_dir/"
    fi
  fi
done
```

### Step 5: Commit and push any changes

```bash
cd /Users/jesseanglen/SharedSkillsLuke
git add -A
if ! git diff --cached --quiet; then
  git commit -m "Auto-sync: update shared skills $(date +%Y-%m-%d)"
  git push origin main
  echo "Changes pushed to GitHub"
else
  echo "No changes to push"
fi
```

### Step 6: Report

Print a summary:
- Skills synced (pulled from repo)
- Skills pushed (local changes sent to repo)
- Any errors encountered
- Timestamp of sync

## Important

- The repo lives at `/Users/jesseanglen/SharedSkillsLuke/`
- GitHub repo: `lotfb86/SharedSkillsLuke`
- This skill itself lives in the repo at `skills/sync-shared-skills/`
- **Never delete** a local skill that isn't in the repo — only add/update
- If there's a merge conflict, prefer the newer version (by timestamp) and flag it in the report
- The sync skill should also be installed to `~/.claude/skills/sync-shared-skills/` so it can be invoked manually
