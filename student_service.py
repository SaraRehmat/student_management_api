
# student_service.py

students = {
    101: {"id": 101, "name": "Ali", "semester": 3},
    102: {"id": 102, "name": "Sara", "semester": 5}
}


def get_all_students():
    return list(students.values())


def get_student(student_id):
    return students.get(student_id)


def create_student(name, semester):
    new_id = max(students, default=100) + 1

    student = {
        "id": new_id,
        "name": name,
        "semester": semester
    }

    students[new_id] = student
    return student


def replace_student(student_id, name, semester):
    if student_id not in students:
        return None

    students[student_id] = {
        "id": student_id,
        "name": name,
        "semester": semester
    }

    return students[student_id]


def update_student(student_id, changes):
    if student_id not in students:
        return None

    students[student_id].update(changes)
    return students[student_id]


def delete_student(student_id):
    if student_id not in students:
        return False

    del students[student_id]
    return True
