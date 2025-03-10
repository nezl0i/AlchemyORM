from sqlalchemy.ext.asyncio import AsyncSession
from database import connection
from asyncio import run
from models import User


@connection
async def create_user_example_1(username: str, email: str, password: str, session: AsyncSession) -> int:
    """
    Создает нового пользователя с использованием ORM SQLAlchemy.

    Аргументы:
    - username: str - имя пользователя
    - email: str - адрес электронной почты
    - password: str - пароль пользователя
    - session: AsyncSession - асинхронная сессия базы данных

    Возвращает:
    - int - идентификатор созданного пользователя
    """

    user = User(username=username, email=email, password=password)
    session.add(user)
    await session.commit()
    return user.id


if __name__ == '__main__':
    new_user_id = run(create_user_example_1(username="yakvenalex",
                                            email="example@example.com",
                                            password="asdasd"))

    print(f"Новый пользователь с идентификатором {new_user_id} создан")