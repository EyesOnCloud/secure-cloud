#!/bin/bash

# ─────────────────────────────────────────────────────────────────────────────
# apply_policy.sh — Inject the Cosign public key and registry into the
# Kyverno policy and apply it to the cluster.
#
# Usage: ./apply_policy.sh <registry_prefix> <cosign_public_key_file>
# Example: ./apply_policy.sh docker.io/myusername cosign.pub
# ─────────────────────────────────────────────────────────────────────────────

set -e

REGISTRY_PREFIX="${1}"
PUBLIC_KEY_FILE="${2:-cosign.pub}"

if [ -z "$REGISTRY_PREFIX" ]; then
    echo "Usage: $0 <registry_prefix> [public_key_file]"
    echo "Example: $0 docker.io/eyesoncloud cosign.pub"
    echo "Example: $0 localhost:5000 cosign.pub"
    exit 1
fi

if [ ! -f "$PUBLIC_KEY_FILE" ]; then
    echo "[ERROR] Public key file not found: $PUBLIC_KEY_FILE"
    echo "Run: cosign generate-key-pair   first"
    exit 1
fi

PUBLIC_KEY_CONTENT=$(cat "$PUBLIC_KEY_FILE")

echo "[*] Applying Kyverno image signature policy..."
echo "    Registry prefix : $REGISTRY_PREFIX"
echo "    Public key file : $PUBLIC_KEY_FILE"
echo ""

# Substitute placeholders and apply
sed \
    -e "s|REGISTRY_PLACEHOLDER|${REGISTRY_PREFIX#docker.io/}|g" \
    -e "s|docker.io/REGISTRY_PLACEHOLDER|${REGISTRY_PREFIX}|g" \
    policies/verify-image-signature.yaml | \
python3 -c "
import sys
content = sys.stdin.read()
key = open('${PUBLIC_KEY_FILE}').read().strip()
# Indent the public key for proper YAML formatting
indented_key = '\n'.join('                      ' + line for line in key.split('\n'))
content = content.replace('PUBLIC_KEY_PLACEHOLDER', indented_key)
print(content)
" | kubectl apply -f -

echo ""
echo "Policy applied"
echo ""
echo "[*] Verifying policy is active..."
kubectl get clusterpolicy verify-image-signature -o wide

echo ""
echo "[*] Policy details:"
kubectl describe clusterpolicy verify-image-signature | grep -A5 "Validation Failure Action\|Match\|Namespace"
