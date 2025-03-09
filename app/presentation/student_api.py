from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.student import StudentCreate, StudentRead, StudentUpdate
from app.crud.student import create_student, get_student, update_student, delete_student

studentRouter = APIRouter()


@studentRouter.post("/", response_model=StudentRead)
def create_student_endpoint(student: StudentCreate):
    return create_student(student)


@studentRouter.get("/{student_id}", response_model=StudentRead)
def get_student_endpoint(student_id: int):
    student = get_student(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@studentRouter.put("/{student_id}", response_model=StudentRead)
def update_student_endpoint(student_id: int, student: StudentUpdate):
    updated_student = update_student(student_id, student)
    if updated_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student


@studentRouter.delete("/{student_id}", response_model=dict)
def delete_student_endpoint(student_id: int):
    result = delete_student(student_id)
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Student deleted successfully"}
