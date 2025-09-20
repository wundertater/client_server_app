"""Файл data access object, содержит методы получения данных из бд для instructor"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, load_only

from server.src.dao.basedao import BaseDAO
from server.src.models.group import Group
from server.src.models.instructor import Instructor


class InstructorDAO(BaseDAO):
    model = Instructor

    @classmethod
    async def find_all(cls, session: AsyncSession, filters: dict):
        """{"d": "departments", "g": "groups", "fn": first_name", "ln: "last_name"}"""
        query = select(cls.model).options(
            load_only(cls.model.id, cls.model.first_name, cls.model.last_name, cls.model.department_id),
            joinedload(cls.model.department),
            joinedload(cls.model.groups),
        )

        if filters.get("d"):
            query = query.where(cls.model.department_id.in_(filters["d"]))

        if filters.get("g"):
            query = (query.join(Group, Group.instructor_id == cls.model.id)
                     .where(Group.id.in_(filters["g"])).distinct())

        if filters.get("fn"):
            query = query.where(cls.model.first_name.ilike(f"%{filters['fn']}%"))

        if filters.get("ln"):
            query = query.where(cls.model.last_name.ilike(f"%{filters['ln']}%"))

        result = await session.execute(query)
        return result.scalars().unique().all()

    @classmethod
    def sync_find_all_in_dep(cls, session, department_id):
        query = select(cls.model.id).where(cls.model.department_id == department_id)
        result = session.execute(query)
        return result.scalars().all()
