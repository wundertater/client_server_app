from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from server.src.dao.basedao import BaseDAO
from server.src.models.student import Student


class StudentDAO(BaseDAO):
    model = Student

    @classmethod
    async def find_all(cls, session: AsyncSession, filters: dict):
        query = select(cls.model).options(
            joinedload(cls.model.group),
            joinedload(cls.model.department),
        )

        if filters.get("d"):
            query = query.where(cls.model.department_id.in_(filters["d"]))

        if filters.get("g"):
            query = query.where(cls.model.group_id.in_(filters["g"]))

        if filters.get("fn"):
            query = query.where(cls.model.first_name.ilike(f"%{filters['fn']}%"))

        if filters.get("ln"):
            query = query.where(cls.model.last_name.ilike(f"%{filters['ln']}%"))

        result = await session.execute(query)
        return result.scalars().unique().all()
