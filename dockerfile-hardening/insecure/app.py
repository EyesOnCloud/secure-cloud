import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "service": "lab-hardening-demo",
        "version": "insecure-1.0",
        "status": "running",
        "warning": "This image is intentionally insecure"
    })

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/env-leak')
def env_leak():
    # This endpoint demonstrates why ENV secrets are dangerous
    # In the insecure version, environment variables with secrets are readable
    return jsonify({
        "api_key": os.environ.get("API_KEY", "not set"),
        "database_url": os.environ.get("DATABASE_URL", "not set"),
        "note": "In a real attack, this data is extracted via RCE or SSRF"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
