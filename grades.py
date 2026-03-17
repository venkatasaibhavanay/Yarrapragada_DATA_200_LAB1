"""
grades.py
Handles grade scale, statistics, and reports.
CSV file: grades.csv
Columns : grade_id, grade, min_marks, max_marks

Grade scale:
  A = 90 - 100
  B = 80 - 89
  C = 70 - 79
  D = 60 - 69
  F =  0 - 59
"""

import csv
import os
import statistics

GRADES_FILE = "grades.csv"
FIELDNAMES  = ["grade_id", "grade", "min_marks", "max_marks"]

DEFAULT_GRADES = [
    {"grade_id": "1", "grade": "A", "min_marks": "90", "max_marks": "100"},
    {"grade_id": "2", "grade": "B", "min_marks": "80", "max_marks": "89"},
    {"grade_id": "3", "grade": "C", "min_marks": "70", "max_marks": "79"},
    {"grade_id": "4", "grade": "D", "min_marks": "60", "max_marks": "69"},
    {"grade_id": "5", "grade": "F", "min_marks": "0",  "max_marks": "59"},
]


# ── internal helpers ──────────────────────────────────────────────────────────

def _load():
    if not os.path.exists(GRADES_FILE):
        _save(DEFAULT_GRADES)
        return DEFAULT_GRADES
    with open(GRADES_FILE, newline="") as f:
        return list(csv.DictReader(f))


def _save(records):
    with open(GRADES_FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        w.writerows(records)


# ── Grades class ──────────────────────────────────────────────────────────────

class Grades:

    def __init__(self, grade_id, grade, min_marks, max_marks):
        self.grade_id  = str(grade_id)
        self.grade     = grade.strip().upper()
        self.min_marks = float(min_marks)
        self.max_marks = float(max_marks)

    def to_dict(self):
        return {
            "grade_id":  self.grade_id,
            "grade":     self.grade,
            "min_marks": self.min_marks,
            "max_marks": self.max_marks,
        }

    # ── Grade scale CRUD ──────────────────────────────────────────────────────

    @staticmethod
    def marks_to_grade(marks):
        """Convert numeric marks to letter grade."""
        marks = float(marks)
        for r in _load():
            if float(r["min_marks"]) <= marks <= float(r["max_marks"]):
                return r["grade"]
        return "F"

    @staticmethod
    def add_grade(grade_id, grade, min_marks, max_marks):
        records = _load()
        if any(r["grade_id"] == str(grade_id) for r in records):
            print(f"[ERROR] Grade ID '{grade_id}' already exists.")
            return False
        g = Grades(grade_id, grade, min_marks, max_marks)
        records.append(g.to_dict())
        _save(records)
        print(f"[OK] Grade '{grade}' added.")
        return True

    @staticmethod
    def delete_grade(grade_id):
        records = _load()
        new = [r for r in records if r["grade_id"] != str(grade_id)]
        if len(new) == len(records):
            print(f"[ERROR] Grade ID '{grade_id}' not found.")
            return False
        _save(new)
        print(f"[OK] Grade ID '{grade_id}' deleted.")
        return True

    @staticmethod
    def modify_grade(grade_id, **kwargs):
        records = _load()
        found = False
        for r in records:
            if r["grade_id"] == str(grade_id):
                for k, v in kwargs.items():
                    if k in FIELDNAMES:
                        r[k] = v
                found = True
                break
        if not found:
            print(f"[ERROR] Grade ID '{grade_id}' not found.")
            return False
        _save(records)
        print(f"[OK] Grade ID '{grade_id}' updated.")
        return True

    @staticmethod
    def display_grade_report():
        records = _load()
        print(f"\n{'='*50}")
        print(f"  Grade Scale")
        print(f"{'='*50}")
        for r in records:
            print(f"  {r['grade']}  :  {r['min_marks']} – {r['max_marks']}")
        print("-" * 50)

    # ── Statistics ────────────────────────────────────────────────────────────

    @staticmethod
    def average_marks(student_records):
        if not student_records:
            print("  No records to calculate average.")
            return 0.0
        marks = [float(r["marks"]) for r in student_records]
        avg = sum(marks) / len(marks)
        print(f"  Average marks : {avg:.2f}")
        return avg

    @staticmethod
    def median_marks(student_records):
        if not student_records:
            print("  No records to calculate median.")
            return 0.0
        marks = [float(r["marks"]) for r in student_records]
        med = statistics.median(marks)
        print(f"  Median marks  : {med:.2f}")
        return med

    # ── Reports ───────────────────────────────────────────────────────────────

    @staticmethod
    def report_by_course(student_records, course_id):
        filtered = [r for r in student_records
                    if r["course_id"].upper() == course_id.upper()]
        print(f"\n{'='*50}")
        print(f"  Report — Course: {course_id}  ({len(filtered)} students)")
        print(f"{'='*50}")
        if not filtered:
            print("  No students found for this course.")
            return
        for r in filtered:
            print(f"  {r['email_address']:<35} {r['grade']}  {r['marks']}")
        print("-" * 50)
        Grades.average_marks(filtered)
        Grades.median_marks(filtered)

    @staticmethod
    def report_by_student(student_records, email):
        filtered = [r for r in student_records
                    if r["email_address"].lower() == email.lower()]
        print(f"\n{'='*50}")
        print(f"  Report — Student: {email}")
        print(f"{'='*50}")
        if not filtered:
            print("  No records found for this student.")
            return
        for r in filtered:
            print(f"  Course: {r['course_id']:<12} Grade: {r['grade']}  Marks: {r['marks']}")
        print("-" * 50)

    @staticmethod
    def report_by_professor(student_records, professor_records, prof_id):
        courses = [r["course_id"] for r in professor_records
                   if r["professor_id"].lower() == prof_id.lower()]
        print(f"\n{'='*50}")
        print(f"  Report — Professor: {prof_id}")
        print(f"  Courses taught : {courses}")
        print(f"{'='*50}")
        if not courses:
            print("  No courses found for this professor.")
            return
        for course in courses:
            Grades.report_by_course(student_records, course)