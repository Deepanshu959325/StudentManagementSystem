from flask import Flask, request, jsonify, render_template

from database import (
    get_connection,
    create_table,
    add_student,
    get_students,
    update_student
)

# Create Flask application
app = Flask(__name__)


# Create database table
create_table()


@app.route("/")
def home():
    return render_template("index.html")


# API 1: GET - View all students
@app.route("/api/students", methods=["GET"])
def view_students():

    students = get_students()

    return jsonify({
        "success": True,
        "students": students
    }), 200


# API 2: POST - Add a new student
@app.route("/api/students", methods=["POST"])
def create_student():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Please send valid JSON data."
        }), 400

    name = data.get("name")
    email = data.get("email")
    course = data.get("course")

    if not all(
        isinstance(value, str) and value.strip()
        for value in [name, email, course]
    ):
        return jsonify({
            "success": False,
            "message": "Name, email and course are required."
        }), 400

    result = add_student(
        name.strip(),
        email.strip(),
        course.strip()
    )

    if not result:
        return jsonify({
            "success": False,
            "message": "Email already exists."
        }), 409

    return jsonify({
        "success": True,
        "message": "Student added successfully!"
    }), 201


# API 3: PUT - Update student
@app.route("/api/students/<int:student_id>", methods=["PUT"])
def edit_student(student_id):

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Please send valid JSON data."
        }), 400

    name = data.get("name")
    email = data.get("email")
    course = data.get("course")

    if not all(
        isinstance(value, str) and value.strip()
        for value in [name, email, course]
    ):
        return jsonify({
            "success": False,
            "message": "Name, email and course are required."
        }), 400

    result = update_student(
        student_id,
        name.strip(),
        email.strip(),
        course.strip()
    )

    if not result:
        return jsonify({
            "success": False,
            "message": "Student not found or email already exists."
        }), 404

    return jsonify({
        "success": True,
        "message": "Student updated successfully!"
    }), 200


# API 4: DELETE - Delete student
@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def remove_student(student_id):

    conn = get_connection()

    cursor = conn.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()

    if not deleted:
        return jsonify({
            "success": False,
            "message": "Student not found."
        }), 404

    return jsonify({
        "success": True,
        "message": "Student deleted successfully!"
    }), 200


# Run Flask application
if __name__ == "__main__":
    app.run(debug=True)
