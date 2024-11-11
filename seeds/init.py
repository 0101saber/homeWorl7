from faker import Faker
from sqlalchemy.exc import SQLAlchemyError
from random import randint, choice

from conf.db import session
from conf.models import Students, Teachers, Journal, Groups, Subjects

FAKE_GROUPS = ['D1', 'D2', 'D3']
FAKE_SUBJECTS = ['Literature', 'Physics', 'Chemistry', 'Biology', 'Geography', 'History']

NUMBER_STUDENTS = 50
NUMBER_GROUPS = 3
NUMBER_TEACHER = 5
NUMBER_SUBJECTS = 5
NUMBER_STUDENTS_JOURNAL = 20

fake = Faker('uk-UA')


def insert_groups():
    for name in FAKE_GROUPS:
        group = Groups(name=name)
        session.add(group)


def insert_students():
    group = session.query(Groups).all()
    for _ in range(NUMBER_STUDENTS):
        student = Students(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            birthday=fake.date_between(start_date='-80y', end_date='-13y'),
            group_id=choice(group).id
        )
        session.add(student)


def insert_teachers():
    for _ in range(NUMBER_TEACHER):
        teacher = Teachers(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        session.add(teacher)


def insert_subjects():
    teacher = session.query(Teachers).all()
    for name in ['Literature', 'Physics', 'Chemistry', 'Biology', 'Geography', 'History']:
        subject = Subjects(
            name=name,
            teacher_id=choice(teacher).id
        )
        session.add(subject)


def insert_journal():
    student = session.query(Students).all()
    subject = session.query(Subjects).all()
    for _ in range(NUMBER_STUDENTS_JOURNAL):
        journal = Journal(
            rate=randint(1, 12),
            created_at=fake.date_time_between(start_date='-1y'),
            student_id=choice(student).id,
            subject_id=choice(subject).id,
        )
        session.add(journal)


if __name__ == '__main__':
    try:
        insert_groups()
        insert_teachers()
        insert_subjects()
        insert_students()
        insert_journal()
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()

