from fastapi import FastAPI
from database import collection
from models import Student

app = FastAPI()

# Home API
@app.get("/")
def home():
    return {"message": "Welcome to Student Management API"}

# Add Student
@app.post("/students")
def add_student(student: Student):
    collection.insert_one(student.dict())
    return {
        "message": "Student Added Successfully"
    }

# View All Students
@app.get("/students")
def get_students():

    students = []

    for student in collection.find({}, {"_id": 0}):
        students.append(student)

    return students

# View One Student
@app.get("/students/{student_id}")
def get_student(student_id: int):

    student = collection.find_one(
        {"id": student_id},
        {"_id": 0}
    )

    if student:
        return student

    return {"message": "Student not found"}

# Update Student
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):

    result = collection.update_one(
        {"id": student_id},
        {"$set": student.dict()}
    )

    if result.modified_count == 1:
        return {"message": "Student Updated Successfully"}

    return {"message": "Student not found"}

# Delete Student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    result = collection.delete_one(
        {"id": student_id}
    )

    if result.deleted_count == 1:
        return {"message": "Student Deleted Successfully"}

    return {"message": "Student not found"}