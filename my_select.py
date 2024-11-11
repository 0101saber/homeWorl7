from conf.db import session
from conf.models import Students, Teachers, Journal, Groups, Subjects
from sqlalchemy import func, desc, and_, or_
from sqlalchemy.orm import joinedload, subqueryload


def select_1():
    students = (session.query(Students.fullname, func.round(func.avg(Journal.rate), 2).label('avg_rate'))
                .select_from(Journal).join(Students)
                .group_by(Students.id)
                .order_by(desc('avg_rate'))
                .limit(5).all())

    return students


# Знайти студента із найвищим середнім балом з певного предмета.
def select_2(subject_id=1):
    student = (session.query(Students.fullname, func.round(func.avg(Journal.rate), 2).label('avg_rate'))
               .select_from(Journal).join(Students)
               .filter(Journal.id == subject_id)
               .group_by(Students.id)
               .order_by(desc('avg_rate'))
               .limit(1).all())

    return student


# Знайти середній бал у групах з певного предмета.
def select_3(subject_id=3):
    group_arg_rate = (session.query(Groups.name, func.round(func.avg(Journal.rate), 2).label('avg_rate'))
                      .select_from(Groups).join(Students).join(Journal)
                      .filter(Journal.subject_id == subject_id)
                      .group_by(Groups.id)
                      .all())

    return group_arg_rate


# Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    avg_rate = (session.query(func.round(func.avg(Journal.rate), 2).label('avg_rate')).scalar())

    return avg_rate


# Знайти які курси читає певний викладач.
def select_5(teacher_id=1):
    subjects = session.query(Subjects.name).select_from(Subjects).filter(Subjects.teacher_id == teacher_id).all()

    return subjects


# Знайти список студентів у певній групі.
def select_6(group_id=1):
    students = session.query(Students.fullname).filter(Students.group_id == group_id).all()

    return students


# Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(group_id=3, subject_id=3):
    subjects_rate = (session.query(Subjects.name, Groups.name, Students.fullname, Journal.rate).select_from(Students)
                     .join(Groups).join(Journal)
                     .filter(and_(Journal.subject_id == subject_id, Students.group_id == group_id)).all())

    return subjects_rate


# Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher_id=1):
    arg_rate_subjects = (session.query(Subjects.name, func.round(func.avg(Journal.rate), 2).label('avg_rate'))
                         .select_from(Journal)
                         .join(Subjects)
                         .filter(Subjects.teacher_id == teacher_id)
                         .group_by(Subjects.name).all())

    return arg_rate_subjects


# Знайти список курсів, які відвідує певний студент.
def select_9(student_id=1):
    subjects = session.query(Subjects.name).select_from(Subjects).join(Journal).filter(
        Journal.student_id == student_id).all()

    return subjects


# Список курсів, які певному студенту читає певний викладач.
def select_10(student_id=11, teacher_id=1):
    subjects = (session.query(Subjects.name).select_from(Journal)
                .join(Subjects, Journal.subject_id == Subjects.id)
                .filter(and_(Subjects.teacher_id == teacher_id, Journal.student_id == student_id)).all())

    return subjects
