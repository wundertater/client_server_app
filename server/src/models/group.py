from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.src.database import Base


class Group(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    instructor_id: Mapped[int] = mapped_column(ForeignKey("instructors.id"))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))

    instructor: Mapped["Instructor"] = relationship("Instructor", back_populates="groups")
    department: Mapped["Department"] = relationship("Department", back_populates="groups")
    students: Mapped[list["Student"]] = relationship("Student", back_populates="group")
