"""Файл содержит endpoints относящиеся к instructors"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from server.src.dao.services import is_last_available_instructor
from server.src.api.instructors.dao import InstructorDAO
from server.src.api.instructors.schema import (
    FilterInstructors,
    SInstructor,
    SInstructorsOut,
    SInstructorUpd,
    SDepartmentOut
)
from server.src.database import get_async_session, get_sync_session
from server.src.dao.services import balancer

instructors_route = APIRouter(prefix="/instructors")


@instructors_route.get("/", summary="Получить всех инструкторов по фильтру")
async def get_instructors(
        filter_query: Annotated[FilterInstructors, Query()],
        session: AsyncSession = Depends(get_async_session)
) -> list[SInstructorsOut]:
    instructors_data = await InstructorDAO.find_all(session, filter_query.model_dump(exclude_none=True))
    return [
        SInstructorsOut(
            id=instructor.id,
            first_name=instructor.first_name,
            last_name=instructor.last_name,
            department=SDepartmentOut(id=instructor.department_id, name=instructor.department.name),
            groups=[group.id for group in instructor.groups]
        )
        for instructor in instructors_data
    ]


@instructors_route.get("/{instructor_id}", summary="Получить 1 инструктора по id")
async def get_instructor_by_id(
        instructor_id: int,
        session: AsyncSession = Depends(get_async_session)
):  # -> SInstructorCard
    instructor = await InstructorDAO.find_one_or_none_by_id(session, instructor_id)
    if not instructor:
        raise HTTPException(status_code=404, detail="Инструктор не найден")
    return instructor


@instructors_route.post("/add")
async def add_instructor(
        instructor: SInstructor,
        background_tasks: BackgroundTasks,
        sync_session=Depends(get_sync_session),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    async with session.begin():
        added = await InstructorDAO.add(session, **instructor.model_dump())
        if added:
            background_tasks.add_task(balancer.balance, sync_session, added.department_id)
            return {"message": "Инструктор успешно добавлен!", "instructors": instructor}
        else:
            return {"message": "Ошибка при добавлении инструктора!"}


@instructors_route.put("/{instructor_id}/update")
async def update_instructor(
        instructor_id: int,
        upd_data: SInstructorUpd,
        background_tasks: BackgroundTasks,
        sync_session=Depends(get_sync_session),
        session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        instructor = await InstructorDAO.find_one_or_none_by_id(session, instructor_id)
        if not instructor:
            raise HTTPException(status_code=404, detail="Такого инструктора нет")
        department_id = instructor.department_id
        if upd_data.department_id and await is_last_available_instructor(session, department_id):
            return {"message": "Нельзя переводить последнего инструктора пока на кафедре числятся студенты"}
        updated = await InstructorDAO.update_by_id(session, instructor_id, upd_data.model_dump(exclude_none=True))
        if updated:
            if upd_data.department_id:
                # Балансируем новый департамент и прошлый
                background_tasks.add_task(balancer.balance, sync_session, department_id)
                background_tasks.add_task(balancer.balance, sync_session, upd_data.department_id)
            return {"message": "Данные инструктора успешно обновлены!", "instructors": updated}
        else:
            return {"message": "Ошибка при обновлении данных инструктора!"}


@instructors_route.delete("/{instructor_id}/delete")
async def delete_instructor(
        instructor_id: int,
        background_tasks: BackgroundTasks,
        sync_session=Depends(get_sync_session),
        session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        instructor = await InstructorDAO.find_one_or_none_by_id(session, instructor_id)
        if not instructor:
            raise HTTPException(status_code=404, detail="Такого инструктора нет")
        department_id = instructor.department_id
        if await is_last_available_instructor(session, department_id):
            return {"message": "Нельзя увольнять последнего инструктора пока на кафедре числятся студенты"}
        deleted = await InstructorDAO.delete_by_id(session, instructor_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Ошибка при увольнении")
        background_tasks.add_task(balancer.balance, sync_session, department_id)
        return {"message": "Инструктор уволен"}
