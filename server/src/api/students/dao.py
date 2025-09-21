from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import update as sqlalchemy_update
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

    @classmethod
    def sync_update_by_id(cls, session, obj_id: int, values: dict):
        stmt = (
            sqlalchemy_update(cls.model)
            .where(cls.model.id == obj_id)
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        try:
            with session.begin():
                result = session.execute(stmt)

                if result.rowcount == 0:
                    return None

                return None
        except Exception as e:
            raise e