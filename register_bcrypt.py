
#Description: User registration module with bcrypt password hashing and password policy enforcement.

import bcrypt
import json
import os
import re

USERS_FILE = "users.json"

# Password policy regex: at least 8 characters, uppercase, lowercase, number, special char
PASSWORD_POLICY_REGEX = re.compile(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
)
def load_users():
    """Load users from JSON file. If the file is empty or invalid JSON, return an empty dict."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            content = f.read()
            if not content.strip():
                # empty file -> treat as no users
                return {}
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # invalid JSON -> treat as no users (or optionally reset file)
                return {}
    return {}

def save_users(users):
    """Save users to JSON file."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def password_is_valid(password):
    """Check if the password meets policy."""
    return PASSWORD_POLICY_REGEX.match(password)

def register_user():
    users = load_users()
    print("=== User Registration ===")
    
    while True:
        user_id = input("Enter a unique user ID: ").strip()
        if user_id in users:
            print(f"User ID '{user_id}' already exists. Try again.")
            continue

        password = input("Enter password: ").strip()
        confirm_password = input("Confirm password: ").strip()

        if password != confirm_password:
            print("Passwords do not match. Try again.")
            continue

        if not password_is_valid(password):
            print(
                "Password must be at least 8 characters long, "
                "contain uppercase and lowercase letters, "
                "at least one number, and one special character."
            )
            continue

        role = input("Enter role your role (Manager, Cashier, Dept Manager, Day/Night Admin): ").strip()
        department = input("Enter department (A or B): ").strip().upper()
        if department not in ["A", "B"]:
            print("Invalid department. Must be 'A' or 'B'.")
            continue

        # Hash password with bcrypt
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()

        # Save user
        users[user_id] = {
            "password_hash": hashed_pw,
            "role": role,
            "department": department
        }
        save_users(users)
        print(f"Registration successful! User '{user_id}' has been created.")
        break

if __name__ == "__main__":
    register_user()
