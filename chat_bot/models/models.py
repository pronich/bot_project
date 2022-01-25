from datetime import time

import sqlalchemy.types as types
from config.settings import ENGINE
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class ChoiceType(types.TypeDecorator):
    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.items() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=False)
    tg_login = Column(String(50), unique=True)
    name = Column(String(50))
    surname = Column(String(100))
    email = Column(String(100))
    phone = Column(String(12))
    status = Column(ChoiceType({"New": "New", "Initial": "Initial", "Active": "Active", "Deactivate": "Deactivate"}),
                    nullable=False, default="New")
    is_promo = Column(Boolean, default=False)
    role = Column(ChoiceType({"Admin": "Admin", "Student": "Student"}),
                  nullable=False, default="Student")
    classes = relationship("Classes", backref='users', uselist=False)


class Classes(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(String(100))
    time_length = Column(ChoiceType({
        "60": "60",
        "90": "90"
    }))
    available_lesson = Column(Integer())
    schedule = relationship("Schedule", backref='classes')
    user_id = Column(Integer(), ForeignKey('users.id'))


class Schedule(Base):
    __tablename__ = 'schedule'

    id = Column(Integer, primary_key=True, autoincrement=True)
    day = Column(ChoiceType({
        "Monday": "Monday",
        "Tuesday": "Tuesday",
        "Wednesday": "Wednesday",
        "Thursday": "Thursday",
        "Friday": "Friday",
        "Saturday": "Saturday"
    }), default="Monday")
    time = Column(Time, default=time(0, 0, 0))
    class_id = Column(Integer(), ForeignKey('classes.id'))


Base.metadata.create_all(ENGINE)
