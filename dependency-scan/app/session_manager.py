"""
Session Manager Module
Handles JWT token creation and validation.

CRITICAL CVE NOTE:
PyJWT 1.7.2 (used here) has a critical vulnerability:
CVE-2022-29217 — Algorithm confusion attack.
In version 1.x, jwt.decode() does not enforce the algorithm
parameter strictly. An attacker can craft a token using the
'none' algorithm and it may be accepted without signature verification.

Here it appears as a SUPPLY CHAIN issue — the vulnerability is
in the library version, not in this application's code.
The code looks correct but the library betrays it.
"""

import jwt
import datetime
import os

SECRET_KEY = os.environ.get('JWT_SECRET', 'reporting-app-secret-2024')


def create_session(username: str) -> str:
    """
    Create a JWT session token for the authenticated user.
    Returns a signed JWT string.
    """
    payload = {
        'sub': username,
        'username': username,
        'role': 'analyst',
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }
    # PyJWT 1.x encode returns bytes in some versions, str in others
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


def validate_session(auth_header: str):
    """
    Validate a JWT session token from the Authorization header.

    VULNERABILITY: In PyJWT 1.7.2, the algorithms parameter here
    does not fully protect against algorithm confusion in all edge cases.
    Upgrade to PyJWT 2.x which has a completely rewritten and hardened
    verification path.
    """
    if not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded
    except Exception:
        return None
