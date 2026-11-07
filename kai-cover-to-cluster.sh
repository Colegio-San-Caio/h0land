#!/bin/bash
# By: kai - cover.jpg -> cluster
# rm cover.jpg, it becomes a cluster

echo "=== [kai] before ==="
ls -lh cover.jpg cover-small.png 2>/dev/null

# 1. Keep the original, don't lose it
cp cover.jpg cover-original.jpg

# 2. rm - the joke
rm cover.jpg
echo "cover.jpg deleted..."

# 3. ...it becomes a cluster
cat > cluster.html <<'HTML'
<!doctype html><html><head><meta charset="utf-8">
<title>kai - cover becomes cluster</title>
<style>
body{background:#000;color:#fff;font-family:monospace;text-align:center}
.cluster{display:grid;grid-template-columns:1fr 1fr;gap:10px;max-width:800px;margin:20px auto}
.node{border:1px solid #76ff03;padding:10px;border-radius:12px}
.node img{width:100%;border-radius:8px}
</style></head><body>
<h1>cover.jpg -&gt; cluster</h1>
<p>1 cover, 4 nodes, all kai</p>
<div class="cluster">
<div class="node">control-plane-0<br><img src="cover-original.jpg"><br>Ready</div>
<div class="node">worker-0<br><img src="cover-original.jpg"><br>Ready</div>
<div class="node">worker-1<br><img src="cover-original.jpg"><br>Ready</div>
<div class="node">worker-2<br><img src="cover-original.jpg"><br>Ready</div>
</div>
<p>kubectl get nodes: 4x Ready</p>
</body></html>
HTML

echo "=== [kai] after ==="
ls -lh cover-original.jpg cluster.html
echo "Open: cluster.html - your cover IS the cluster now"
