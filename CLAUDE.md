# MAIN - MOSFETQ Gesamtwerk V2.2 - KAI OLAF KETELHUT

## What is this?
GitHub Pages site. Repo: kaiolafketelhut/kaiolafketelhut.github.io
Live: https://kaiolafketelhut.github.io/index.html

## HARD RULES - never break these
1. KNOWN = 60 unique, 0 doubles, sorted A-Z. ISMS box shows KNOWN.
2. Cover is cover.png (518K). NEVER cover.jpg. cover.jpg is banned.
3. og:image must be in <head>, must point to https://kaiolafketelhut.github.io/cover.png
4. NO *.bak / *.BAK files. Ever. Use .gitignore.
5. main.html must ALWAYS equal index.html. Hook auto-syncs it.

## Agents
- bluh = checker agent. Run: ./bluh.sh
- bluh definition: claude/agents/bluh.md

## Hooks
- .git/hooks/pre-commit = blocks .bak + cover.jpg, syncs main.html

## Commands
- Check: ./bluh.sh
- Push: git add index.html main.html; git commit -m "..."; git push
- Test preview: open link in incognito, or add ?v=2

## Other repo
- potential-octo-garbanzo / fnt/MAIN.FNT = font data, already pushed. Do not mix with this repo.
