from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.src.database import Base


class Department(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    subjects: Mapped[list["Subject"]] = relationship("Subject", back_populates="department")
    instructors: Mapped[list["Instructor"]] = relationship("Instructor", back_populates="department")
    groups: Mapped[list["Group"]] = relationship("Group", back_populates="department")
    students: Mapped[list["Student"]] = relationship("Student", back_populates="department")
