#!/bin/bash
echo "=== App1 lodash version ==="
cat app1/node_modules/lodash/package.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['version'])"

echo "=== App2 lodash version ==="
cat app2/node_modules/lodash/package.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['version'])"

echo "=== App3 lodash version (if installed as transitive) ==="
ls app3/node_modules/lodash 2>/dev/null && \
    cat app3/node_modules/lodash/package.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['version'])" || \
    echo "lodash not found in node_modules"
