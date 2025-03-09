from pydantic import BaseModel

class StudentBase(BaseModel):
    name: str
    age: int
    grade: str

class StudentCreate(StudentBase):
    pass

class StudentRead(StudentBase):
    id: int

class StudentUpdate(StudentBase):
    pass