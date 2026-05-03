# Publish to GitHub

## Option A — use GitHub CLI (recommended)

Prerequisite: log in first.

```bash
gh auth login
```

Then:

```bash
cd /Users/cyq/clawd/projects/gptr-workspace-upgrade
git init
git add .
git commit -m "feat: add GPT Researcher workspace upgrade proposal"
gh repo create gptr-workspace-upgrade --public --source=. --remote=origin --push
```

If you want a private repo, change `--public` to `--private`.

## Option B — create the repo on GitHub web first

1. Create a new empty repository on GitHub
2. Then run:

```bash
cd /Users/cyq/clawd/projects/gptr-workspace-upgrade
git init
git add .
git commit -m "feat: add GPT Researcher workspace upgrade proposal"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## Recommended repository description

Proposal and technical design for evolving GPT Researcher into a continuous research workspace inspired by DeepTutor-style workflow organization.

## Good next files to add later

- `.gitignore`
- `LICENSE`
- `docs/decision-log.md`
- `docs/example-schemas.md`
- `assets/architecture-diagram.png`
