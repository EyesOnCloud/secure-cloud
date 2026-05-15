"""
Internal Financial Reporting Application
This application demonstrates a realistic codebase that uses
multiple third-party packages — each potentially carrying vulnerabilities.
"""

from flask import Flask, request, jsonify, session
import os

# Import application modules
from app.report_generator import generate_report
from app.file_processor import process_upload
from app.session_manager import create_session, validate_session

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "running", "app": "Financial Reporting API"})


@app.route('/login', methods=['POST'])
def login():
    """Authenticate user and create session."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Simplified auth — in real app this queries a database
    if username == 'analyst' and password == 'reportpass':
        token = create_session(username)
        return jsonify({"token": token, "message": "Login successful"})
    return jsonify({"error": "Invalid credentials"}), 401


@app.route('/report', methods=['POST'])
def report():
    """Generate a financial report from submitted data."""
    auth_header = request.headers.get('Authorization', '')
    if not validate_session(auth_header):
        return jsonify({"error": "Authentication required"}), 401

    data = request.get_json()
    report_type = data.get('type', 'summary')
    period = data.get('period', 'Q1-2024')

    result = generate_report(report_type, period, data.get('config', {}))
    return jsonify(result)


@app.route('/upload', methods=['POST'])
def upload():
    """Process an uploaded data file."""
    auth_header = request.headers.get('Authorization', '')
    if not validate_session(auth_header):
        return jsonify({"error": "Authentication required"}), 401

    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    uploaded_file = request.files['file']
    result = process_upload(uploaded_file)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
