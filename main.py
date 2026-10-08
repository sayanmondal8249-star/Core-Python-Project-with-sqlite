from db_config import create_tables
from operations import (
    insert_user, display_users, update_user, delete_user,
    insert_student, display_students,
    insert_course, display_courses,
    insert_admin, display_admins,
    insert_management, display_management,
    student_course_report,
)


def menu() -> None:
    while True:
        print("\n" + "=" * 55)
        print("        STUDENT MANAGEMENT SYSTEM")
        print("=" * 55)
        print("1. Insert User")
        print("2. Display Users")
        print("3. Update User")
        print("4. Delete User")
        print("5. Insert Student")
        print("6. Display Students")
        print("7. Insert Course")
        print("8. Display Courses")
        print("9. Insert Admin")
        print("10. Display Admins")
        print("11. Add Student to Course (Management)")
        print("12. Display Management Records")
        print("13. Student-Course Report")
        print("14. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            insert_user()
        elif choice == "2":
            display_users()
        elif choice == "3":
            update_user()
        elif choice == "4":
            delete_user()
        elif choice == "5":
            insert_student()
        elif choice == "6":
            display_students()
        elif choice == "7":
            insert_course()
        elif choice == "8":
            display_courses()
        elif choice == "9":
            insert_admin()
        elif choice == "10":
            display_admins()
        elif choice == "11":
            insert_management()
        elif choice == "12":
            display_management()
        elif choice == "13":
            student_course_report()
        elif choice == "14":
            print("Exiting Student Management System...")
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    create_tables()
    menu()
