from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate

def create_student(db: Session, student: StudentCreate):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def update_student(db: Session, student_id: int, student: StudentUpdate):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student:
        for key, value in student.dict(exclude_unset=True).items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student