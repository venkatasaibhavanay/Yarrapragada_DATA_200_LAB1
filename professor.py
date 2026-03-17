"""
professor.py
Handles all professor CRUD operations.
CSV file: professors.csv
Columns : professor_id, professor_name, rank, course_id
"""

import csv
import os

PROFESSOR_FILE = "professors.csv"
FIELDNAMES     = ["professor_id", "professor_name", "rank", "course_id"]


# ── internal helpers ──────────────────────────────────────────────────────────

def _load():
    if not os.path.exists(PROFESSOR_FILE):
        return []
    with open(PROFESSOR_FILE, newline="") as f:
        return list(csv.DictReader(f))


def _save(records):
    with open(PROFESSOR_FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        w.writerows(records)


# ── Professor class ───────────────────────────────────────────────────────────

class Professor:

    def __init__(self, professor_id, professor_name, rank, course_id):
        self.professor_id   = professor_id.strip().lower()
        self.professor_name = professor_name.strip()
        self.rank           = rank.strip()
        self.course_id      = course_id.strip().upper()

    def to_dict(self):
        return {
            "professor_id":   self.professor_id,
            "professor_name": self.professor_name,
            "rank":           self.rank,
            "course_id":      self.course_id,
        }

    def professors_details(self):
        print(f"  Email  : {self.professor_id}")
        print(f"  Name   : {self.professor_name}")
        print(f"  Rank   : {self.rank}")
        print(f"  Course : {self.course_id}")
        print("-" * 50)

    # ── Add ───────────────────────────────────────────────────────────────────

    @staticmethod
    def add_new_professor(prof_id, name, rank, course_id):
        if not prof_id or not prof_id.strip():
            print("[ERROR] Professor ID cannot be empty.")
            return False
        records = _load()
        if any(r["professor_id"].lower() == prof_id.strip().lower() for r in records):
            print(f"[ERROR] Professor '{prof_id}' already exists.")
            return False
        p = Professor(prof_id, name, rank, course_id)
        records.append(p.to_dict())
        _save(records)
        print(f"[OK] Professor '{prof_id}' added.")
        return True

    # ── Delete ────────────────────────────────────────────────────────────────

    @staticmethod
    def delete_professor(prof_id):
        records = _load()
        new = [r for r in records if r["professor_id"].lower() != prof_id.strip().lower()]
        if len(new) == len(records):
            print(f"[ERROR] Professor '{prof_id}' not found.")
            return False
        _save(new)
        print(f"[OK] Professor '{prof_id}' deleted.")
        return True

    # ── Modify ────────────────────────────────────────────────────────────────

    @staticmethod
    def modify_professor_details(prof_id, **kwargs):
        records = _load()
        found = False
        for r in records:
            if r["professor_id"].lower() == prof_id.strip().lower():
                for k, v in kwargs.items():
                    if k in FIELDNAMES and k != "professor_id":
                        r[k] = v
                found = True
                break
        if not found:
            print(f"[ERROR] Professor '{prof_id}' not found.")
            return False
        _save(records)
        print(f"[OK] Professor '{prof_id}' updated.")
        return True

    # ── Display ───────────────────────────────────────────────────────────────

    @staticmethod
    def show_course_details_by_professor(prof_id):
        records = _load()
        for r in records:
            if r["professor_id"].lower() == prof_id.strip().lower():
                print(f"  Professor : {r['professor_name']}")
                print(f"  Teaches   : {r['course_id']}")
                return r["course_id"]
        print(f"[ERROR] Professor '{prof_id}' not found.")
        return None

    @staticmethod
    def display_all():
        records = _load()
        if not records:
            print("No professors found.")
            return
        print(f"\n{'='*50}")
        print(f"  Total professors: {len(records)}")
        print(f"{'='*50}")
        for r in records:
            Professor(**r).professors_details()

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def get_all():
        return _load()
