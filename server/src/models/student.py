from datetime import date

from sqlalchemy import Date, ForeignKey, LargeBinary, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.src.database import Base


class Student(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    birth_date: Mapped[date]
    enroll_date: Mapped[date] = mapped_column(Date, default=date.today(), server_default=func.current_date())
    photo: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))

    group: Mapped["Group"] = relationship("Group", back_populates="students")
    department: Mapped["Department"] = relationship("Department", back_populates="students")
