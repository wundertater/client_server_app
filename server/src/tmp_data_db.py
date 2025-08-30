from pydantic import BaseModel
from datetime import date


class Student(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    enroll_date: date


class Instructor(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    employ_date: date


class Group(BaseModel):
    name: str


class Department(BaseModel):
    name: str


class Subject(BaseModel):
    name: str


# db
ALL_STUDENTS = []
