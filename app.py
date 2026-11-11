
# app.py

from flask import Flask, request, jsonify, url_for

from student_service import (
    get_all_students,
    get_student,
    create_student,
    replace_student,
    update_student,
    delete_student
)

app = Flask(__name__)


# Validate request data
def validate_student(data, partial=False):
    if not isinstance(data, dict):
        return "JSON object required"

    if not partial and (
        "name" not in data or "semester" not in data
    ):
        return "Name and semester required"

    if not set(data).issubset({"name", "semester"}):
        return "Unsupported field"

    if "name" in data and (
        not isinstance(data["name"], str)
        or not data["name"].strip()
    ):
        return "Invalid name"

    if "semester" in data and (
        type(data["semester"]) is not int
        or not 1 <= data["semester"] <= 12
    ):
        return "Invalid semester"

    return None


# GET: All students
@app.get("/api/students")
def api_get_all_students():
    return jsonify(get_all_students()), 200


# GET: One student
@app.get("/api/students/<int:student_id>")
def api_get_student(student_id):
    student = get_student(student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student), 200


# POST: Create a student
@app.post("/api/students")
def api_create_student():
    data = request.get_json(silent=True)
    error = validate_student(data)

    if error:
        return jsonify({"error": error}), 400

    student = create_student(
        data["name"], data["semester"]
    )

    response = jsonify(student)
    response.status_code = 201
    response.headers["Location"] = url_for(
        "api_get_student",
        student_id=student["id"]
    )

    return response


# PUT: Replace a student
@app.put("/api/students/<int:student_id>")
def api_replace_student(student_id):
    if get_student(student_id) is None:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json(silent=True)
    error = validate_student(data)

    if error:
        return jsonify({"error": error}), 400

    student = replace_student(
        student_id, data["name"], data["semester"]
    )

    return jsonify(student), 200


# PATCH: Partially update a student
@app.patch("/api/students/<int:student_id>")
def api_update_student(student_id):
    if get_student(student_id) is None:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json(silent=True)
    error = validate_student(data, partial=True)

    if error:
        return jsonify({"error": error}), 400

    student = update_student(student_id, data)
    return jsonify(student), 200


# DELETE: Remove a student
@app.delete("/api/students/<int:student_id>")
def api_delete_student(student_id):
    if not delete_student(student_id):
        return jsonify({"error": "Student not found"}), 404

    return "", 204


if __name__ == "__main__":
    app.run(debug=True, port=5000)
