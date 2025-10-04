from server.src.dao.basedao import BaseDAO
from server.src.models.group import Group


class GroupDAO(BaseDAO):
    model = Group

