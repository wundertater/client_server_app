from server.src.dao.basedao import BaseDAO
from server.src.models.department import Department


class DepartmentDAO(BaseDAO):
    model = Department
