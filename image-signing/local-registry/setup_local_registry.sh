#!/bin/bash
set -e

# ─────────────────────────────────────────────────────────────────────────────
# setup_local_registry.sh — Sets up a local Docker registry accessible
# from both the VM and the Kubernetes cluster nodes.
#
# Use this if Docker Hub is not available.
# The registry runs on the VM at port 5000.
# Cluster nodes need to be configured to trust this insecure registry.
# ─────────────────────────────────────────────────────────────────────────────

VM_IP=$(hostname -I | awk '{print $1}')
REGISTRY_PORT=5000
REGISTRY_ADDR="${VM_IP}:${REGISTRY_PORT}"

echo "[*] Setting up local Docker registry at ${REGISTRY_ADDR}"

# Start local registry container
docker container run -d \
    --name local-registry \
    --restart=always \
    -p ${REGISTRY_PORT}:5000 \
    -v /opt/registry-data:/var/lib/registry \
    registry:2

echo "[✓] Local registry running at ${REGISTRY_ADDR}"

echo ""
echo "[*] Configuring Docker daemon on this VM to trust the insecure registry..."
sudo mkdir -p /etc/docker
cat | sudo tee /etc/docker/daemon.json << EOF
{
  "insecure-registries": ["${REGISTRY_ADDR}"]
}
EOF
sudo systemctl restart docker
sleep 5
echo "[✓] Docker daemon reconfigured"

echo ""
echo "════════════════════════════════════════════════════════"
echo " IMPORTANT: You must configure each Kubernetes node to"
echo " trust this insecure registry."
echo ""
echo " Run these commands on EACH cluster node (control-plane"
echo " and both workers):"
echo ""
echo "   for containerd:"
echo "   sudo mkdir -p /etc/containerd"
echo "   Add to /etc/containerd/config.toml:"
echo "   [plugins.\"io.containerd.grpc.v1.cri\".registry.mirrors.\"${REGISTRY_ADDR}\"]"
echo "   endpoint = [\"http://${REGISTRY_ADDR}\"]"
echo "   sudo systemctl restart containerd"
echo ""
echo " Registry address for image tags: ${REGISTRY_ADDR}"
echo " Example: docker image tag myapp:1.0 ${REGISTRY_ADDR}/myapp:1.0"
echo "════════════════════════════════════════════════════════"
