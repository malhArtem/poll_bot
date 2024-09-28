from sqlalchemy.ext.asyncio import async_sessionmaker, async_session, AsyncSession
from sqlalchemy.sql.functions import count

from db.base import Base, created_at, updated_at
import datetime
from sqlalchemy import (select, exc)

from sqlalchemy.orm import Mapped, mapped_column


# таблица tests в БД
class Tests(Base):
    __tablename__ = 'tests'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str]
    is_free: Mapped[bool]
    show_answer: Mapped[bool]
    invite_answer: Mapped[bool]
    notify: Mapped[bool]
    detailed_analysis: Mapped[str]
    first_message: Mapped[str]
    last_message: Mapped[str]
    points_greed: Mapped[str]


    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    @staticmethod
    async def add_test(name, is_free, show_answer, invite_answer, notify, detailed_analysis, first_message, last_message, points_greed, session: AsyncSession):
        test = Tests(name=name,
                     is_free=is_free,
                     show_answer=show_answer,
                     invite_answer=invite_answer,
                     notify=notify,
                     detailed_analysis=detailed_analysis,
                     first_message=first_message,
                     last_message=last_message,
                     points_greed=points_greed)
        try:
            test = await session.merge(test)
            await session.flush()
            print(test)
        except exc.IntegrityError as e:
            print(e)
            test = None
        return test


    @staticmethod
    async def get_tests(session: AsyncSession):
        stmt = select(Tests.id)
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_test(id, session: AsyncSession):
        stmt = select(Tests).filter(Tests.id == id)
        user = await session.execute(stmt)
        return user.scalar_one_or_none()


    @staticmethod
    async def stats(session: AsyncSession):
        stmt = select(count(Tests.id))
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
