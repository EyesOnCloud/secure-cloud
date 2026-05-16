import os
import signal
import sys
from flask import Flask, jsonify

app = Flask(__name__)

def handle_sigterm(signum, frame):
    """
    Graceful shutdown handler.
    With exec form CMD and PID 1 = python3, SIGTERM reaches this handler.
    With shell form CMD and PID 1 = /bin/sh, SIGTERM may never reach Python.
    """
    print("[SHUTDOWN] Received SIGTERM — shutting down gracefully", flush=True)
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)

@app.route('/')
def index():
    return jsonify({
        "service": "lab-hardening-demo",
        "version": "secure-2.0",
        "status": "running",
        "security_note": "Running as non-root, minimal image, no hardcoded secrets"
    })

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/info')
def info():
    import os
    return jsonify({
        "running_as_uid": os.getuid(),
        "running_as_gid": os.getgid(),
        "username": os.environ.get("USER", "unknown"),
        "flask_env": os.environ.get("FLASK_ENV", "unknown"),
        "api_key_present": bool(os.environ.get("API_KEY")),
        "note": "UID 1001 = non-root. API_KEY not set in image — must come from orchestrator."
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_ENV', 'production') == 'development'
    print(f"[STARTUP] Starting server on port {port}, debug={debug}", flush=True)
    app.run(host='0.0.0.0', port=port, debug=False)
