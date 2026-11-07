#!/bin/sh
echo "bluh: checking site-index..."
grep -q "og:image" index.html && echo "OK og:image" || echo "FAIL og:image missing"
[ -f cover.png ] && echo "OK cover.png" || echo "FAIL cover.png missing"
[ -f cover.jpg ] && echo "FAIL cover.jpg exists - rm it" || echo "OK no cover.jpg"
ls *.bak *.BAK 2>/dev/null && echo "FAIL .bak exists" || echo "OK no .bak"
cmp -s index.html main.html && echo "OK main.html synced" || echo "FAIL main.html != index.html - cp index.html main.html"
echo "bluh: done"
