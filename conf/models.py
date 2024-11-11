from sqlalchemy import Column, Integer, String, Date, ForeignKey, SmallInteger, DateTime, func
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birthday = Column(Date)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='SET NULL', onupdate='CASCADE'))
    group = relationship('Groups', back_populates='students')
    journal = relationship('Journal', backref='student')

    @hybrid_property
    def fullname(self):
        return func.concat(self.first_name, ' ', self.last_name)


class Groups(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    students = relationship('Students', back_populates='group')


class Teachers(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    subjects = relationship('Subjects', backref='teacher')

    @hybrid_property
    def fullname(self):
        return func.concat(self.first_name, ' ', self.last_name)


class Subjects(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='SET NULL', onupdate='CASCADE'))
    journal = relationship('Journal', backref='subject')


class Journal(Base):
    __tablename__ = 'journal'
    id = Column(Integer, primary_key=True)
    rate = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='SET NULL', onupdate='CASCADE'))
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='SET NULL', onupdate='CASCADE'))
