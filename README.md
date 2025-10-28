# Secure User Registration & Login System using bcrypt

This project provides small utilities to **register users** (`register_bcrypt.py`) and **authenticate users** (`login_bcrypt.py`) using **bcrypt-hashed passwords** stored in a simple JSON datastore. It also includes an **audit logging mechanism** for security-relevant events.

---

## Contents

- `register_bcrypt.py` — interactive user registration (creates/updates `users.json`)  
- `login_bcrypt.py` — interactive login that verifies bcrypt hashes and appends audit events to `audit_log.json`  
- `users.json` — user datastore (managed by scripts)  
- `audit_log.json` — append-only audit log (managed by login script)  
- `customer_A.txt` - file for department A
- `customer_B.txt` - file for department B

---

## Requirements

- Python 3.8+  
- pip  
- `bcrypt` Python package  

---

## Setup (inside the VM)

1. Open a terminal and navigate to the project directory:

```bash
cd /path/to/project
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install bcrypt
```

---

## Run

1. **Register a new user**:

```bash
python3 register_bcrypt.py
```

2. **Login**:

```bash
python3 access_control.py
```

---

## Password Policy

Passwords must:

- Be at least 8 characters  
- Contain at least one uppercase letter  
- Contain at least one lowercase letter  
- Contain at least one digit  
- Contain at least one special character (`@$!%*?&`)  

**Regex used in code:**

```regex
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$
```

---

## Access Control Policy

| Role           | Department | customer_A.txt | customer_B.txt | Time-Restricted |
|----------------|-----------|----------------|----------------|----------------|
| Manager        | N/A       | View/Edit      | View/Edit      | No             |
| Dept Manager   | A         | View/Edit      | Deny           | No             |
| Dept Manager   | B         | Deny           | View/Edit      | No             |
| Cashier        | A         | View           | Deny           | No             |
| Cashier        | B         | Deny           | View           | No             |
| Day Admin      | N/A       | View/Edit      | View/Edit      | 01:00–12:59    |
| Night Admin    | N/A       | View/Edit      | View/Edit      | 13:00–00:59    |

---

## JSON Storage Formats

**`users.json` example:**

```json
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
```

**`audit_log.json` example (append-only JSON lines):**

```json
{"timestamp": "2025-10-24 12:34:56", "user": "alice", "event": "login", "file": "", "outcome": "allowed", "reason": "login success"}
{"timestamp": "2025-10-24 12:35:10", "user": "unknown", "event": "login", "file": "", "outcome": "denied", "reason": "user not found"}
{"timestamp": "2025-10-24 12:36:05", "user": "alice", "event": "view", "file": "customer_A.txt", "outcome": "allowed", "reason": "Access granted"}
{"timestamp": "2025-10-24 12:37:20", "user": "bob", "event": "edit", "file": "customer_B.txt", "outcome": "denied", "reason": "Access denied: insufficient permissions"}
```

---

## Sample User Accounts (for demonstration)

| Username | Role           | Department |
|----------|----------------|-----------|
| alice    | Cashier        | A         |
| bob      | Manager        | B         |
| carol    | Dept Manager   | A         |

> **Note:** Passwords are **hashed using bcrypt** and never stored in plaintext.