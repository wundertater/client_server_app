from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker
from sqlalchemy import create_engine

from server.src.config import get_async_db_url, get_sync_db_url

# --- ASYNC ---
DATABASE_URL_ASYNC = get_async_db_url()
async_engine = create_async_engine(DATABASE_URL_ASYNC, echo=True)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session():
    async with async_session_maker() as session:
        yield session


# --- SYNC ---
DATABASE_URL_SYNC = get_sync_db_url()
sync_engine = create_engine(DATABASE_URL_SYNC, echo=True)
sync_session_maker = sessionmaker(bind=sync_engine, expire_on_commit=False)


def get_sync_session():
    with sync_session_maker() as session:
        yield session


# --- Base model ---
class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self) -> str:
        return f"{self.__name__.lower()}s"
