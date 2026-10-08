import sqlite3

DB_NAME = "mydb.db"


def create_connection() -> sqlite3.Connection:
    """Create and return a connection to the SQLite database."""
    con = sqlite3.connect(DB_NAME)
    con.execute("PRAGMA foreign_keys = ON")
    return con


def create_tables() -> None:
    """Create all tables required for the Student Management System."""
    con = create_connection()
    cursor = con.cursor()

    # 1. USERS: common details for both students and administrators.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE
        )
    """)

    # 2. STUDENT: student-specific details.
    # user_id is a foreign key to users.user_id.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            roll_no TEXT NOT NULL UNIQUE,
            dob TEXT,
            department TEXT NOT NULL,
            semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 12),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        )
    """)

    # 3. COURSE: list of courses offered by the institution.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS course (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT NOT NULL UNIQUE,
            course_name TEXT NOT NULL,
            credits INTEGER NOT NULL CHECK (credits > 0)
        )
    """)

    # 4. ADMIN: administrator-specific details.
    # user_id is a foreign key to users.user_id.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
            designation TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        )
    """)

    # 5. MANAGEMENT: connects students, courses and admins.
    # It acts like an enrollment/management table.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS management (
            management_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            admin_id INTEGER NOT NULL,
            enrollment_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Active'
                CHECK (status IN ('Active', 'Completed', 'Dropped')),
            UNIQUE (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES student(student_id)
                ON UPDATE CASCADE
                ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES course(course_id)
                ON UPDATE CASCADE
                ON DELETE CASCADE,
            FOREIGN KEY (admin_id) REFERENCES admin(admin_id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        )
    """)

    con.commit()
    con.close()


# Kept as an alias so your old style create_table() code still works.
def create_table() -> None:
    create_tables()
