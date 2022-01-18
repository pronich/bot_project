from bot.settings import ENGINE
from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.types as types

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
    role = Column(ChoiceType({"Admin": "Admin", "Student": "Student"}),
                  nullable=False, default="Student")


Base.metadata.create_all(ENGINE)
