#!/bin/bash
# MAIN.FNT CHECK - Cluster h0land - Lock
# GREEN = 1 Main = 1 Truth, RED = Broken

echo "--- MAIN.FNT CHECK ---"
FILES=$(git ls-tree -r --name-only origin/main)

COUNT_HTML=$(echo "$FILES" | grep -c "index.html$")
COUNT_CSS=$(echo "$FILES" | grep -c "main.css$")
COUNT_JS=$(echo "$FILES" | grep -c "main.js$")
COUNT_SIGNAL=$(echo "$FILES" | grep -c "MAIN.FNT-SIGNAL.md$")

echo "index.html: $COUNT_HTML (must be 1)"
echo "main.css: $COUNT_CSS (must be 1)"
echo "main.js: $COUNT_JS (must be 1)"
echo "SIGNAL: $COUNT_SIGNAL (must be 1)"

if [ "$COUNT_HTML" -eq 1 ] && [ "$COUNT_CSS" -eq 1 ] && [ "$COUNT_JS" -eq 1 ] && [ "$COUNT_SIGNAL" -eq 1 ]; then
  echo "RESULT: 🟢 SIGNAL GREEN - 1 Main = 1 Truth"
else
  echo "RESULT: 🔴 SIGNAL RED - Duplicate or Missing Main!"
  echo "$FILES" | grep -E "index.html|main.css|main.js"
fi
