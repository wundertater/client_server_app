from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from server.src.api.students.dao import StudentDAO
from server.src.api.students.schema import FilterStudents, SStudent, SStudentUpd
from server.src.dao.services import is_department_available
from server.src.database import get_async_session
from server.src.dao.services import balancer


students_route = APIRouter(prefix="/students")


# TODO сделать выдачу только 10 результатов
@students_route.get("/", summary="Получить список студентов отфильтрованный по параметрам")
async def get_students(
        filter_query: Annotated[FilterStudents, Query()],
        session: AsyncSession = Depends(get_async_session)
):  # TODO сделать схему returnа
    return await StudentDAO.find_all(session, filter_query.model_dump(exclude_none=True))


# TODO проверить что returnится

@students_route.get("/{student_id}", summary="Получить одного студента по id")
async def get_student_by_id(
        student_id: int,
        session: AsyncSession = Depends(get_async_session)
):  # TODO -> SInstructorCard
    student = await StudentDAO.find_one_or_none_by_id(session, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return student


# TODO проверить что returnится

@students_route.post("/add", summary="Добавление студента")
async def add_student(
        student: SStudent,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_async_session),
) -> dict:
    if not await is_department_available(session, student.department_id):
        return {"message": "Нельзя зачислять студента на кафедру без преподавателей"}

    added = await StudentDAO.add(session, **student.model_dump())
    if added:
        # background_tasks.add_task(balancer.add_to_group, added)
        return {"message": "Студент успешно добавлен!", "student": student}
    else:
        return {"message": "Ошибка при добавлении студента!"}


@students_route.put("/{student_id}/update")
async def update_student(
        student_id: int,
        upd_data: SStudentUpd,
        session: AsyncSession = Depends(get_async_session)
):
    if upd_data.department_id and not is_department_available(session, upd_data.department_id):
        return {"message:": "Нельзя зачислять студента на кафедру без преподавателей"}
    updated = await StudentDAO.update_by_id(session, student_id, upd_data.model_dump(exclude_none=True))
    if updated:
        return {"message": "Данные студента успешно обновлены!", "student": updated}
    else:
        # raise HTTP
        return {"message": "Ошибка при обновлении данных студента!"}


@students_route.delete("/{student_id}/delete")
async def delete_student(student_id: int, session: AsyncSession = Depends(get_async_session)):
    deleted = await StudentDAO.delete_by_id(session, student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Ошибка при отчислении")
    return {"message": "Студент отчислен"}
