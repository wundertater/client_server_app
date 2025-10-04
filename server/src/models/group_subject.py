from sqlalchemy import Column, ForeignKey, Table

from server.src.database import Base

GroupSubjectTable = Table(
    "group_subject_table",
    Base.metadata,
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
    Column("subject_id", ForeignKey("subjects.id"), primary_key=True),
)
