from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.src.database import Base


class StudentSubject(Base):
    __tablename__ = "student_subject_table"

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), primary_key=True)
    mark: Mapped[int] = mapped_column(nullable=True)

    student: Mapped["Student"] = relationship(back_populates="student_subjects")
    subject: Mapped["Subject"] = relationship(back_populates="student_subjects")