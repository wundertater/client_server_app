from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import update as sqlalchemy_update
from server.src.dao.basedao import BaseDAO
from server.src.models.student import Student
from server.src.models.student_subject import StudentSubject
from server.src.models.subject import Subject


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
    async def find_one_or_none_by_id(cls, session: AsyncSession, data_id: int):
        query = (
            select(Student)
            .options(
                joinedload(Student.student_subjects).joinedload(StudentSubject.subject)
            )
            .where(Student.id == data_id)
        )
        result = await session.execute(query)
        return result.unique().scalar_one_or_none()

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        # 1. Создаём студента
        new_student = cls.model(**values)
        session.add(new_student)
        await session.flush()  # ⚡ получает ID нового студента

        # 2. Получаем все предметы кафедры студента
        department_id = new_student.department_id
        stmt = select(Subject.id).where(Subject.department_id == department_id)
        result = await session.execute(stmt)
        subject_ids = [row.id for row in result.all()]

        # 3. Создаём StudentSubject для всех предметов с mark = None
        student_subjects = [
            StudentSubject(student_id=new_student.id, subject_id=sid, mark=None)
            for sid in subject_ids
        ]
        session.add_all(student_subjects)
        await session.flush()

        return new_student

    @classmethod
    async def update_marks(cls, session: AsyncSession, student_id: int, marks: dict[int, int | None]):
        for subject_id, mark in marks.items():
            stmt = (
                sqlalchemy_update(StudentSubject)
                .where(
                    StudentSubject.student_id == student_id,
                    StudentSubject.subject_id == subject_id
                )
                .values(mark=mark)
            )
            await session.execute(stmt)
        await session.flush()
