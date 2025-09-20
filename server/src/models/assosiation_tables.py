from sqlalchemy import Column, ForeignKey, Integer, Table

from server.src.database import Base

GroupSubjectTable = Table(
    "group_subject_table",
    Base.metadata,
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
    Column("subject_id", ForeignKey("subjects.id"), primary_key=True),
)

StudentSubjectTable = Table(
    "student_subject_table",
    Base.metadata,
    Column("student_id", ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
    Column("subject_id", ForeignKey("subjects.id"), primary_key=True),
    Column("mark", Integer, nullable=True),
)
