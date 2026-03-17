"""
login_user.py
Handles user authentication with encrypted password storage.
CSV file: login.csv
Columns : user_id, password, role
"""

import csv
import os
from encdyc import TextSecurity

LOGIN_FILE = "login.csv"
FIELDNAMES = ["user_id", "password", "role"]
_cipher    = TextSecurity(4)


# ── internal helpers ──────────────────────────────────────────────────────────

def _load():
    if not os.path.exists(LOGIN_FILE):
        return []
    with open(LOGIN_FILE, newline="") as f:
        return list(csv.DictReader(f))


def _save(records):
    with open(LOGIN_FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        w.writerows(records)


# ── LoginUser class ───────────────────────────────────────────────────────────

class LoginUser:

    def __init__(self, user_id, password, role="student"):
        self.user_id  = user_id.strip().lower()
        self.password = password
        self.role     = role.strip().lower()

    # ── Encrypt / Decrypt ─────────────────────────────────────────────────────

    @staticmethod
    def encrypt_password(plain_text):
        return _cipher.encrypt(plain_text)

    @staticmethod
    def decrypt_password(cipher_text):
        return _cipher.decrypt(cipher_text)

    # ── Register ──────────────────────────────────────────────────────────────

    @staticmethod
    def register(user_id, plain_password, role="student"):
        if not user_id or not plain_password:
            print("[ERROR] User ID and password cannot be empty.")
            return False
        records = _load()
        if any(r["user_id"].lower() == user_id.strip().lower() for r in records):
            print(f"[ERROR] User '{user_id}' already exists.")
            return False
        encrypted = LoginUser.encrypt_password(plain_password)
        records.append({
            "user_id":  user_id.strip().lower(),
            "password": encrypted,
            "role":     role.strip().lower()
        })
        _save(records)
        print(f"[OK] User '{user_id}' registered as {role}.")
        return True

    # ── Login ─────────────────────────────────────────────────────────────────

    @staticmethod
    def login(user_id, plain_password):
        records = _load()
        for r in records:
            if r["user_id"].lower() == user_id.strip().lower():
                decrypted = LoginUser.decrypt_password(r["password"])
                if decrypted == plain_password:
                    print(f"[OK] Login successful. Welcome {user_id}! Role: {r['role']}")
                    return r["role"]
        print("[ERROR] Invalid email or password.")
        return None

    # ── Logout ────────────────────────────────────────────────────────────────

    @staticmethod
    def logout(user_id):
        print(f"[OK] User '{user_id}' logged out successfully.")

    # ── Change Password ───────────────────────────────────────────────────────

    @staticmethod
    def change_password(user_id, old_password, new_password):
        records = _load()
        for r in records:
            if r["user_id"].lower() == user_id.strip().lower():
                decrypted = LoginUser.decrypt_password(r["password"])
                if decrypted != old_password:
                    print("[ERROR] Old password is incorrect.")
                    return False
                r["password"] = LoginUser.encrypt_password(new_password)
                _save(records)
                print("[OK] Password changed successfully.")
                return True
        print(f"[ERROR] User '{user_id}' not found.")
        return False

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def get_role(user_id):
        for r in _load():
            if r["user_id"].lower() == user_id.strip().lower():
                return r["role"]
        return None