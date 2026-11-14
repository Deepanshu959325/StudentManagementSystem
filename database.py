
import sqlite3


# 1. Connect to database
def get_connection():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn


# 2. Create student table
def create_table():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            course TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# 3. CREATE - Add student
def add_student(name, email, course):
    conn = get_connection()

    try:
        conn.execute(
            "INSERT INTO students (name, email, course) VALUES (?, ?, ?)",
            (name, email, course)
        )

        conn.commit()
        print("Student added successfully!")
        return True

    except sqlite3.IntegrityError:
        print("Error: Email already exists.")
        return False

    finally:
        conn.close()


# 4. READ - Display all students
def get_students():
    conn = get_connection()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return [dict(student) for student in students]


# 5. UPDATE - Update student
def update_student(student_id, name, email, course):
    conn = get_connection()

    try:
        cursor = conn.execute(
            """UPDATE students
               SET name = ?, email = ?, course = ?
               WHERE id = ?""",
            (name, email, course, student_id)
        )

        conn.commit()

        if cursor.rowcount > 0:
            print("Student updated successfully!")
            return True
        else:
            print("Student not found!")
            return False

    except sqlite3.IntegrityError:
        print("Error: Email already exists.")
        return False

    finally:
        conn.close()


# 6. DELETE - Delete student
def delete_student(student_id):
    conn = get_connection()

    cursor = conn.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()

    if cursor.rowcount > 0:
        print("Student deleted successfully!")
    else:
        print("Student not found!")

    conn.close()


# 7. Search student by name
def search_student(keyword):
    conn = get_connection()

    students = conn.execute(
        "SELECT * FROM students WHERE name LIKE ?",
        ('%' + keyword + '%',)
    ).fetchall()

    conn.close()

    return [dict(student) for student in students]


# 8. Main program
if __name__ == "__main__":

    create_table()

    while True:

        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Search Student")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":

            name = input("Enter name: ")
            email = input("Enter email: ")
            course = input("Enter course: ")

            add_student(name, email, course)

        elif choice == "2":

            students = get_students()

            for student in students:
                print(student)

        elif choice == "3":

            student_id = int(input("Enter student ID: "))
            name = input("Enter new name: ")
            email = input("Enter new email: ")
            course = input("Enter new course: ")

            update_student(student_id, name, email, course)

        elif choice == "4":

            student_id = int(input("Enter student ID: "))

            delete_student(student_id)

        elif choice == "5":

            keyword = input("Enter student name: ")

            results = search_student(keyword)

            for student in results:
                print(student)

            if not results:
                print("No student found!")

        elif choice == "6":

            print("Thank you for using Student Management System!")
            break

        else:
            print("Invalid choice! Try again.")
