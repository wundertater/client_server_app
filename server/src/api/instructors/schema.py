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


class SInstructorUpd(BaseModel):
    last_name: str | None = None
    first_name: str | None = None
    birth_date: date | None = None
    department_id: int | None = None


class SDepartmentOut(BaseModel):
    id: int
    name: str


class SInstructorsOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    department: SDepartmentOut
    groups: list[int]


class InstructorRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: date
    employ_date: date
    department_id: int
    photo_url: str | None = None

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, instructor):
        return cls(
            id=instructor.id,
            first_name=instructor.first_name,
            last_name=instructor.last_name,
            birth_date=instructor.birth_date,
            employ_date=instructor.employ_date,
            department_id=instructor.department_id,
            photo_url=f"/instructors/{instructor.id}/photo" if instructor.photo else None
        )
