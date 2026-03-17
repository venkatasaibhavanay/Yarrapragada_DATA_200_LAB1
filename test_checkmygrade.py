"""
test_checkmygrade.py
Unit tests for CheckMyGrade application.
Run: python3 -m unittest test_checkmygrade -v
"""

import unittest
import os
import csv
import time
import random

from student    import Student, STUDENT_FILE
from course     import Course, COURSE_FILE
from professor  import Professor, PROFESSOR_FILE
from grades     import Grades, _load as load_grades
from login_user import LoginUser, LOGIN_FILE


# ── helpers ───────────────────────────────────────────────────────────────────

def clean_files():
    for f in [STUDENT_FILE, COURSE_FILE, PROFESSOR_FILE, LOGIN_FILE]:
        if os.path.exists(f):
            os.remove(f)


def seed_1000_students():
    """Write 1000 student records directly to CSV."""
    courses = ["DATA200", "DATA220", "DATA226"]
    fieldnames = ["email_address", "first_name", "last_name", "course_id", "grade", "marks"]
    rows = []
    for i in range(1000):
        marks = round(random.uniform(40, 100), 2)
        grade = Grades.marks_to_grade(marks)
        rows.append({
            "email_address": f"student{i:04d}@sjsu.edu",
            "first_name":    f"First{i}",
            "last_name":     f"Last{i}",
            "course_id":     courses[i % len(courses)],
            "grade":         grade,
            "marks":         marks,
        })
    with open(STUDENT_FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    return rows


# ── Test 1: Student CRUD ──────────────────────────────────────────────────────

class TestStudentCRUD(unittest.TestCase):

    def setUp(self):
        clean_files()

    def tearDown(self):
        clean_files()

    def test_01_add_student(self):
        result = Student.add_new_student(
            "bhavana@sjsu.edu", "Venkata Sai Bhavana", "Yarrapragada", "DATA200", "A", 95)
        self.assertTrue(result)
        r = Student.search_by_email("bhavana@sjsu.edu")
        self.assertIsNotNone(r)
        self.assertEqual(r["first_name"], "Venkata Sai Bhavana")
        print("  [PASS] Add student")

    def test_02_duplicate_rejected(self):
        Student.add_new_student("dup@sjsu.edu", "Test", "User", "DATA200", "B", 85)
        result = Student.add_new_student("dup@sjsu.edu", "Test", "User", "DATA200", "B", 85)
        self.assertFalse(result)
        print("  [PASS] Duplicate student rejected")

    def test_03_delete_student(self):
        Student.add_new_student("del@sjsu.edu", "Delete", "Me", "DATA200", "C", 72)
        result = Student.delete_student("del@sjsu.edu")
        self.assertTrue(result)
        self.assertIsNone(Student.search_by_email("del@sjsu.edu"))
        print("  [PASS] Delete student")

    def test_04_update_student(self):
        Student.add_new_student("upd@sjsu.edu", "Update", "Me", "DATA200", "B", 82)
        Student.update_student_record("upd@sjsu.edu", marks=95, grade="A")
        r = Student.search_by_email("upd@sjsu.edu")
        self.assertEqual(float(r["marks"]), 95)
        self.assertEqual(r["grade"], "A")
        print("  [PASS] Update student")

    def test_05_empty_email_rejected(self):
        result = Student.add_new_student("", "No", "Email", "DATA200", "A", 99)
        self.assertFalse(result)
        print("  [PASS] Empty email rejected")


# ── Test 2: 1000 Records + Timing ────────────────────────────────────────────

class TestBulkAndTiming(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        clean_files()
        load_grades()
        cls.rows = seed_1000_students()

    @classmethod
    def tearDownClass(cls):
        clean_files()

    def test_01_1000_records_loaded(self):
        all_students = Student.get_all()
        self.assertEqual(len(all_students), 1000)
        print(f"\n  [PASS] 1000 records loaded successfully")

    def test_02_search_found_timing(self):
        target = "student0500@sjsu.edu"
        start  = time.perf_counter()
        result = Student.search_by_email(target)
        elapsed = time.perf_counter() - start
        self.assertIsNotNone(result)
        self.assertLess(elapsed, 1.0)
        print(f"  [PASS] Search (found) completed in {elapsed:.6f}s")

    def test_03_search_not_found_timing(self):
        start   = time.perf_counter()
        result  = Student.search_by_email("nobody@ghost.edu")
        elapsed = time.perf_counter() - start
        self.assertIsNone(result)
        print(f"  [PASS] Search (not found) completed in {elapsed:.6f}s")

    def test_04_sort_marks_ascending(self):
        start  = time.perf_counter()
        rows   = Student.sort_by_marks(descending=False)
        elapsed = time.perf_counter() - start
        marks  = [float(r["marks"]) for r in rows]
        self.assertEqual(marks, sorted(marks))
        print(f"  [PASS] Sort by marks ascending in {elapsed:.6f}s")

    def test_05_sort_marks_descending(self):
        start  = time.perf_counter()
        rows   = Student.sort_by_marks(descending=True)
        elapsed = time.perf_counter() - start
        marks  = [float(r["marks"]) for r in rows]
        self.assertEqual(marks, sorted(marks, reverse=True))
        print(f"  [PASS] Sort by marks descending in {elapsed:.6f}s")

    def test_06_sort_email_ascending(self):
        start  = time.perf_counter()
        rows   = Student.sort_by_email(descending=False)
        elapsed = time.perf_counter() - start
        emails = [r["email_address"] for r in rows]
        self.assertEqual(emails, sorted(emails))
        print(f"  [PASS] Sort by email ascending in {elapsed:.6f}s")

    def test_07_sort_email_descending(self):
        start  = time.perf_counter()
        rows   = Student.sort_by_email(descending=True)
        elapsed = time.perf_counter() - start
        emails = [r["email_address"] for r in rows]
        self.assertEqual(emails, sorted(emails, reverse=True))
        print(f"  [PASS] Sort by email descending in {elapsed:.6f}s")


# ── Test 3: Course CRUD ───────────────────────────────────────────────────────

class TestCourseCRUD(unittest.TestCase):

    def setUp(self):
        if os.path.exists(COURSE_FILE):
            os.remove(COURSE_FILE)

    def tearDown(self):
        if os.path.exists(COURSE_FILE):
            os.remove(COURSE_FILE)

    def test_01_add_course(self):
        self.assertTrue(Course.add_new_course("DATA200", "Data Science", "Python and DS"))
        self.assertTrue(Course.exists("DATA200"))
        print("  [PASS] Add course")

    def test_02_duplicate_course_rejected(self):
        Course.add_new_course("CS101", "Computer Science", "")
        self.assertFalse(Course.add_new_course("CS101", "CS Again", ""))
        print("  [PASS] Duplicate course rejected")

    def test_03_delete_course(self):
        Course.add_new_course("BIO101", "Biology", "Life science")
        self.assertTrue(Course.delete_new_course("BIO101"))
        self.assertFalse(Course.exists("BIO101"))
        print("  [PASS] Delete course")

    def test_04_modify_course(self):
        Course.add_new_course("MATH301", "Math", "Old desc")
        Course.modify_course("MATH301", description="New desc")
        records = Course.get_all()
        r = next(r for r in records if r["course_id"] == "MATH301")
        self.assertEqual(r["description"], "New desc")
        print("  [PASS] Modify course")

    def test_05_empty_id_rejected(self):
        self.assertFalse(Course.add_new_course("", "No ID", ""))
        print("  [PASS] Empty course ID rejected")


# ── Test 4: Professor CRUD ────────────────────────────────────────────────────

class TestProfessorCRUD(unittest.TestCase):

    def setUp(self):
        if os.path.exists(PROFESSOR_FILE):
            os.remove(PROFESSOR_FILE)

    def tearDown(self):
        if os.path.exists(PROFESSOR_FILE):
            os.remove(PROFESSOR_FILE)

    def test_01_add_professor(self):
        self.assertTrue(Professor.add_new_professor(
            "saini@sjsu.edu", "Paramdeep Saini", "Senior Professor", "DATA200"))
        print("  [PASS] Add professor")

    def test_02_duplicate_professor_rejected(self):
        Professor.add_new_professor("saini@sjsu.edu", "Paramdeep Saini", "Senior Professor", "DATA200")
        self.assertFalse(Professor.add_new_professor(
            "saini@sjsu.edu", "Paramdeep Saini", "Senior Professor", "DATA200"))
        print("  [PASS] Duplicate professor rejected")

    def test_03_delete_professor(self):
        Professor.add_new_professor("del@sjsu.edu", "Dr. Del", "Associate", "CS101")
        self.assertTrue(Professor.delete_professor("del@sjsu.edu"))
        print("  [PASS] Delete professor")

    def test_04_modify_professor(self):
        Professor.add_new_professor("mod@sjsu.edu", "Dr. Old", "Lecturer", "MATH301")
        Professor.modify_professor_details("mod@sjsu.edu", professor_name="Dr. New", rank="Professor")
        records = Professor.get_all()
        r = next(r for r in records if r["professor_id"] == "mod@sjsu.edu")
        self.assertEqual(r["professor_name"], "Dr. New")
        self.assertEqual(r["rank"], "Professor")
        print("  [PASS] Modify professor")


# ── Test 5: Login & Password ──────────────────────────────────────────────────

class TestLogin(unittest.TestCase):

    def setUp(self):
        if os.path.exists(LOGIN_FILE):
            os.remove(LOGIN_FILE)

    def tearDown(self):
        if os.path.exists(LOGIN_FILE):
            os.remove(LOGIN_FILE)

    def test_01_register_and_login(self):
        LoginUser.register("bhavana@sjsu.edu", "Welcome12#", "student")
        role = LoginUser.login("bhavana@sjsu.edu", "Welcome12#")
        self.assertEqual(role, "student")
        print("  [PASS] Register and login")

    def test_02_wrong_password_rejected(self):
        LoginUser.register("prof@sjsu.edu", "Correct99#", "professor")
        role = LoginUser.login("prof@sjsu.edu", "WrongPass")
        self.assertIsNone(role)
        print("  [PASS] Wrong password rejected")

    def test_03_password_encrypted_in_file(self):
        LoginUser.register("enc@sjsu.edu", "PlainText1", "student")
        with open(LOGIN_FILE, newline="") as f:
            rows = list(csv.DictReader(f))
        stored = rows[0]["password"]
        self.assertNotEqual(stored, "PlainText1")
        print("  [PASS] Password is encrypted in file")

    def test_04_change_password(self):
        LoginUser.register("chg@sjsu.edu", "OldPass1#", "student")
        LoginUser.change_password("chg@sjsu.edu", "OldPass1#", "NewPass2#")
        self.assertIsNone(LoginUser.login("chg@sjsu.edu", "OldPass1#"))
        self.assertEqual(LoginUser.login("chg@sjsu.edu", "NewPass2#"), "student")
        print("  [PASS] Change password")


# ── Test 6: Grades & Statistics ───────────────────────────────────────────────

class TestGradesAndStats(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        clean_files()
        load_grades()
        seed_1000_students()

    @classmethod
    def tearDownClass(cls):
        clean_files()

    def test_01_marks_to_grade(self):
        self.assertEqual(Grades.marks_to_grade(95), "A")
        self.assertEqual(Grades.marks_to_grade(82), "B")
        self.assertEqual(Grades.marks_to_grade(74), "C")
        self.assertEqual(Grades.marks_to_grade(65), "D")
        self.assertEqual(Grades.marks_to_grade(50), "F")
        print("  [PASS] Marks to grade conversion")

    def test_02_average_marks(self):
        students = Student.get_all()
        avg = Grades.average_marks(students)
        self.assertGreater(avg, 0)
        self.assertLessEqual(avg, 100)
        print(f"  [PASS] Average marks: {avg:.2f}")

    def test_03_median_marks(self):
        students = Student.get_all()
        med = Grades.median_marks(students)
        self.assertGreater(med, 0)
        self.assertLessEqual(med, 100)
        print(f"  [PASS] Median marks: {med:.2f}")


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    unittest.main(verbosity=2)