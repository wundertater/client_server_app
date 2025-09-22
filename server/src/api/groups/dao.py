from sqlalchemy import select, func
from sqlalchemy.orm import Session
from server.src.models.group import Group
from server.src.models.student import Student
from server.src.dao.basedao import BaseDAO


class GroupDAO(BaseDAO):
    model = Group

    @classmethod
    def get_counter(cls, session: Session, department_id: int) -> dict:
        query = (
            select(
                Group.id.label("group_id"),
                func.count(Student.id).label("students_cnt"),
                Group.instructor_id.label("instructor_id"),
            )
            .join(Student, Student.group_id == Group.id)
            .group_by(Group.id, Group.instructor_id)
        )
        query = query.where(Group.department_id == department_id)
        result = session.execute(query)
        return [
            {
                "group_id": row.group_id,
                "students_id_group_cnt": row.students_id_group_cnt,
                "instructor_id": row.instructor_id,
            }
            for row in result
        ]
