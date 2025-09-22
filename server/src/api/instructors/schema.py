from datetime import date

from pydantic import BaseModel, Field


class FilterInstructors(BaseModel):
    d: list[int] = Field([], description="departments")
    g: list[int] = Field([], description="groups")
    fn: str | None = Field(None, description="first name")
    ln: str | None = Field(None, description="last name")


class SInstructor(BaseModel):
    last_name: str
    first_name: str
    birth_date: date
    department_id: int
    photo: bytes | None = None


class SInstructorUpd(BaseModel):
    last_name: str | None = None
    first_name: str | None = None
    birth_date: date | None = None
    department_id: int | None = None
    photo: bytes | None = None


class SDepartmentOut(BaseModel):
    id: int
    name: str


class SInstructorsOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    department: SDepartmentOut
    groups: list[int]
