"""Файл с балансирующей функцией и дополнительной логикой для crud"""
from server.src.api.instructor.dao import InstructorDAO
from server.src.api.students.dao import StudentDAO
from server.src.database import get_sync_db_url
from sqlalchemy.future import select


async def is_department_available(session, department_id) -> bool:
    """Проверка правила: нельзя зачислять студента на кафедру без преподавателей"""
    if await InstructorDAO.find_all(session, {"d": [department_id]}):
        return True
    else:
        return False


class Balancer:
    MAX_STUDENTS_IN_GROUP = 10

    def add_to_group(self, student_id, sync_session):
        print("-------adding to group")
        StudentDAO.sync_update_by_id(sync_session, student_id, {"group_id": 1})

    def balance(self):
        pass

    def fetch_data(self):
        instructors_in_dep_cnt = InstructorDAO.sync_find_all_in_dep()


balancer = Balancer()
