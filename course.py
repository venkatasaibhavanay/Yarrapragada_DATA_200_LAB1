"""
course.py
Handles all course CRUD operations.
CSV file: courses.csv
Columns : course_id, course_name, description
"""

import csv
import os

COURSE_FILE = "courses.csv"
FIELDNAMES  = ["course_id", "course_name", "description"]


# ── internal helpers ──────────────────────────────────────────────────────────

def _load():
    if not os.path.exists(COURSE_FILE):
        return []
    with open(COURSE_FILE, newline="") as f:
        return list(csv.DictReader(f))


def _save(records):
    with open(COURSE_FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        w.writerows(records)


# ── Course class ──────────────────────────────────────────────────────────────

class Course:

    def __init__(self, course_id, course_name, description=""):
        self.course_id   = course_id.strip().upper()
        self.course_name = course_name.strip()
        self.description = description.strip()

    def to_dict(self):
        return {
            "course_id":   self.course_id,
            "course_name": self.course_name,
            "description": self.description,
        }

    def display_courses(self):
        print(f"  ID          : {self.course_id}")
        print(f"  Name        : {self.course_name}")
        print(f"  Description : {self.description}")
        print("-" * 50)

    # ── Add ───────────────────────────────────────────────────────────────────

    @staticmethod
    def add_new_course(course_id, course_name, description=""):
        if not course_id or not course_id.strip():
            print("[ERROR] Course ID cannot be empty.")
            return False
        records = _load()
        if any(r["course_id"].upper() == course_id.strip().upper() for r in records):
            print(f"[ERROR] Course '{course_id}' already exists.")
            return False
        c = Course(course_id, course_name, description)
        records.append(c.to_dict())
        _save(records)
        print(f"[OK] Course '{course_id}' added.")
        return True

    # ── Delete ────────────────────────────────────────────────────────────────

    @staticmethod
    def delete_new_course(course_id):
        records = _load()
        new = [r for r in records if r["course_id"].upper() != course_id.strip().upper()]
        if len(new) == len(records):
            print(f"[ERROR] Course '{course_id}' not found.")
            return False
        _save(new)
        print(f"[OK] Course '{course_id}' deleted.")
        return True

    # ── Modify ────────────────────────────────────────────────────────────────

    @staticmethod
    def modify_course(course_id, **kwargs):
        records = _load()
        found = False
        for r in records:
            if r["course_id"].upper() == course_id.strip().upper():
                for k, v in kwargs.items():
                    if k in FIELDNAMES and k != "course_id":
                        r[k] = v
                found = True
                break
        if not found:
            print(f"[ERROR] Course '{course_id}' not found.")
            return False
        _save(records)
        print(f"[OK] Course '{course_id}' updated.")
        return True

    # ── Display ───────────────────────────────────────────────────────────────

    @staticmethod
    def display_all():
        records = _load()
        if not records:
            print("No courses found.")
            return
        print(f"\n{'='*50}")
        print(f"  Total courses: {len(records)}")
        print(f"{'='*50}")
        for r in records:
            Course(**r).display_courses()

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def get_all():
        return _load()

    @staticmethod
    def exists(course_id):
        return any(r["course_id"].upper() == course_id.strip().upper() for r in _load())