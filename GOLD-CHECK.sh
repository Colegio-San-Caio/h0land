#!/bin/bash
# GOLD CHECK - Vault, NOT Main
echo "--- GOLD VAULT CHECK ---"
git fetch origin
FILES=$(git ls-tree -r --name-only origin/main)
TOTAL=$(echo "$FILES" | wc -l)
HTML=$(echo "$FILES" | grep -c "\.html$")
PY=$(echo "$FILES" | grep -c "\.py$")
HAS_SITEMAP=$(echo "$FILES" | grep -c "sitemap.xml$")
HAS_ROBOTS=$(echo "$FILES" | grep -c "robots.txt$")
echo "Total files: $TOTAL"
echo "HTML files: $HTML"
echo "Python files: $PY"
echo "sitemap.xml: $HAS_SITEMAP (must be 1)"
echo "robots.txt: $HAS_ROBOTS (must be 1)"
if [ "$TOTAL" -gt 10 ] && [ "$HAS_SITEMAP" -eq 1 ] && [ "$HAS_ROBOTS" -eq 1 ]; then
  echo "RESULT: 🟡 GOLD VAULT GREEN - Archive intact, $TOTAL files"
else
  echo "RESULT: 🔴 GOLD VAULT RED - Files missing!"
fi
