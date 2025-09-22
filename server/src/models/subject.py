from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.src.database import Base


class Subject(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    department: Mapped["Department"] = relationship("Department", back_populates="subjects")
    student_subjects: Mapped[list["StudentSubject"]] = relationship(
        "StudentSubject", back_populates="subject", cascade="all, delete-orphan"
    )
    students: Mapped[list["Student"]] = relationship(
        "Student", secondary="student_subject_table", back_populates="subjects"
    )