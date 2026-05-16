import os
import hashlib
import platform
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "service": "lab-signing-demo",
        "version": os.environ.get("APP_VERSION", "1.0"),
        "status": "running",
        "message": "This image was signed with Cosign and verified by Kyverno"
    })

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/info')
def info():
    return jsonify({
        "hostname": platform.node(),
        "python_version": platform.python_version(),
        "image_signed": True,
        "signing_tool": "Cosign",
        "policy_enforcer": "Kyverno"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
