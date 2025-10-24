# User Registration (for now) (bcrypt)

Small utility to register users with bcrypt-hashed passwords and a simple JSON store.

## Contents
- P1/register_bcrypt.py — interactive registration script
- P1/users.json — JSON datastore for registered users (created/updated by the script)
- P1/customer_A.txt, P1/customer_B.txt — sample files (not required for registration)

## Requirements
- Python 3.8+
- pip
- bcrypt Python package

Recommended: create and use a virtual environment.

## Setup (inside the VM / on macOS / Linux)
1. Change to project directory:
   ```sh
   cd /Users/andreataguinod/Desktop/fall2025/SYSC4810/Assignment\ 2/P1 #change 
   ```
2. Create and activate a virtual environment:
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependency:
   ```sh
   pip install bcrypt
   ```
## Run
Start the interactive registration script:
```sh
python3 register_bcrypt.py
```
Follow prompts to enter:
- unique user ID
- password (and confirmation)
- role (e.g., Manager, Cashier, DeptManager)
- department (A or B)

The script writes/updates users.json in the same folder.

## Password policy
Passwords must:
- be at least 8 characters
- contain at least one uppercase letter
- contain at least one lowercase letter
- contain at least one digit
- contain at least one special character (one of @$!%*?&)

Regex used in the script:
```
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$
```

## users.json format (example)
Expected structure: a top-level object mapping user IDs to objects with password_hash, role, and department. Example:
```json
{
  "alice": {
    "password_hash": "bcrypt_hash_placeholder",
    "role": "Cashier",
    "department": "A"
  },
  "bob": {
    "password_hash": "bcrypt_hash_placeholder",
    "role": "Manager",
    "department": "B"
  }
}
```
(password_hash values are bcrypt hashes produced by the script; do not store plain-text passwords)

If users.json is empty or contains invalid JSON, the script treats it as no users and will create/overwrite the file when saving.

## Access control policy (summary)
The project submission includes role-based access control intended for the larger system. Current fields stored per-user: role and department. Example policy (roles & permissions):

- Manager
  - Permissions: manage_users, view_reports, approve_discounts
  - Scope: full (both departments)

- DeptManager
  - Permissions: view_reports, approve_discounts
  - Scope: own department only

- Cashier
  - Permissions: process_sales
  - Scope: own department only

Table (brief)
| Role       | Example permissions                   | Department scope |
|------------|----------------------------------------|------------------|
| Manager    | manage_users, view_reports, approve   | A & B (global)   |
| DeptManager| view_reports, approve                 | own department   |
| Cashier    | process_sales                         | own department   |


Adjust the permissions table to match your system's full access matrix when integrating this module.

## Sample accounts (provided for demonstration; no passwords included)
- alice — role: Cashier, department: A
- bob   — role: Manager, department: B
- carol — role: DeptManager, department: A

(These are sample user IDs only — the script will create bcrypt hashes when you register them interactively.)

## Notes & security
- Bcrypt rounds are set in the script; tune the cost (bcrypt.gensalt(rounds=...)) for your environment.
- This utility is educational. For production use, review secure storage, file permissions, backup and access controls, and integrate with a proper authentication system.
- The script handles empty or invalid users.json by treating it as an empty store and will create/overwrite the file when saving.
