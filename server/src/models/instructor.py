from datetime import date

from sqlalchemy import Date, ForeignKey, LargeBinary, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.src.database import Base


class Instructor(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    birth_date: Mapped[date]
    employ_date: Mapped[date] = mapped_column(Date, default=date.today(), server_default=func.current_date())
    photo: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    photo_mime: Mapped[str | None] = mapped_column(nullable=True)  # тип файла фото
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))

    department: Mapped["Department"] = relationship("Department", back_populates="instructors")
    groups: Mapped[list["Group"]] = relationship("Group", back_populates="instructor")
