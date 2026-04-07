# SharedSkillsLuke

Shared Claude Code skills between Jesse and Luke. Both users can add, update, and sync skills through this repo.

## How It Works

1. **Skills live in `skills/`** — each subdirectory is a complete Claude Code skill (with a `SKILL.md` and optional supporting files)
2. **Daily auto-sync** — a scheduled task runs once per day on each machine, pulling the latest skills from this repo and pushing any local changes back
3. **Two-way sync** — if Jesse updates a skill locally, it gets pushed here. When Luke's sync runs, he picks it up (and vice versa)

## Setup (One-Time)

### 1. Clone the repo

```bash
git clone https://github.com/lotfb86/SharedSkillsLuke.git ~/SharedSkillsLuke
```

### 2. Install the sync skill

```bash
cp -R ~/SharedSkillsLuke/skills/sync-shared-skills ~/.claude/skills/sync-shared-skills
```

### 3. Schedule daily sync

In Claude Code, run:

```
/schedule
```

Create a scheduled task called `sync-shared-skills` that runs the `/sync-shared-skills` skill once daily.

Or manually invoke it anytime:

```
/sync-shared-skills
```

## Adding a New Shared Skill

1. Copy your skill folder into `skills/` in this repo:
   ```bash
   cp -R ~/.claude/skills/my-cool-skill ~/SharedSkillsLuke/skills/my-cool-skill
   ```
2. Commit and push:
   ```bash
   cd ~/SharedSkillsLuke
   git add -A
   git commit -m "Add my-cool-skill"
   git push origin main
   ```
3. The other person's daily sync will pick it up automatically

Or just update the skill locally in `~/.claude/skills/` — the next sync run will detect the change and push it to the repo.

## Repo Structure

```
SharedSkillsLuke/
├── README.md
└── skills/
    ├── sync-shared-skills/    # The sync skill itself
    │   └── SKILL.md
    └── [other-shared-skills]/
        └── SKILL.md
```

## Collaborators

- **Jesse** (lotfb86) — repo owner
- **Luke** (LukeVanValin) — collaborator
