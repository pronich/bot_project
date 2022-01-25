import re

from config.settings import ENGINE
from models.models import Users, Classes, Schedule
from sqlalchemy.orm import sessionmaker

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


def add_lessons_info(data):
    user = check_user_in_db(data['id'])
    classes = Classes(
        level=data['classes']['level'],
        time_length=data['classes']['lesson_length'],
        available_lesson=data['classes']['available_lesson']
    )

    for sch in data['classes']['schedule']:
        sched = Schedule(
            day=sch['day'],
            time=sch['time']
        )
        classes.schedule.append(sched)

    user.is_promo = data['is_promo']
    user.status = 'Active'
    user.classes = classes

    session.add(user)
    session.commit()



