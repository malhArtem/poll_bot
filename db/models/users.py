from sqlalchemy.ext.asyncio import async_sessionmaker, async_session, AsyncSession

from db.base import Base, created_at, updated_at
import datetime
from sqlalchemy import (select, exc, update)

from sqlalchemy.orm import Mapped, mapped_column


# таблица users в БД
class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)

    referral_code: Mapped[str] = mapped_column(nullable=True)
    referral_company: Mapped[str] = mapped_column(nullable=True)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    @staticmethod
    async def add_user(user_id, first_name, last_name, username, session: AsyncSession, referral_code=None, referral_company=None):
        stmt = select(Users).filter(Users.user_id == user_id)
        user = (await session.execute(stmt)).scalar_one_or_none()
        if user is None:
            user = Users(user_id=user_id, first_name=first_name, last_name=last_name,
                         username=username, referral_code=referral_code, referral_company=referral_company)
            try:
                session.add(user)
            # await session.commit()
            except Exception as e:
                print(e)
        elif ((referral_code is not None or referral_company is not None) and
              (user.referral_company is None and user.referral_code is None)):
            stmt = update(Users).values(referral_company=referral_company, referral_code=referral_code)
            await session.execute(stmt)


    @staticmethod
    async def get_users(session: AsyncSession):
        stmt = select(Users)
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_user(user_id, session: AsyncSession):
        stmt = select(Users).filter(Users.user_id == user_id)
        user = await session.execute(stmt)
        return user.scalar_one_or_none()

    @staticmethod
    async def update_user(user_id, session: AsyncSession, first_name=None, last_name=None, username=None, referral_code=None):
        user = await session.get(Users, user_id)

        if user is not None:
            user.first_name = first_name if first_name is not None else user.first_name
            user.last_name = last_name if last_name is not None else user.last_name
            user.username = username if username is not None else user.username
            user.referral_code = referral_code if referral_code is not None else user.referral_code
            user.updated_at = datetime.datetime.utcnow()
        await session.commit()


    @staticmethod
    async def stats(session: AsyncSession):
        stmt = select(Users)
        res = await session.execute(stmt)
        users = res.scalars().all()
        today = datetime.datetime.utcnow().date()
        today_users = 0
        for user in users:
            if user.created_at.date() == today:
                today_users += 1

        return len(users), today_users
