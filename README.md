# Cursor setup

This repo contains personal Cursor skills, subagents, and always-applied rules.

## Install

Clone the repo:

```bash
mkdir -p ~/code
git clone git@github.com:caiomarxm/skills.git ~/code/skills
```

Link each Cursor directory to the repo. Existing directories are backed up:

```bash
mkdir -p ~/.cursor
backup=$(date +%Y%m%d-%H%M%S)

for name in skills agents rules; do
  target="$HOME/.cursor/$name"
  if [ -e "$target" ] || [ -L "$target" ]; then
    mv "$target" "$target.backup-$backup"
  fi
  ln -s "$HOME/code/skills/$name" "$target"
done
```

Open a new Cursor chat. Confirm that the skills, subagents, and rules appear.

## Update

```bash
git -C ~/code/skills pull
```
