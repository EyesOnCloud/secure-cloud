#!/bin/bash

# ─────────────────────────────────────────────────────────────────────────────
# compare.sh — Compare insecure vs secure image metrics
# Run after building both images to see the full impact of hardening
# ─────────────────────────────────────────────────────────────────────────────

INSECURE_IMAGE="app-insecure"
SECURE_IMAGE="app-secure"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo " Docker Image Security Hardening Comparison Report"
echo " $(date)"
echo "═══════════════════════════════════════════════════════════════"

# ── Image sizes ───────────────────────────────────────────────────────────────
echo ""
echo "── IMAGE SIZE COMPARISON ────────────────────────────────────────"
INSECURE_SIZE=$(docker image inspect $INSECURE_IMAGE \
    --format='{{.Size}}' 2>/dev/null | \
    awk '{printf "%.1f MB", $1/1024/1024}')
SECURE_SIZE=$(docker image inspect $SECURE_IMAGE \
    --format='{{.Size}}' 2>/dev/null | \
    awk '{printf "%.1f MB", $1/1024/1024}')

echo " Insecure image : $INSECURE_SIZE"
echo " Secure image   : $SECURE_SIZE"

# ── Layer count ───────────────────────────────────────────────────────────────
echo ""
echo "── LAYER COUNT ──────────────────────────────────────────────────"
INSECURE_LAYERS=$(docker image inspect $INSECURE_IMAGE \
    --format='{{len .RootFS.Layers}}' 2>/dev/null)
SECURE_LAYERS=$(docker image inspect $SECURE_IMAGE \
    --format='{{len .RootFS.Layers}}' 2>/dev/null)
echo " Insecure image : $INSECURE_LAYERS layers"
echo " Secure image   : $SECURE_LAYERS layers"

# ── User check ────────────────────────────────────────────────────────────────
echo ""
echo "── PROCESS USER ─────────────────────────────────────────────────"
INSECURE_USER=$(docker image inspect $INSECURE_IMAGE \
    --format='{{.Config.User}}' 2>/dev/null)
SECURE_USER=$(docker image inspect $SECURE_IMAGE \
    --format='{{.Config.User}}' 2>/dev/null)

INSECURE_USER_DISPLAY="${INSECURE_USER:-root (UID 0) — DANGEROUS}"
SECURE_USER_DISPLAY="${SECURE_USER:-unknown}"
echo " Insecure image : $INSECURE_USER_DISPLAY"
echo " Secure image   : $SECURE_USER_DISPLAY"

# ── Exposed ports ─────────────────────────────────────────────────────────────
echo ""
echo "── EXPOSED PORTS ────────────────────────────────────────────────"
echo " Insecure image:"
docker image inspect $INSECURE_IMAGE \
    --format='{{json .Config.ExposedPorts}}' 2>/dev/null | jq -r 'keys[]' | \
    sed 's/^/   /'
echo " Secure image:"
docker image inspect $SECURE_IMAGE \
    --format='{{json .Config.ExposedPorts}}' 2>/dev/null | jq -r 'keys[]' | \
    sed 's/^/   /'

# ── Environment variables ──────────────────────────────────────────────────────
echo ""
echo "── ENVIRONMENT VARIABLES (checking for secrets) ─────────────────"
echo " Insecure image ENV:"
docker image inspect $INSECURE_IMAGE \
    --format='{{json .Config.Env}}' 2>/dev/null | jq -r '.[]' | \
    sed 's/^/   /'
echo ""
echo " Secure image ENV:"
docker image inspect $SECURE_IMAGE \
    --format='{{json .Config.Env}}' 2>/dev/null | jq -r '.[]' | \
    sed 's/^/   /'

# ── Health check ──────────────────────────────────────────────────────────────
echo ""
echo "── HEALTH CHECK ─────────────────────────────────────────────────"
INSECURE_HC=$(docker image inspect $INSECURE_IMAGE \
    --format='{{.Config.Healthcheck}}' 2>/dev/null)
SECURE_HC=$(docker image inspect $SECURE_IMAGE \
    --format='{{json .Config.Healthcheck}}' 2>/dev/null)
echo " Insecure: ${INSECURE_HC:-none — orchestrator cannot detect app failures}"
echo " Secure  : $SECURE_HC"

# ── CVE summary ───────────────────────────────────────────────────────────────
echo ""
echo "── VULNERABILITY SUMMARY ────────────────────────────────────────"
echo " Running Trivy scans (this may take a moment)..."
echo ""

echo " INSECURE image CVE summary:"
trivy image --severity CRITICAL,HIGH,MEDIUM,LOW \
    --format table \
    --no-progress \
    $INSECURE_IMAGE 2>/dev/null | \
    grep -E "Total:|CRITICAL|HIGH|MEDIUM|LOW" | tail -5 | \
    sed 's/^/   /'

echo ""
echo " SECURE image CVE summary:"
trivy image --severity CRITICAL,HIGH,MEDIUM,LOW \
    --format table \
    --no-progress \
    $SECURE_IMAGE 2>/dev/null | \
    grep -E "Total:|CRITICAL|HIGH|MEDIUM|LOW" | tail -5 | \
    sed 's/^/   /'

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo " End of comparison report"
echo "═══════════════════════════════════════════════════════════════"
