from datetime import datetime
from typing import Annotated, List, Text
from sqlalchemy import Integer, func, ARRAY, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, class_mapper
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import settings

# sudo su - postgres -c "createuser admin"
#
# postgres=# CREATE USER admin WITH PASSWORD '123456';
# postgres=# ALTER USER admin WITH PASSWORD '123456';
# postgres=# create database alchemy_db;
# postgres=# GRANT ALL PRIVILEGES ON DATABASE alchemy_db TO admin;
# postgres=# ALTER DATABASE alchemy_db OWNER TO admin;
#
# postgres=# \q



DATABASE_URL = settings.get_db_url()

# Создаем асинхронный движок для работы с базой данных
engine = create_async_engine(url=DATABASE_URL)
# Создаем фабрику сессий для взаимодействия с базой данных
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# Создадим аннотацию для колонок таблиц
uniq_str_an = Annotated[str, mapped_column(unique=True)]
# content_an = Annotated[str | None, mapped_column(Text)]
array_or_none_an = Annotated[List[str] | None, mapped_column(ARRAY(String))]


# Базовый класс для всех моделей
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True  # Класс абстрактный, чтобы не создавать отдельную таблицу для него

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'

    def to_dictionary(self) -> dict:
        """Универсальный метод для конвертации объекта SQLAlchemy в словарь"""
        # Получаем маппер для текущей модели
        columns = class_mapper(self.__class__).columns
        # Возвращаем словарь всех колонок и их значений
        return {column.key: getattr(self, column.key) for column in columns}


def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                # Явно не открываем транзакции, так как они уже есть в контексте
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()  # Откатываем сессию при ошибке
                raise e  # Поднимаем исключение дальше
            finally:
                await session.close()  # Закрываем сессию

    return wrapper

if __name__ == "__main__":
    print("DB URL =>", settings.get_db_url())
    print("DB HOST =>", settings.DB_HOST)