"""Файл с балансирующей функцией и дополнительной логикой для crud"""
from server.src.api.instructors.dao import InstructorDAO
from server.src.api.students.dao import StudentDAO
from server.src.api.groups.dao import GroupDAO
from server.src.database import get_sync_db_url
from sqlalchemy.future import select
from math import ceil
from fastapi import HTTPException


async def is_department_available(session, department_id: int) -> bool:
    """Проверка правила: нельзя зачислять студента на кафедру без преподавателей"""
    if await InstructorDAO.find_all(session, {"d": [department_id]}):
        return True
    return False


async def is_last_available_instructor(session, instructor_id: int) -> bool:
    """Проверка правила: Нельзя увольнять последнего преподавателя пока на кафедре числятся студенты"""
    instructor = await InstructorDAO.find_one_or_none_by_id(session, instructor_id)
    if not instructor:
        raise HTTPException(status_code=404, detail="Инструктор не найден")
    department_id = instructor.department_id
    department_filter = {"d": [department_id]}
    all_instructors = await InstructorDAO.find_all(session, department_filter)
    all_students = await StudentDAO.find_all(session, department_filter)
    if len(all_instructors) < 2 and all_students:
        return True
    return False


class Balancer:
    MAX_STUDENTS_IN_GROUP = 10

    def add_to_group(self, student, sync_session):
        student_id = student.id
        student_department_id = student.department_id
        instructors_in_dep_cnt, students_in_dep_cnt, group_counter = self._fetch_data(sync_session,
                                                                                      student_department_id)

        mean_data = self.get_group_distribution(instructors_in_dep_cnt, students_in_dep_cnt)

        StudentDAO.sync_update_by_id(sync_session, student_id, {"group_id": 1})

    def get_group_distribution(self, instructors_in_dep_cnt, students_in_dep_cnt):
        A = ceil(students_in_dep_cnt / self.MAX_STUDENTS_IN_GROUP)
        B = min(students_in_dep_cnt, instructors_in_dep_cnt)
        group_num = max(A, B)
        mean_student_num_in_group = ceil(students_in_dep_cnt / group_num)
        mean_group_num_per_instructor = ceil(instructors_in_dep_cnt / group_num)

        return group_num, mean_student_num_in_group, mean_group_num_per_instructor

    def add_new_group(self, department_id):
        pass

    def balance(self, sync_session, department_id: int):
        instructors_in_dep_cnt, students_in_dep_cnt, group_counter = self._fetch_data(sync_session, department_id)
        group_num, mean_student_num_in_group, mean_group_num_per_instructor = self.get_group_distribution(
            instructors_in_dep_cnt, students_in_dep_cnt)
        # if group_num > len(group_counter):
        #     self.add_new_group()  # balance
        #
        # else:
        #     self.add_to_exist_group()

    def _fetch_data(self, sync_session, department_id):
        with sync_session.begin():
            instructors_in_dep_cnt = len(InstructorDAO.sync_find_all_id_in_dep(sync_session, department_id))
            students_in_dep_cnt = len(StudentDAO.sync_find_all_id_in_dep(sync_session, department_id))
            group_counter = GroupDAO.get_counter(sync_session, department_id)
        return instructors_in_dep_cnt, students_in_dep_cnt, group_counter


balancer = Balancer()

if __name__ == '__main__':
    from server.src.database import sync_session_maker

    session = sync_session_maker()
    with session.begin():
        balancer.fetch_data(session, 1)
