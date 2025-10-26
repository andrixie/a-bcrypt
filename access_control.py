import json
from datetime import datetime
import os
from login_bcrypt import login_user

# -------------------------
# Load users from JSON
# -------------------------
def load_users(filename="users.json"):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)

users = load_users()

# -------------------------
# Role-based permissions
# -------------------------
permissions = {
    # Manager: Full access anytime
    "Manager": {
        "customer_A.txt": {"view": True, "edit": True},
        "customer_B.txt": {"view": True, "edit": True},
        "time_restricted": False
    },

    # Department Manager A: Full access to A only
    "Dept Manager A": {
        "customer_A.txt": {"view": True, "edit": True},
        "customer_B.txt": {"view": False, "edit": False},
        "time_restricted": False
    },

    # Department Manager B: Full access to B only
    "Dept Manager B": {
        "customer_A.txt": {"view": False, "edit": False},
        "customer_B.txt": {"view": True, "edit": True},
        "time_restricted": False
    },

    # Cashier A: View only for A
    "Cashier A": {
        "customer_A.txt": {"view": True, "edit": False},
        "customer_B.txt": {"view": False, "edit": False},
        "time_restricted": False
    },

    # Cashier B: View only for B
    "Cashier B": {
        "customer_A.txt": {"view": False, "edit": False},
        "customer_B.txt": {"view": True, "edit": False},
        "time_restricted": False
    },

    # Day Admin: Full access to both, daytime only
    "Day Admin": {
        "customer_A.txt": {"view": True, "edit": True},
        "customer_B.txt": {"view": True, "edit": True},
        "time_restricted": True,
        "start": "01:00:00",
        "end": "12:59:59"
    },

    # Night Admin: Full access to both, nighttime only
    "Night Admin": {
        "customer_A.txt": {"view": True, "edit": True},
        "customer_B.txt": {"view": True, "edit": True},
        "time_restricted": True,
        "start": "13:00:00",
        "end": "00:59:59"
    },
}

# -------------------------
# Audit logging
# -------------------------
AUDIT_FILE = "audit_log.json"

def log_event(user, file_name, action, success, reason=""):
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user,
        "event": action,
        "file": file_name,
        "outcome": "allowed" if success else "denied",
        "reason": reason
    }
    with open(AUDIT_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

# -------------------------
# Time restriction check
# -------------------------
def is_time_allowed(role_info):
    if not role_info.get("time_restricted"):
        return True

    now = datetime.now().time()
    start = datetime.strptime(role_info["start"], "%H:%M:%S").time()
    end = datetime.strptime(role_info["end"], "%H:%M:%S").time()

    if start < end:
        return start <= now <= end
    else:
        # Overnight case (e.g., 13:00:00–00:59:59)
        return now >= start or now <= end

# -------------------------
# Permission check
# -------------------------
def can_access(user_role, file_name, action):
    role_info = permissions.get(user_role)
    if not role_info:
        return False, f"Unknown role: {user_role}"

    if not is_time_allowed(role_info):
        return False, "Access denied: outside allowed hours"

    file_perms = role_info.get(file_name, {})
    if file_perms.get(action, False):
        return True, "Access granted"
    else:
        return False, f"Access denied: insufficient permissions for {action}"

# -------------------------
# File operations
# -------------------------
def view_file(user, file_name):
    role = users[user]["role"]
    allowed, message = can_access(role, file_name, "view")
    log_event(user, file_name, "view", allowed, message)
    if allowed:
        try:
            with open(file_name, "r") as f:
                print(f"\n--- {file_name} ---")
                print(f.read())
                print("--- End of file ---\n")
        except FileNotFoundError:
            print(f"{file_name} does not exist.")
    else:
        print(message)

def edit_file(user, file_name, new_text):
    role = users[user]["role"]
    allowed, message = can_access(role, file_name, "edit")
    log_event(user, file_name, "edit", allowed, message)
    if allowed:
        with open(file_name, "a") as f:
            f.write(new_text + "\n")
        print(f"{file_name} updated successfully.")
    else:
        print(message)

# -------------------------
# Main interface
# -------------------------
def main_interface(user):
    role = users[user]["role"]
    print(f"\nWelcome {user} ({role})!\n")

    while True:
        options = []
        menu_map = {}

        # Customer A
        if can_access(role, "customer_A.txt", "view")[0]:
            options.append("1. View customer_A.txt")
            menu_map["1"] = lambda: view_file(user, "customer_A.txt")
        if can_access(role, "customer_A.txt", "edit")[0]:
            options.append("2. Edit customer_A.txt")
            menu_map["2"] = lambda: edit_file(user, "customer_A.txt", input("Enter text: "))

        # Customer B
        if can_access(role, "customer_B.txt", "view")[0]:
            options.append("3. View customer_B.txt")
            menu_map["3"] = lambda: view_file(user, "customer_B.txt")
        if can_access(role, "customer_B.txt", "edit")[0]:
            options.append("4. Edit customer_B.txt")
            menu_map["4"] = lambda: edit_file(user, "customer_B.txt", input("Enter text: "))

        # Logout
        options.append("5. Logout")
        menu_map["5"] = lambda: "logout"

        print("\nChoose an action:")
        for opt in options:
            print(opt)

        choice = input("Enter choice: ").strip()
        if choice in menu_map:
            result = menu_map[choice]()
            if result == "logout":
                print("Logging out...")
                break
        else:
            print("Invalid choice.")

# -------------------------
# Run system
# -------------------------
if __name__ == "__main__":
    user_info = login_user()
    if user_info:
        username = user_info["username"]
        role = user_info["data"]["role"]
        department = user_info["data"]["department"]
        main_interface(username)
