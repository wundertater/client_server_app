from sqlalchemy import delete as sqlalchemy_delete, update as sqlalchemy_update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import load_only


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, session: AsyncSession, filters: dict):
        query = select(cls.model).filter_by(**filters)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_one_or_none_by_id(cls, session: AsyncSession, data_id: int):
        query = select(cls.model).filter_by(id=data_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        new_instance = cls.model(**values)
        session.add(new_instance)
        await session.flush()
        return new_instance

    @classmethod
    async def update_by_id(cls, session: AsyncSession, obj_id: int, values: dict):
        stmt = (
            sqlalchemy_update(cls.model)
            .where(cls.model.id == obj_id)
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        result = await session.execute(stmt)

        if result.rowcount == 0:
            return None

        refreshed = await session.execute(select(cls.model).where(cls.model.id == obj_id))
        return refreshed.scalar_one()

    @classmethod
    async def delete_by_id(cls, session: AsyncSession, obj_id: int):
        stmt = sqlalchemy_delete(cls.model).where(cls.model.id == obj_id).execution_options(synchronize_session="fetch")
        result = await session.execute(stmt)
        return result

    @classmethod
    def sync_find_all_in_dep(cls, sync_session, department_id):
        query = select(cls.model).where(cls.model.department_id == department_id)
        result = sync_session.execute(query)
        return result.scalars().all()

    @classmethod
    def sync_add(cls, sync_session, **values):
        new_instance = cls.model(**values)
        sync_session.add(new_instance)
        sync_session.flush()
        return new_instance

    @classmethod
    def sync_delete_by_id(cls, session, obj_id: int):
        stmt = sqlalchemy_delete(cls.model).where(cls.model.id == obj_id).execution_options(synchronize_session="fetch")
        result = session.execute(stmt)
        return result