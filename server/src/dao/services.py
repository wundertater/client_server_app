"""Файл с балансирующей функцией и дополнительной логикой для crud"""
from server.src.api.instructors.dao import InstructorDAO
from server.src.api.students.dao import StudentDAO
from server.src.api.groups.dao import GroupDAO
from math import ceil
from fastapi import HTTPException


async def is_department_available(session, department_id: int) -> bool:
    """Проверка правила: нельзя зачислять студента на кафедру без преподавателей"""
    if await InstructorDAO.find_all(session, {"d": [department_id]}):
        return True
    return False


async def is_last_available_instructor(session, department_id: int) -> bool:
    """Проверка правила: Нельзя увольнять последнего преподавателя пока на кафедре числятся студенты"""
    department_filter = {"d": [department_id]}
    all_instructors = await InstructorDAO.find_all(session, department_filter)
    all_students = await StudentDAO.find_all(session, department_filter)
    if len(all_instructors) < 2 and all_students:
        return True
    return False


class Balancer:
    _MAX_STUDENTS_IN_GROUP = 10

    def _get_group_distribution(self, instructors_in_dep_num, students_in_dep_num):
        A = ceil(students_in_dep_num / self._MAX_STUDENTS_IN_GROUP)
        B = min(students_in_dep_num, instructors_in_dep_num)
        group_num = max(A, B)
        mean_student_num_in_group = ceil(students_in_dep_num / group_num)
        mean_group_num_per_instructor = ceil(group_num / instructors_in_dep_num)
        return group_num, mean_student_num_in_group, mean_group_num_per_instructor

    def balance(self, sync_session, department_id: int) -> None:
        with sync_session.begin():
            instructors, students, groups = self._fetch_data(sync_session, department_id)
            if not students:
                return None

            group_num, mean_student_num_in_group, mean_group_num_per_instructor = self._get_group_distribution(
                len(instructors), len(students))

            if group_num > len(groups):
                new_group = GroupDAO.sync_add(sync_session, department_id=department_id)
                groups.append(new_group)

            elif group_num < len(groups):
                extra_group = groups.pop()
                GroupDAO.sync_delete_by_id(sync_session, extra_group.id)

            self._balance_students(students, groups, mean_student_num_in_group)
            self._balance_instructors(instructors, groups, mean_group_num_per_instructor)

    @staticmethod
    def _balance_students(students, groups, mean_student_num_in_group):
        groups_ids = [group.id for group in groups]
        curr_group_index = 0
        for i, student in enumerate(students, 1):
            student.group_id = groups_ids[curr_group_index]
            if i % mean_student_num_in_group == 0:
                curr_group_index += 1

    @staticmethod
    def _balance_instructors(instructors, groups, mean_group_num_per_instructor):
        instructors_ids = [instructor.id for instructor in instructors]
        curr_instructor_index = 0
        for i, group in enumerate(groups, 1):
            group.instructor_id = instructors_ids[curr_instructor_index]
            if i % mean_group_num_per_instructor == 0:
                curr_instructor_index += 1

    @staticmethod
    def _fetch_data(sync_session, department_id):
        instructors = InstructorDAO.sync_find_all_in_dep(sync_session, department_id)
        students = StudentDAO.sync_find_all_in_dep(sync_session, department_id)
        groups = GroupDAO.sync_find_all_in_dep(sync_session, department_id)
        return instructors, students, groups


balancer = Balancer()
