from dao.dao import UserDAO
from database import connection
from asyncio import run

from schemas import UserPydantic, UsernameIdPydantic


@connection
async def select_all_users(session):
    return await UserDAO.get_all_users(session)

@connection
async def select_username_id(session):
    return await UserDAO.get_username_id(session)

@connection
async def select_full_user_info(session, user_id: int):
    result = await UserDAO.get_user_info(session=session, user_id=user_id)
    if result:
        return UserPydantic.from_orm(result).dict()
    return {'message': f'Пользователь с ID {user_id} не найден!'}

@connection
async def select_full_user_info_id(session, user_id: int):
    rez = await UserDAO.find_one_or_none_by_id(session=session, data_id=user_id)
    if rez:
        return UserPydantic.from_orm(rez).dict()
    return {'message': f'Пользователь с ID {user_id} не найден!'}

@connection
async def select_full_user_info_email(session, user_id: int, email: str):
    rez = await UserDAO.find_one_or_none(session=session, id=user_id, email=email)
    if rez:
        return UserPydantic.from_orm(rez).dict()
    return {'message': f'Пользователь с ID {user_id} не найден!'}


if __name__ == "__main__":

    # all_users = run(select_all_users())
    # for i in all_users:
    #     print(i.to_dictionary())

    # Pydantic

    # all_users = run(select_all_users())
    # for i in all_users:
    #     user_pydantic = UserPydantic.from_orm(i)
    #     print(user_pydantic.dict())

    # rez = run(select_username_id())
    # for i in rez:
    #     # print(i)
    #
    #     data = {'user_id': i[0], 'username': i[1]}
    #     print(data)

    # rez = run(select_username_id())
    # for i in rez:
    #     rez = UsernameIdPydantic.from_orm(i)
    #     print(rez.dict())

    # info = run(select_full_user_info(user_id=1))
    # print(info)
    # {'username': 'yakvenalex', 'email': 'example@example.com', 'profile': None}

    # info = run(select_full_user_info(user_id=3))
    # print(info)
    # {'username': 'john_doe', 'email': 'john.doe@example.com', 'profile': {'first_name': 'John', 'last_name': 'Doe', 'age': 28, 'gender': 'мужчина', 'profession': 'инженер', 'interests': ['hiking', 'photography', 'coding'], 'contacts': {'phone': '+123456789', 'email': 'john.doe@example.com'}}}

    # info = run(select_full_user_info(user_id=1113))
    # print(info)
    # {'message': 'Пользователь с ID 1113 не найден!'}

    info = run(select_full_user_info_email(user_id=13, email='bob.smith@example.com'))
    print(info)
