# login_bcrypt.py

import bcrypt
import json
import os
from datetime import datetime

USERS_FILE = "users.json"
AUDIT_FILE = "audit_log.json"

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                content = f.read()
                if not content.strip():
                    return {}
                return json.loads(content)
        except json.JSONDecodeError:
            return {}
    return {}

def log_event(user_id, event, reason=""):
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "user_id": user_id,
        "event": event,
        "reason": reason
    }

    logs = []
    if os.path.exists(AUDIT_FILE):
        try:
            with open(AUDIT_FILE, "r") as f:
                content = f.read()
                if content.strip():
                    logs = json.loads(content)
        except json.JSONDecodeError:
            logs = []

    logs.append(log_entry)
    with open(AUDIT_FILE, "w") as f:
        json.dump(logs, f, indent=4)

def login_user():
    users = load_users()
    print("=== User Login ===")

    user_input = input("Enter user ID: ").strip().lower()
    password_input = input("Enter password: ").strip()

    # Case-insensitive lookup
    matched_user_id = None
    for uid in users.keys():
        if uid.lower() == user_input:
            matched_user_id = uid
            break

    if matched_user_id is None:
        log_event(user_input, "login_failed", "user not found")
        print("Invalid credentials")
        return None

    user_record = users[matched_user_id]
    stored_hash = user_record.get("password_hash", "").encode()

    if bcrypt.checkpw(password_input.encode(), stored_hash):
        log_event(matched_user_id, "login_success")
        print(f"Login successful! Welcome, {matched_user_id}.")
        # ✅ Return structure expected by access_control.py
        return {
            "username": matched_user_id,
            "data": user_record
        }
    else:
        log_event(matched_user_id, "login_failed", "incorrect password")
        print("Invalid credentials")
        return None

if __name__ == "__main__":
    login_user()
