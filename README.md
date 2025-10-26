# User Registration & Login (bcrypt)

Small utilities to register users (register_bcrypt.py) and authenticate users (login_bcrypt.py) using bcrypt-hashed passwords and a simple JSON store.

## Contents
- register_bcrypt.py — interactive user registration (creates/updates users.json)
- login_bcrypt.py — interactive login that verifies bcrypt hashes and appends audit events to audit_log.json
- users.json — user datastore (created/managed by scripts)
- audit_log.json — append-only audit log (created/managed by login_bcrypt.py)

## Requirements
- Python 3.8+
- pip
- bcrypt Python package

## Setup (inside the VM / on macOS)
1. Open a terminal and change to project directory:
   --> sh

2. Create and activate a virtual environment
   --> python3 -m venv .venv
   --> source .venv/bin/activate
3. Install dependency
   --> pip install bcrypt

## Run
1. Register a new user
   --> python3 register_bcrypt.py
2. Login
   --> python3 login_bcrypt.py

Password policy
Passwords must:

be at least 8 characters
contain at least one uppercase letter
contain at least one lowercase letter
contain at least one digit
contain at least one special character (one of @$!%*?&)
Regex used (in code):

## JSON storage formats (examples)
users.json

{
  "alice": {
    "password_hash": "$2b$12$...bcrypt-hash...",
    "role": "Cashier",
    "department": "A"
  },
  "bob": {
    "password_hash": "$2b$12$...bcrypt-hash...",
    "role": "Manager",
    "department": "B"
  }
}

audit_log.json (append-only list)

[
  {
    "timestamp": "2025-10-24T12:34:56.789012",
    "user_id": "alice",
    "event": "login_success",
    "reason": ""
  },
  {
    "timestamp": "2025-10-24T12:35:10.123456",
    "user_id": "unknown",
    "event": "login_failed",
    "reason": "user not found"
  }
]

