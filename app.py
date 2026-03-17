"""
app.py
Main console menu for CheckMyGrade application.
Run: python3 app.py
"""

from student    import Student
from course     import Course
from professor  import Professor
from grades     import Grades, _load as load_grades
from login_user import LoginUser

current_user = None
current_role = None


# ── Student Menu ──────────────────────────────────────────────────────────────

def student_menu():
    while True:
        print("""
  ── Student Menu ──────────────────────
  1. Add student
  2. Delete student
  3. Update student
  4. Display all students
  5. Search student by email
  6. Check my grades
  7. Check my marks
  8. Sort by marks
  9. Sort by email
  0. Back
        """)
        choice = input("  Choice: ").strip()

        if choice == "1":
            e  = input("  Email            : ")
            fn = input("  First name       : ")
            ln = input("  Last name        : ")
            ci = input("  Course ID        : ")
            m  = input("  Marks            : ")
            g  = Grades.marks_to_grade(float(m))
            print(f"  Auto grade       : {g}")
            Student.add_new_student(e, fn, ln, ci, g, m)

        elif choice == "2":
            e = input("  Email to delete  : ")
            Student.delete_student(e)

        elif choice == "3":
            e = input("  Email to update  : ")
            print("  Fields you can update: first_name, last_name, course_id, grade, marks")
            field = input("  Field name       : ")
            value = input("  New value        : ")
            Student.update_student_record(e, **{field: value})

        elif choice == "4":
            Student.display_all_records()

        elif choice == "5":
            e = input("  Email to search  : ")
            r = Student.search_by_email(e)
            if r:
                Student(**r).display_records()

        elif choice == "6":
            e = input("  Your email       : ")
            Student.check_my_grades(e)

        elif choice == "7":
            e = input("  Your email       : ")
            Student.check_my_marks(e)

        elif choice == "8":
            d = input("  Descending? (y/n): ").lower() == "y"
            rows = Student.sort_by_marks(d)
            print(f"\n  {'Email':<35} {'Marks'}")
            print("-" * 50)
            for r in rows[:10]:
                print(f"  {r['email_address']:<35} {r['marks']}")
            if len(rows) > 10:
                print(f"  ... and {len(rows)-10} more records")

        elif choice == "9":
            d = input("  Descending? (y/n): ").lower() == "y"
            rows = Student.sort_by_email(d)
            print(f"\n  {'Email':<35} {'Marks'}")
            print("-" * 50)
            for r in rows[:10]:
                print(f"  {r['email_address']:<35} {r['marks']}")
            if len(rows) > 10:
                print(f"  ... and {len(rows)-10} more records")

        elif choice == "0":
            break


# ── Course Menu ───────────────────────────────────────────────────────────────

def course_menu():
    while True:
        print("""
  ── Course Menu ───────────────────────
  1. Add course
  2. Delete course
  3. Modify course
  4. Display all courses
  0. Back
        """)
        choice = input("  Choice: ").strip()

        if choice == "1":
            ci = input("  Course ID        : ")
            cn = input("  Course name      : ")
            d  = input("  Description      : ")
            Course.add_new_course(ci, cn, d)

        elif choice == "2":
            ci = input("  Course ID to delete: ")
            Course.delete_new_course(ci)

        elif choice == "3":
            ci = input("  Course ID to modify: ")
            print("  Fields: course_name, description")
            field = input("  Field name       : ")
            value = input("  New value        : ")
            Course.modify_course(ci, **{field: value})

        elif choice == "4":
            Course.display_all()

        elif choice == "0":
            break


# ── Professor Menu ────────────────────────────────────────────────────────────

def professor_menu():
    while True:
        print("""
  ── Professor Menu ────────────────────
  1. Add professor
  2. Delete professor
  3. Modify professor
  4. Display all professors
  5. Show courses by professor
  0. Back
        """)
        choice = input("  Choice: ").strip()

        if choice == "1":
            pi = input("  Professor email  : ")
            pn = input("  Professor name   : ")
            r  = input("  Rank             : ")
            ci = input("  Course ID        : ")
            Professor.add_new_professor(pi, pn, r, ci)

        elif choice == "2":
            pi = input("  Professor email to delete: ")
            Professor.delete_professor(pi)

        elif choice == "3":
            pi = input("  Professor email to modify: ")
            print("  Fields: professor_name, rank, course_id")
            field = input("  Field name       : ")
            value = input("  New value        : ")
            Professor.modify_professor_details(pi, **{field: value})

        elif choice == "4":
            Professor.display_all()

        elif choice == "5":
            pi = input("  Professor email  : ")
            Professor.show_course_details_by_professor(pi)

        elif choice == "0":
            break


# ── Grades Menu ───────────────────────────────────────────────────────────────

def grades_menu():
    while True:
        print("""
  ── Grades & Reports Menu ─────────────
  1. Display grade scale
  2. Report by course
  3. Report by student
  4. Report by professor
  5. Average & median for a course
  0. Back
        """)
        choice = input("  Choice: ").strip()
        students   = Student.get_all()
        professors = Professor.get_all()

        if choice == "1":
            Grades.display_grade_report()

        elif choice == "2":
            ci = input("  Course ID        : ")
            Grades.report_by_course(students, ci)

        elif choice == "3":
            e = input("  Student email    : ")
            Grades.report_by_student(students, e)

        elif choice == "4":
            pi = input("  Professor email  : ")
            Grades.report_by_professor(students, professors, pi)

        elif choice == "5":
            ci = input("  Course ID        : ")
            filtered = [r for r in students if r["course_id"].upper() == ci.upper()]
            print(f"\n  Stats for {ci}:")
            Grades.average_marks(filtered)
            Grades.median_marks(filtered)

        elif choice == "0":
            break


# ── Login Menu ────────────────────────────────────────────────────────────────

def login_menu():
    global current_user, current_role
    while True:
        print("""
  ── Login Menu ────────────────────────
  1. Register
  2. Login
  3. Change password
  4. Logout
  0. Back
        """)
        choice = input("  Choice: ").strip()

        if choice == "1":
            u = input("  Email            : ")
            p = input("  Password         : ")
            r = input("  Role (student/professor/admin): ")
            LoginUser.register(u, p, r)

        elif choice == "2":
            u = input("  Email            : ")
            p = input("  Password         : ")
            role = LoginUser.login(u, p)
            if role:
                current_user = u
                current_role = role

        elif choice == "3":
            u   = input("  Email            : ")
            old = input("  Old password     : ")
            new = input("  New password     : ")
            LoginUser.change_password(u, old, new)

        elif choice == "4":
            if current_user:
                LoginUser.logout(current_user)
                current_user = None
                current_role = None
            else:
                print("  No user is currently logged in.")

        elif choice == "0":
            break


# ── Main Menu ─────────────────────────────────────────────────────────────────

def main():
    load_grades()  # seed grade scale on first run

    print("\n  ╔══════════════════════════════════╗")
    print("  ║    CheckMyGrade Application      ║")
    print("  ║    SJSU — DATA 200               ║")
    print("  ╚══════════════════════════════════╝")

    while True:
        user_info = f"  Logged in : {current_user} ({current_role})" if current_user else "  Not logged in"
        print(f"\n{user_info}")
        print("""
  ── Main Menu ─────────────────────────
  1. Login / Register
  2. Students
  3. Courses
  4. Professors
  5. Grades & Reports
  6. Exit
        """)
        choice = input("  Choice: ").strip()

        if choice == "1":
            login_menu()
        elif choice == "2":
            student_menu()
        elif choice == "3":
            course_menu()
        elif choice == "4":
            professor_menu()
        elif choice == "5":
            grades_menu()
        elif choice == "6":
            print("\n  Goodbye! See you next time.\n")
            break
        else:
            print("  [ERROR] Invalid choice. Please enter 1-6.")


if __name__ == "__main__":
    main()