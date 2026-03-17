"""
student.py
Handles all student CRUD operations.
CSV file: students.csv
Columns : email_address, first_name, last_name, course_id, grade, marks
"""

import csv
import os
import time

STUDENT_FILE = "students.csv"
FIELDNAMES   = ["email_address", "first_name", "last_name", "course_id", "grade", "marks"]


# ── internal helpers ──────────────────────────────────────────────────────────

def _load():
    if not os.path.exists(STUDENT_FILE):
        return []
    with open(STUDENT_FILE, newline="") as f:
        return list(csv.DictReader(f))


def _save(records):
    with open(STUDENT_FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        w.writerows(records)


# ── Student class ─────────────────────────────────────────────────────────────

class Student:

    def __init__(self, email_address, first_name, last_name, course_id, grade, marks):
        self.email_address = email_address.strip().lower()
        self.first_name    = first_name.strip()
        self.last_name     = last_name.strip()
        self.course_id     = course_id.strip().upper()
        self.grade         = grade.strip().upper()
        self.marks         = float(marks)

    def to_dict(self):
        return {
            "email_address": self.email_address,
            "first_name":    self.first_name,
            "last_name":     self.last_name,
            "course_id":     self.course_id,
            "grade":         self.grade,
            "marks":         self.marks,
        }

    def display_records(self):
        print(f"  Email  : {self.email_address}")
        print(f"  Name   : {self.first_name} {self.last_name}")
        print(f"  Course : {self.course_id}  |  Grade: {self.grade}  |  Marks: {self.marks}")
        print("-" * 50)

    # ── Add ───────────────────────────────────────────────────────────────────

    @staticmethod
    def add_new_student(email, first, last, course, grade, marks):
        if not email or not email.strip():
            print("[ERROR] Email cannot be empty.")
            return False
        records = _load()
        if any(r["email_address"].lower() == email.strip().lower() for r in records):
            print(f"[ERROR] Student '{email}' already exists.")
            return False
        s = Student(email, first, last, course, grade, marks)
        records.append(s.to_dict())
        _save(records)
        print(f"[OK] Student '{email}' added.")
        return True

    # ── Delete ────────────────────────────────────────────────────────────────

    @staticmethod
    def delete_student(email):
        records = _load()
        new = [r for r in records if r["email_address"].lower() != email.strip().lower()]
        if len(new) == len(records):
            print(f"[ERROR] '{email}' not found.")
            return False
        _save(new)
        print(f"[OK] Student '{email}' deleted.")
        return True

    # ── Update ────────────────────────────────────────────────────────────────

    @staticmethod
    def update_student_record(email, **kwargs):
        records = _load()
        found = False
        for r in records:
            if r["email_address"].lower() == email.strip().lower():
                for k, v in kwargs.items():
                    if k in FIELDNAMES and k != "email_address":
                        r[k] = v
                found = True
                break
        if not found:
            print(f"[ERROR] '{email}' not found.")
            return False
        _save(records)
        print(f"[OK] Student '{email}' updated.")
        return True

    # ── Search ────────────────────────────────────────────────────────────────

    @staticmethod
    def search_by_email(email):
        records = _load()
        start   = time.perf_counter()
        result  = None
        for r in records:
            if r["email_address"].lower() == email.strip().lower():
                result = r
                break
        elapsed = time.perf_counter() - start
        print(f"[SEARCH] Time: {elapsed:.6f}s | {'Found' if result else 'Not found'}: {email}")
        return result

    # ── Grades / Marks ────────────────────────────────────────────────────────

    @staticmethod
    def check_my_grades(email):
        r = Student.search_by_email(email)
        if r:
            print(f"  Grade: {r['grade']}  Marks: {r['marks']}")
        return r["grade"] if r else None

    @staticmethod
    def check_my_marks(email):
        r = Student.search_by_email(email)
        return float(r["marks"]) if r else None

    # ── Display all ───────────────────────────────────────────────────────────

    @staticmethod
    def display_all_records():
        records = _load()
        if not records:
            print("No student records found.")
            return
        print(f"\n{'='*50}")
        print(f"  Total students: {len(records)}")
        print(f"{'='*50}")
        for r in records:
            Student(**r).display_records()

    # ── Sort ──────────────────────────────────────────────────────────────────

    @staticmethod
    def sort_by_marks(descending=False):
        records = _load()
        start   = time.perf_counter()
        sorted_records = sorted(records, key=lambda r: float(r["marks"]), reverse=descending)
        elapsed = time.perf_counter() - start
        order   = "descending" if descending else "ascending"
        print(f"[SORT] Sorted {len(records)} records by marks ({order}) in {elapsed:.6f}s")
        return sorted_records

    @staticmethod
    def sort_by_email(descending=False):
        records = _load()
        start   = time.perf_counter()
        sorted_records = sorted(records, key=lambda r: r["email_address"].lower(), reverse=descending)
        elapsed = time.perf_counter() - start
        order   = "descending" if descending else "ascending"
        print(f"[SORT] Sorted {len(records)} records by email ({order}) in {elapsed:.6f}s")
        return sorted_records

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def get_all():
        return _load()