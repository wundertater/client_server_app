from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import String, ForeignKey, select, create_engine, Date

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(engine)


class Base(DeclarativeBase): pass


class Subject(Base):
    __tablename__ = "subjects"

    name: Mapped[str] = mapped_column(primary_key=True)


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    birth_date: Mapped[Date]
    enroll_date: Mapped[Date]
    # photo:
    group_name: Mapped[str] = mapped_column(ForeignKey("Group.name"))


class Group(Base):
    __tablename__ = "groups"

    name: Mapped[str] = mapped_column(primary_key=True)


# with Session() as session:
# 	#какие-то операции с БД


if __name__ == '__main__':
    Base.metadata.create_all(engine)
