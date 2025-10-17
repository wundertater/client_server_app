from datetime import date

from pydantic import BaseModel, Field, field_validator


def validate_birth_date(value: date) -> date:
    """Проверка корректности даты рождения."""
    today = date.today()
    min_date = date(1900, 1, 1)
    if value > today:
        raise ValueError("Дата рождения не может быть в будущем")
    if value < min_date:
        raise ValueError("Дата рождения слишком старая (должна быть после 1900 года)")
    return value


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

    @field_validator("birth_date")
    def validate_birth_date(cls, value: date) -> date:
        return validate_birth_date(value)


class SDepartmentOut(BaseModel):
    id: int
    name: str


class SStudentsOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    department: SDepartmentOut
    group: int | None


class SStudentUpd(BaseModel):
    last_name: str | None = None
    first_name: str | None = None
    birth_date: date | None = None
    department_id: int | None = None
    marks: dict[int, int | None] | None = None  # {subject_id: mark}

    @field_validator("birth_date")
    def validate_birth_date(cls, value: date | None) -> date | None:
        # Проверяем только если значение указано
        if value is not None:
            return validate_birth_date(value)

    @field_validator("marks")
    def validate_marks(cls, value: dict[int, int | None] | None) -> dict[int, int | None] | None:
        if value is None:
            return value  # marks не переданы — пропускаем
        for subject_id, mark in value.items():
            if mark is None:
                continue  # допускаем отсутствие оценки
            # Проверяем, что это число
            if not isinstance(mark, int):
                raise ValueError(f"Оценка по предмету {subject_id} должна быть числом")
            # Проверяем диапазон
            if not (0 < mark <= 5):
                raise ValueError(f"Оценка по предмету {subject_id} должна быть в диапазоне от 1 до 5 включительно")
        return value


class SubjectBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class SubjectWithMark(BaseModel):
    subject: SubjectBase
    mark: int | None

    class Config:
        from_attributes = True


class StudentRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: date
    enroll_date: date
    group_id: int | None
    department_id: int
    student_subjects: list[SubjectWithMark]
    photo_url: str | None = None

    class Config:
        from_attributes = True
