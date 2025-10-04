from datetime import date

from pydantic import BaseModel, Field


class FilterStudents(BaseModel):
    d: list[int] = Field([], description="departments")
    g: list[int] = Field([], description="groups")
    fn: str | None = Field(None, description="first name")
    ln: str | None = Field(None, description="last name")


class SStudent(BaseModel):
    last_name: str
    first_name: str
    birth_date: date
    department_id: int
    photo: bytes | None = None


class SStudentUpd(BaseModel):
    last_name: str | None = None
    first_name: str | None = None
    birth_date: date | None = None
    department_id: int | None = None
    photo: bytes | None = None
    marks: dict[int, int | None] | None = None  # {subject_id: mark}

class SubjectBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class SubjectWithMark(BaseModel):
    subject: SubjectBase
    mark: int | None

    class Config:
        orm_mode = True


class StudentRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: date
    enroll_date: date
    group_id: int | None
    department_id: int
    student_subjects: list[SubjectWithMark]

    class Config:
        orm_mode = True