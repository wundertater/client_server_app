from sqlalchemy import select, func
from sqlalchemy.orm import Session
from server.src.models.group import Group
from server.src.models.student import Student
from server.src.dao.basedao import BaseDAO


class GroupDAO(BaseDAO):
    model = Group

