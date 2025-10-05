from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.src.api.students.dao import StudentDAO
from server.src.api.students.schema import FilterStudents, SStudent, SStudentUpd, StudentRead
from server.src.dao.services import balancer, is_department_available
from server.src.database import get_async_session, get_sync_session
from server.src.api.students.schema import SStudentsOut, SDepartmentOut

students_route = APIRouter(prefix="/students")


@students_route.get("/", summary="Получить список студентов отфильтрованный по параметрам")
async def get_students(
        filter_query: Annotated[FilterStudents, Query()],
        session: AsyncSession = Depends(get_async_session)
):
    students_data = await StudentDAO.find_all(session, filter_query.model_dump(exclude_none=True))
    return [
        SStudentsOut(
            id=student.id,
            first_name=student.first_name,
            last_name=student.last_name,
            department=SDepartmentOut(id=student.department_id, name=student.department.name),
            group=student.group_id
        )
        for student in students_data
    ]


@students_route.get("/{student_id}", summary="Получить одного студента по id", response_model=StudentRead)
async def get_student_by_id(
        student_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    student = await StudentDAO.find_one_or_none_by_id(session, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return student


@students_route.post("/add", summary="Добавление студента")
async def add_student(
        student: SStudent,
        background_tasks: BackgroundTasks,
        sync_session=Depends(get_sync_session),
        session: AsyncSession = Depends(get_async_session),
) -> dict:
    async with session.begin():
        if not await is_department_available(session, student.department_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Нельзя зачислять студента на кафедру без преподавателей"
            )
        added = await StudentDAO.add(session, **student.model_dump())
        if added:
            background_tasks.add_task(balancer.balance, sync_session, added.department_id)
            return {"message": "Студент успешно добавлен!", "student": student}
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ошибка при добавлении студента"
            )


@students_route.put("/{student_id}/update")
async def update_student(
        student_id: int,
        upd_data: SStudentUpd,
        background_tasks: BackgroundTasks,
        sync_session=Depends(get_sync_session),
        session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        student = await StudentDAO.find_one_or_none_by_id(session, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Такого студента нет")
        department_id = student.department_id
        if upd_data.department_id != department_id:
            if not await is_department_available(session, upd_data.department_id):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Нельзя зачислять студента на кафедру без преподавателей"
                )

        # 1) Обновляем поля студента
        student_values = upd_data.model_dump(exclude_none=True)
        marks = student_values.pop("marks", None)  # достаём marks, чтобы обновлять отдельно

        updated = None
        if student_values:  # если есть обычные поля
            updated = await StudentDAO.update_by_id(session, student_id, student_values)

        # 2) Обновляем оценки, если переданы
        if marks:
            await StudentDAO.update_marks(session, student_id, marks)
            updated = True

        if updated:
            if upd_data.department_id:
                # Балансируем новый департамент и прошлый
                background_tasks.add_task(balancer.balance, sync_session, upd_data.department_id)
                background_tasks.add_task(balancer.balance, sync_session, department_id)
            return {"message": "Данные студента успешно обновлены!", "student": updated}
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ошибка при обновлении данных студента!"
            )


@students_route.delete("/{student_id}/delete")
async def delete_student(
        student_id: int,
        background_tasks: BackgroundTasks,
        sync_session=Depends(get_sync_session),
        session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        student = await StudentDAO.find_one_or_none_by_id(session, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Такого студента нет")
        department_id = student.department_id
        deleted = await StudentDAO.delete_by_id(session, student_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Ошибка при отчислении")
        background_tasks.add_task(balancer.balance, sync_session, department_id)
        return {"message": "Студент отчислен"}
