import sqlite3
from db_config import create_connection


# ============================================================
# USERS
# ============================================================

def insert_user() -> None:
    name = input("Enter Name: ").strip()
    phone = input("Enter Phone: ").strip()
    email = input("Enter Email: ").strip()

    if not name or not phone or not email:
        print("Name, phone and email are required.")
        return

    try:
        con = create_connection()
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO users(name, phone, email) VALUES (?, ?, ?)",
            (name, phone, email)
        )
        con.commit()
        user_id = cursor.lastrowid
        con.close()
        print(f"User inserted successfully! User ID = {user_id}")
    except sqlite3.IntegrityError as e:
        print(f"Error: phone/email must be unique. {e}")


def display_users() -> None:
    con = create_connection()
    cursor = con.cursor()
    cursor.execute("SELECT user_id, name, phone, email FROM users ORDER BY user_id")
    rows = cursor.fetchall()
    con.close()

    if not rows:
        print("No users found.")
        return

    print("\n--- USERS ---")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]} | Email: {row[3]}")


def update_user() -> None:
    try:
        user_id = int(input("Enter User ID to update: "))
    except ValueError:
        print("Invalid User ID.")
        return

    updates = []
    values = []

    choice = input("Update Name? (yes/no): ").strip().lower()
    if choice == "yes":
        updates.append("name = ?")
        values.append(input("Enter new Name: ").strip())

    choice = input("Update Phone? (yes/no): ").strip().lower()
    if choice == "yes":
        updates.append("phone = ?")
        values.append(input("Enter new Phone: ").strip())

    choice = input("Update Email? (yes/no): ").strip().lower()
    if choice == "yes":
        updates.append("email = ?")
        values.append(input("Enter new Email: ").strip())

    if not updates:
        print("No updates selected.")
        return

    try:
        con = create_connection()
        cursor = con.cursor()
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"
        cursor.execute(query, values)
        con.commit()
        if cursor.rowcount == 0:
            print("User not found.")
        else:
            print("User updated successfully!")
        con.close()
    except sqlite3.IntegrityError:
        print("Error: phone or email already exists.")


def delete_user() -> None:
    try:
        user_id = int(input("Enter User ID to delete: "))
    except ValueError:
        print("Invalid User ID.")
        return

    try:
        con = create_connection()
        cursor = con.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        con.commit()
        if cursor.rowcount == 0:
            print("User not found.")
        else:
            print("User deleted successfully.")
        con.close()
    except sqlite3.IntegrityError as e:
        print(f"Could not delete user: {e}")


# ============================================================
# STUDENTS
# ============================================================

def insert_student() -> None:
    try:
        user_id = int(input("Enter existing User ID for this student: "))
        semester = int(input("Enter Semester (1-12): "))
    except ValueError:
        print("User ID and semester must be numbers.")
        return

    roll_no = input("Enter Roll No: ").strip()
    dob = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
    department = input("Enter Department: ").strip()

    if not roll_no or not department:
        print("Roll No and Department are required.")
        return

    try:
        con = create_connection()
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO student(user_id, roll_no, dob, department, semester)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, roll_no, dob, department, semester))
        con.commit()
        print(f"Student inserted successfully! Student ID = {cursor.lastrowid}")
        con.close()
    except sqlite3.IntegrityError as e:
        print(f"Could not insert student. Check User ID, roll number and semester. {e}")


def display_students() -> None:
    con = create_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT s.student_id, u.user_id, u.name, s.roll_no,
               s.dob, s.department, s.semester
        FROM student s
        JOIN users u ON s.user_id = u.user_id
        ORDER BY s.student_id
    """)
    rows = cursor.fetchall()
    con.close()

    if not rows:
        print("No students found.")
        return

    print("\n--- STUDENTS ---")
    for r in rows:
        print(
            f"Student ID: {r[0]} | User ID: {r[1]} | Name: {r[2]} | "
            f"Roll No: {r[3]} | DOB: {r[4]} | Dept: {r[5]} | Semester: {r[6]}"
        )


# ============================================================
# COURSES
# ============================================================

def insert_course() -> None:
    course_code = input("Enter Course Code: ").strip()
    course_name = input("Enter Course Name: ").strip()
    try:
        credits = int(input("Enter Credits: "))
    except ValueError:
        print("Credits must be a number.")
        return

    try:
        con = create_connection()
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO course(course_code, course_name, credits)
            VALUES (?, ?, ?)
        """, (course_code, course_name, credits))
        con.commit()
        print(f"Course inserted successfully! Course ID = {cursor.lastrowid}")
        con.close()
    except sqlite3.IntegrityError as e:
        print(f"Could not insert course. Course code may already exist. {e}")


def display_courses() -> None:
    con = create_connection()
    cursor = con.cursor()
    cursor.execute("SELECT course_id, course_code, course_name, credits FROM course ORDER BY course_id")
    rows = cursor.fetchall()
    con.close()

    if not rows:
        print("No courses found.")
        return

    print("\n--- COURSES ---")
    for r in rows:
        print(f"ID: {r[0]} | Code: {r[1]} | Name: {r[2]} | Credits: {r[3]}")


# ============================================================
# ADMINS
# ============================================================

def insert_admin() -> None:
    try:
        user_id = int(input("Enter existing User ID for this admin: "))
    except ValueError:
        print("User ID must be a number.")
        return

    username = input("Enter Username: ").strip()
    designation = input("Enter Designation: ").strip()

    try:
        con = create_connection()
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO admin(user_id, username, designation)
            VALUES (?, ?, ?)
        """, (user_id, username, designation))
        con.commit()
        print(f"Admin inserted successfully! Admin ID = {cursor.lastrowid}")
        con.close()
    except sqlite3.IntegrityError as e:
        print(f"Could not insert admin. User ID/username may already be used. {e}")


def display_admins() -> None:
    con = create_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT a.admin_id, a.user_id, u.name, a.username, a.designation
        FROM admin a
        JOIN users u ON a.user_id = u.user_id
        ORDER BY a.admin_id
    """)
    rows = cursor.fetchall()
    con.close()

    if not rows:
        print("No admins found.")
        return

    print("\n--- ADMINS ---")
    for r in rows:
        print(
            f"Admin ID: {r[0]} | User ID: {r[1]} | Name: {r[2]} | "
            f"Username: {r[3]} | Designation: {r[4]}"
        )


# ============================================================
# MANAGEMENT / ENROLLMENT
# ============================================================

def insert_management() -> None:
    try:
        student_id = int(input("Enter Student ID: "))
        course_id = int(input("Enter Course ID: "))
        admin_id = int(input("Enter Admin ID: "))
    except ValueError:
        print("Student ID, Course ID and Admin ID must be numbers.")
        return

    enrollment_date = input("Enter Enrollment Date (YYYY-MM-DD): ").strip()
    status = input("Enter Status (Active/Completed/Dropped): ").strip().title()

    if status not in {"Active", "Completed", "Dropped"}:
        print("Invalid status.")
        return

    try:
        con = create_connection()
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO management(
                student_id, course_id, admin_id, enrollment_date, status
            ) VALUES (?, ?, ?, ?, ?)
        """, (student_id, course_id, admin_id, enrollment_date, status))
        con.commit()
        print(f"Management record inserted! Management ID = {cursor.lastrowid}")
        con.close()
    except sqlite3.IntegrityError as e:
        print(f"Could not insert management record. Check all IDs and duplicate enrollment. {e}")


def display_management() -> None:
    con = create_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT m.management_id,
               s.roll_no,
               su.name AS student_name,
               c.course_code,
               c.course_name,
               au.name AS admin_name,
               m.enrollment_date,
               m.status
        FROM management m
        JOIN student s ON m.student_id = s.student_id
        JOIN users su ON s.user_id = su.user_id
        JOIN course c ON m.course_id = c.course_id
        JOIN admin a ON m.admin_id = a.admin_id
        JOIN users au ON a.user_id = au.user_id
        ORDER BY m.management_id
    """)
    rows = cursor.fetchall()
    con.close()

    if not rows:
        print("No management/enrollment records found.")
        return

    print("\n--- MANAGEMENT / ENROLLMENTS ---")
    for r in rows:
        print(
            f"ID: {r[0]} | Roll No: {r[1]} | Student: {r[2]} | "
            f"Course: {r[3]} - {r[4]} | Admin: {r[5]} | "
            f"Date: {r[6]} | Status: {r[7]}"
        )


# ============================================================
# REPORT
# ============================================================

def student_course_report() -> None:
    """Display a joined report showing the main relationships."""
    con = create_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT u.name,
               s.roll_no,
               s.department,
               c.course_code,
               c.course_name,
               m.enrollment_date,
               m.status
        FROM management m
        JOIN student s ON m.student_id = s.student_id
        JOIN users u ON s.user_id = u.user_id
        JOIN course c ON m.course_id = c.course_id
        ORDER BY s.roll_no, c.course_code
    """)
    rows = cursor.fetchall()
    con.close()

    if not rows:
        print("No report data found.")
        return

    print("\n--- STUDENT COURSE REPORT ---")
    for r in rows:
        print(
            f"Student: {r[0]} | Roll No: {r[1]} | Department: {r[2]} | "
            f"Course: {r[3]} - {r[4]} | Date: {r[5]} | Status: {r[6]}"
        )
