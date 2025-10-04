from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from server.src.api.departments.dao import DepartmentDAO
from server.src.database import get_async_session

departments_route = APIRouter(prefix="/departments")


@departments_route.get("/")
async def get_departments(
        session: AsyncSession = Depends(get_async_session)
):
    return await DepartmentDAO.find_all(session)
