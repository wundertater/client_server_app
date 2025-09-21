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
