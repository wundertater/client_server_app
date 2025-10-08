from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from server.src.api.groups.dao import GroupDAO
from server.src.database import get_async_session

groups_route = APIRouter(prefix="/groups")


@groups_route.get("/")
async def get_groups(
        session: AsyncSession = Depends(get_async_session)
):
    return await GroupDAO.find_all(session)
