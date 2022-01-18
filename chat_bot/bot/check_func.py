import re

from sqlalchemy.orm import sessionmaker
from settings import ENGINE
from initial_db import Users

Session = sessionmaker(bind=ENGINE)
session = Session()


def check_user_in_db(user):
    result = session.query(Users).filter(Users.id == user).first()
    return result


def create_user(user_info):
    user = check_user_in_db(user_info['id'])
    if user is None:
        u1 = Users(id=user_info['id'],
                   tg_login=user_info['tg_login'],
                   name=user_info['name'],
                   surname=user_info['surname'],
                   email=user_info['email'],
                   phone=user_info['phone'])
        session.add(u1)
        session.commit()
        id = check_user_in_db(user_info['id']).id
        return id
    else:
        return user.id


def retrieve_user_by_login(login):
    result = session.query(Users).filter(Users.tg_login == login).first()
    return result


def get_login(phrase):
    print(re.findall('.me/(.*)', phrase))
    return re.findall('.me/(.*)', phrase)[0]
